# lib/funcoes_analiticas/temporais.py
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import find_peaks

def lag_series(lst: list, lag: int = 1) -> list:
    """Calcula a diferença entre elementos com um certo atraso (lag)."""
    return [lst[i + lag] - lst[i] for i in range(len(lst) - lag)]

def fft_magnitude(lst: list) -> list:
    """Calcula a magnitude da Transformada Rápida de Fourier."""
    return np.abs(fft(lst)).tolist()

def fft_phase(lst: list) -> list:
    """Calcula a fase da Transformada Rápida de Fourier."""
    return np.angle(fft(lst)).tolist()

def ifft_real(lst: list) -> list:
    """Calcula a Transformada Inversa de Fourier e retorna a parte real."""
    return np.real(ifft(lst)).tolist()

def dominant_frequency(lst: list) -> int:
    """Encontra o índice da frequência dominante em uma lista."""
    freqs = np.abs(fft(lst))
    return int(np.argmax(freqs))

def autocorr(lst: list, lag: int = 1) -> float:
    """Calcula a autocorrelação de uma lista em um determinado atraso."""
    n = len(lst)
    mean = np.mean(lst)
    c0 = np.sum((lst - mean) ** 2) / n
    return np.sum((lst[:n - lag] - mean) * (lst[lag:] - mean)) / ((n - lag) * c0) if c0 != 0 else 0

def autocorr_series(lst: list, max_lag: int = 10) -> list:
    """Calcula a série de autocorrelação para múltiplos atrasos."""
    return [autocorr(lst, lag=i) for i in range(1, max_lag + 1)]
