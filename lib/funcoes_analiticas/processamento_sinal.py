# lib/funcoes_analiticas/processamento_sinal.py
import numpy as np
from scipy.fft import fft, ifft
from scipy.signal import butter, filtfilt, find_peaks, hilbert
import pywt
from typing import List

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

def wavelet_decompose_coiflet(lst: list, level: int = 3) -> list:
    """Decompõe uma lista em coeficientes de wavelet Coiflet."""
    return pywt.wavedec(lst, 'coif1', level=level)

def wavelet_reconstruct_coiflet(coeffs: list) -> list:
    """Reconstrói a lista a partir de coeficientes de wavelet Coiflet."""
    return pywt.waverec(coeffs, 'coif1').tolist()

# FFT real
def fft_real(lst: list) -> list:
    """Calcula a Transformada Rápida de Fourier (FFT) real de uma lista."""
    return np.abs(fft(lst)).tolist()

# FFT normalizada
def fft_normalized(lst: list) -> list:
    """Calcula a FFT normalizada."""
    f = np.abs(fft(lst))
    total_sum = np.sum(f)
    return (f / total_sum).tolist() if total_sum != 0 else f.tolist()

# IFFT real
def ifft_real(lst: list) -> list:
    """Calcula a Transformada Inversa de Fourier (IFFT) real."""
    return np.real(ifft(lst)).tolist()

# FFT do log
def fft_log(lst: list) -> list:
    """Calcula a FFT da transformação logarítmica de uma lista."""
    lst_log = [np.log(1 + x) for x in lst]
    return np.abs(fft(lst_log)).tolist()

# FFT da raiz
def fft_sqrt(lst: list) -> list:
    """Calcula a FFT da transformação de raiz quadrada de uma lista."""
    lst_sqrt = [np.sqrt(x) if x >= 0 else 0 for x in lst]
    return np.abs(fft(lst_sqrt)).tolist()

# Transformada de Wavelet Discreta (DWT) - coeficientes aproximados
def dwt_approx(lst: list, wavelet: str = 'db1') -> list:
    """Retorna os coeficientes de aproximação de uma DWT."""
    coeffs = pywt.wavedec(lst, wavelet)
    return coeffs[0].tolist()

# Transformada de Wavelet - coeficientes detalhados
def dwt_detail(lst: list, wavelet: str = 'db1') -> list:
    """Retorna os coeficientes de detalhe de uma DWT."""
    coeffs = pywt.wavedec(lst, wavelet)
    return [c.tolist() for c in coeffs[1:]]

# Transformada Wavelet inversa
def idwt_reconstruct(lst: list, wavelet: str = 'db1') -> list:
    """Reconstrói a partir dos coeficientes de Wavelet."""
    coeffs = pywt.wavedec(lst, wavelet)
    return pywt.waverec(coeffs, wavelet).tolist()

# Transformada de Hilbert
def hilbert_transform(lst: list) -> list:
    """Calcula a Transformada de Hilbert de uma lista."""
    return np.abs(hilbert(lst)).tolist()
