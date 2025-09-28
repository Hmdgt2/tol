
import numpy as np
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import butter, filtfilt, find_peaks, hilbert, welch, savgol_filter, stft, istft, periodogram, lfilter
import pywt
from typing import List, Tuple

def fft_real(lst: List[float]) -> List[float]:
    'Calcula a magnitude da FFT de uma lista.'
    return np.abs(fft(lst)).tolist()

def fft_log(lst: List[float]) -> List[float]:
    'Calcula a FFT da lista transformada em log.'
    lst_log = [np.log((1 + x)) for x in lst]
    return np.abs(fft(lst_log)).tolist()

def fft_sqrt(lst: List[float]) -> List[float]:
    'Calcula a FFT da raiz quadrada da lista.'
    lst_sqrt = [(np.sqrt(x) if (x >= 0) else 0) for x in lst]
    return np.abs(fft(lst_sqrt)).tolist()

def fft_normalized(lst: List[float]) -> List[float]:
    'Calcula a FFT normalizada da lista.'
    f = np.abs(fft(lst))
    total = np.sum(f)
    return ((f / total).tolist() if (total != 0) else f.tolist())

def fft_frequencies(n: int, sample_rate: float) -> List[float]:
    'Retorna as frequências correspondentes à FFT.'
    return fftfreq(n, (1 / sample_rate)).tolist()

def apply_lowpass(lst: List[float], cutoff: float=0.2, order: int=4) -> List[float]:
    'Aplica um filtro passa-baixa Butterworth.'
    (b, a) = butter(order, cutoff, btype='low')
    return filtfilt(b, a, lst).tolist()

def apply_highpass(lst: List[float], cutoff: float=0.2, order: int=4) -> List[float]:
    'Aplica um filtro passa-alta Butterworth.'
    (b, a) = butter(order, cutoff, btype='high')
    return filtfilt(b, a, lst).tolist()

def apply_bandpass(lst: List[float], low: float=0.05, high: float=0.2, order: int=4) -> List[float]:
    'Aplica um filtro passa-faixa Butterworth.'
    (b, a) = butter(order, [low, high], btype='band')
    return filtfilt(b, a, lst).tolist()

def wavelet_decompose(lst: List[float], wavelet: str='db1', level: int=1) -> List[np.ndarray]:
    'Decompõe uma lista em coeficientes de Wavelet (DWT).'
    return pywt.wavedec(lst, wavelet, level=level)

def wavelet_reconstruct(coeffs: List[np.ndarray], wavelet: str='db1') -> List[float]:
    'Reconstrói uma lista a partir de coeficientes de Wavelet.'
    return pywt.waverec(coeffs, wavelet).tolist()

def dwt_approx(lst: List[float], wavelet: str='db1') -> List[float]:
    'Retorna apenas os coeficientes de aproximação da DWT.'
    coeffs = pywt.wavedec(lst, wavelet)
    return coeffs[0].tolist()

def dwt_detail(lst: List[float], wavelet: str='db1') -> List[List[float]]:
    'Retorna os coeficientes de detalhe da DWT.'
    coeffs = pywt.wavedec(lst, wavelet)
    return [c.tolist() for c in coeffs[1:]]

def hilbert_transform(lst: List[float]) -> List[float]:
    'Calcula a Transformada de Hilbert (magnitude).'
    return np.abs(hilbert(lst)).tolist()

def savgol_smooth(lst: List[float], window: int=5, poly: int=2) -> List[float]:
    'Aplica filtro de Savitzky-Golay para suavização.'
    return savgol_filter(lst, window, poly).tolist()

def stft_transform(lst: List[float], fs: float) -> List[List[complex]]:
    'Aplica a Transformada de Fourier de Curto Prazo (STFT).'
    (_, _, Zxx) = stft(lst, fs=fs)
    return Zxx.tolist()

def istft_transform(Z: List[List[complex]], fs: float) -> List[float]:
    'Reconstrói sinal a partir da STFT (ISTFT).'
    (_, x) = istft(Z, fs=fs)
    return x.tolist()

def welch_psd(lst: List[float], fs: float) -> Tuple[(List[float], List[float])]:
    'Calcula o Power Spectral Density pelo método de Welch.'
    (f, P) = welch(lst, fs=fs)
    return (f.tolist(), P.tolist())

def periodogram_psd(lst: List[float], fs: float) -> Tuple[(List[float], List[float])]:
    'Calcula o Power Spectral Density pelo periodograma.'
    (f, P) = periodogram(lst, fs=fs)
    return (f.tolist(), P.tolist())

def spectral_energy(lst: List[float]) -> float:
    'Calcula a energia total do espectro.'
    return np.sum((np.abs(fft(lst)) ** 2))

def spectral_entropy(lst: List[float]) -> float:
    'Calcula a entropia espectral do sinal.'
    X = (np.abs(fft(lst)) ** 2)
    P = ((X / np.sum(X)) if (np.sum(X) != 0) else np.zeros_like(X))
    return (- np.sum((P * np.log2((P + 1e-12)))))

def find_signal_peaks(lst: List[float]) -> List[int]:
    'Encontra os índices dos picos no sinal.'
    (peaks, _) = find_peaks(lst)
    return peaks.tolist()

def detect_cycle_length(lst: List[float]) -> int:
    'Detecta o comprimento do ciclo repetitivo mais curto.'
    n = len(lst)
    for l in range(1, ((n // 2) + 1)):
        if (lst[:l] == lst[l:(2 * l)]):
            return l
    return 0

def butter_lowpass(cutoff: float, fs: float, order: int=5) -> Tuple[(np.ndarray, np.ndarray)]:
    'Retorna coeficientes de filtro Butterworth passa-baixa.'
    return butter(order, cutoff, fs=fs, btype='low')

def filter_signal(b: List[float], a: List[float], x: List[float]) -> List[float]:
    'Filtra um sinal usando os coeficientes b e a.'
    return lfilter(b, a, x).tolist()
