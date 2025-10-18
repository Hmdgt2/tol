# lib/funcoes_analiticas/sinais_nao_lineares.py
import numpy as np
from typing import List
from scipy import signal

def teager_kaiser_energy(signal_data: List[float]) -> List[float]:
    """Energia de Teager-Kaiser para sinais não-lineares."""
    energy = []
    for i in range(1, len(signal_data) - 1):
        e = signal_data[i]**2 - signal_data[i-1] * signal_data[i+1]
        energy.append(e)
    # Preencher extremos
    return [energy[0]] + energy + [energy[-1]]

def higher_order_moments(signal_data: List[float], order: int = 3) -> List[float]:
    """Momentos de ordem superior deslizantes."""
    moments = []
    window_size = min(10, len(signal_data) // 4)
    
    for i in range(len(signal_data)):
        start = max(0, i - window_size // 2)
        end = min(len(signal_data), i + window_size // 2 + 1)
        window = signal_data[start:end]
        
        if len(window) > 0:
            mean = np.mean(window)
            moment = np.mean((window - mean) ** order)
            moments.append(moment)
        else:
            moments.append(0.0)
    
    return moments

def bispectral_analysis(signal_data: List[float]) -> List[List[float]]:
    """Análise bispectral simplificada (transformada de Fourier 2D)."""
    n = len(signal_data)
    bispectrum = [[0.0] * n for _ in range(n)]
    
    # DFT 1D
    dft = np.fft.fft(signal_data)
    
    for f1 in range(n):
        for f2 in range(n):
            f3 = (f1 + f2) % n
            bispectrum[f1][f2] = np.abs(dft[f1] * dft[f2] * np.conj(dft[f3]))
    
    return bispectrum

def empirical_wavelet_transform(signal_data: List[float], num_modes: int = 5) -> List[List[float]]:
    """Transformada empírica de wavelet."""
    n = len(signal_data)
    modes = []
    
    residue = signal_data.copy()
    for _ in range(num_modes):
        if len(residue) < 2:
            break
            
        # Detecção de picos no espectro
        spectrum = np.abs(np.fft.fft(residue))
        peaks = signal.find_peaks(spectrum[:n//2])[0]
        
        if len(peaks) == 0:
            break
            
        # Frequência dominante
        dominant_freq = peaks[np.argmax(spectrum[peaks])]
        
        # Filtrar modo
        t = np.linspace(0, 1, n)
        mode = np.sin(2 * np.pi * dominant_freq * t) * residue
        modes.append(mode.tolist())
        
        # Atualizar resíduo
        residue = [r - m for r, m in zip(residue, mode)]
    
    return modes
