# lib/funcoes_analiticas/processamento_sinal.py
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import pywt

def fft_real(lst: list) -> list:
    """Calcula a parte real da Transformada Rápida de Fourier."""
    return np.fft.fft(lst).real.tolist()

def fft_imag(lst: list) -> list:
    """Calcula a parte imaginária da Transformada Rápida de Fourier."""
    return np.fft.fft(lst).imag.tolist()

def fft_magnitude(lst: list) -> list:
    """Calcula a magnitude da Transformada Rápida de Fourier."""
    return np.abs(np.fft.fft(lst)).tolist()

def fft_phase(lst: list) -> list:
    """Calcula a fase da Transformada Rápida de Fourier."""
    return np.angle(np.fft.fft(lst)).tolist()

def low_pass_filter(lst: list, cutoff: float = 0.2, order: int = 3) -> list:
    """Aplica um filtro passa-baixa a uma lista."""
    b, a = butter(order, cutoff, btype='low')
    return filtfilt(b, a, lst).tolist()

def high_pass_filter(lst: list, cutoff: float = 0.2, order: int = 3) -> list:
    """Aplica um filtro passa-alta a uma lista."""
    b, a = butter(order, cutoff, btype='high')
    return filtfilt(b, a, lst).tolist()

def fft_peak_indices(lst: list) -> list:
    """Encontra os índices dos picos na magnitude da FFT."""
    mag = np.abs(np.fft.fft(lst))
    peaks, _ = find_peaks(mag)
    return peaks.tolist()

def wavelet_decompose(lst: list, wavelet: str = 'db1', level: int = 1) -> list:
    """Decompõe uma lista em coeficientes de wavelet."""
    return pywt.wavedec(lst, wavelet, level=level)

def wavelet_reconstruct(coeffs: list, wavelet: str = 'db1') -> list:
    """Reconstrói a lista a partir de coeficientes de wavelet."""
    return pywt.waverec(coeffs, wavelet).tolist()

def detect_cycle_length(lst: list) -> int:
    """Detecta o comprimento do ciclo de repetição mais curto em uma lista."""
    n = len(lst)
    for l in range(1, n // 2 + 1):
        if lst[:l] == lst[l:2 * l]:
            return l
    return 0
