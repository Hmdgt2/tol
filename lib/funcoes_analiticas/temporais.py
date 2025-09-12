# lib/funcoes_analiticas/temporais.py

import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import find_peaks
from typing import List

# ============================================================
# Séries temporais com atraso
# ============================================================

def lag_series(lst: List[float], lag: int = 1) -> List[float]:
    """Calcula a diferença entre elementos com um certo atraso (lag)."""
    return [lst[i + lag] - lst[i] for i in range(len(lst) - lag)]

# ============================================================
# Transformada de Fourier
# ============================================================

def fft_magnitude(lst: List[float]) -> List[float]:
    """Calcula a magnitude da Transformada Rápida de Fourier (FFT)."""
    return np.abs(fft(lst)).tolist()

def fft_phase(lst: List[float]) -> List[float]:
    """Calcula a fase da Transformada Rápida de Fourier (FFT)."""
    return np.angle(fft(lst)).tolist()

def ifft_real(lst: List[float]) -> List[float]:
    """Calcula a Transformada Inversa de Fourier (IFFT) e retorna a parte real."""
    return np.real(ifft(lst)).tolist()

def dominant_frequency(lst: List[float]) -> int:
    """Encontra o índice da frequência dominante em uma lista."""
    freqs = np.abs(fft(lst))
    return int(np.argmax(freqs))

# ============================================================
# Autocorrelação
# ============================================================

def autocorr(lst: List[float], lag: int = 1) -> float:
    """Calcula a autocorrelação de uma lista em um determinado atraso."""
    n = len(lst)
    mean = np.mean(lst)
    c0 = np.sum((lst - mean) ** 2) / n
    return np.sum((lst[:n - lag] - mean) * (lst[lag:] - mean)) / ((n - lag) * c0) if c0 != 0 else 0

def autocorr_series(lst: List[float], max_lag: int = 10) -> List[float]:
    """Calcula a série de autocorrelação para múltiplos atrasos."""
    return [autocorr(lst, lag=i) for i in range(1, max_lag + 1)]
