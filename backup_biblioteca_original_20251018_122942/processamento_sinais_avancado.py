# lib/funcoes_analiticas/processamento_sinais_avancado.py
import numpy as np
from typing import List, Tuple
from scipy import signal, fft
import pywt

# ============================================================
# Transformadas de Tempo-Frequência
# ============================================================

def wigner_ville_distribution(signal_data: List[float]) -> np.ndarray:
    """Distribuição de Wigner-Ville simplificada."""
    n = len(signal_data)
    wvd = np.zeros((n, n), dtype=complex)
    
    for t in range(n):
        for tau in range(-min(t, n-t-1), min(t, n-t-1) + 1):
            if 0 <= t + tau < n and 0 <= t - tau < n:
                wvd[t, tau] = signal_data[t + tau] * np.conj(signal_data[t - tau])
    
    return np.fft.fft(wvd, axis=1)

def reassigned_spectrogram(signal_data: List[float], fs: float = 1.0) -> Tuple:
    """Espectrograma reassigned para melhor resolução tempo-frequência."""
    f, t, Sxx = signal.spectrogram(signal_data, fs=fs)
    
    # Cálculo das derivadas para reassignment
    df = np.gradient(Sxx, axis=0)
    dt = np.gradient(Sxx, axis=1)
    
    # Posições reassigned
    f_reassigned = f[:, np.newaxis] - np.imag(df / (Sxx + 1e-10))
    t_reassigned = t[np.newaxis, :] + np.real(dt / (Sxx + 1e-10))
    
    return f_reassigned, t_reassigned, Sxx

# ============================================================
# Análise de Componentes
# ============================================================

def empirical_mode_decomposition(signal_data: List[float], num_imfs: int = 5) -> List[np.ndarray]:
    """Decomposição Modal Empírica simplificada."""
    residue = np.array(signal_data, dtype=float)
    imfs = []
    
    for _ in range(num_imfs):
        h = residue.copy()
        
        for _ in range(10):  # Número máximo de iterações
            # Encontrar máximos e mínimos
            maxima = signal.argrelextrema(h, np.greater)[0]
            minima = signal.argrelextrema(h, np.less)[0]
            
            if len(maxima) < 2 or len(minima) < 2:
                break
                
            # Interpolar envelopes
            upper_env = np.interp(range(len(h)), maxima, h[maxima])
            lower_env = np.interp(range(len(h)), minima, h[minima])
            
            mean_env = (upper_env + lower_env) / 2
            h = h - mean_env
            
            if np.sum(mean_env**2) < 1e-10:
                break
        
        imfs.append(h.copy())
        residue = residue - h
        
        if np.sum(h**2) < 1e-10:
            break
    
    return imfs

# ============================================================
# Análise de Não-Linearidade
# ============================================================

def higuchi_fractal_dimension(signal_data: List[float], k_max: int = 10) -> float:
    """Dimensão fractal de Higuchi para séries temporais."""
    n = len(signal_data)
    L = []
    
    for k in range(1, k_max + 1):
        Lk = 0
        for m in range(k):
            # Criar sub-séries
            indices = range(m, n, k)
            if len(indices) < 2:
                continue
                
            # Comprimento normalizado
            length = np.sum(np.abs(np.diff([signal_data[i] for i in indices])))
            Lk += length * (n - 1) / (len(indices) * k)
        
        L.append(Lk / k if k > 0 else 0)
    
    # Regressão linear para encontrar dimensão fractal
    k_values = np.arange(1, k_max + 1)
    if len(L) == len(k_values):
        coeffs = np.polyfit(np.log(k_values), np.log(np.array(L) + 1e-10), 1)
        return -coeffs[0]
    
    return 0.0

def sample_entropy(signal_data: List[float], m: int = 2, r: float = 0.2) -> float:
    """Entropia amostral para análise de complexidade."""
    n = len(signal_data)
    if n <= m:
        return 0.0
    
    # Calcular desvio padrão para normalizar r
    std = np.std(signal_data)
    r_norm = r * std
    
    def _maxdist(xi, xj):
        return max(abs(xi[k] - xj[k]) for k in range(len(xi)))
    
    def _phi(m):
        patterns = [signal_data[i:i + m] for i in range(n - m + 1)]
        count = 0
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                if _maxdist(patterns[i], patterns[j]) <= r_norm:
                    count += 1
        return count
    
    A = _phi(m + 1)
    B = _phi(m)
    
    return -np.log(A / B) if A > 0 and B > 0 else 0.0
