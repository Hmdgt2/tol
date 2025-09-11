# lib/funcoes_analiticas/wavelets.py
# ... (manter as funções existentes)
import numpy as np
import pywt
from typing import List, Tuple

def wavelet_dwt(data: list, wavelet: str = "db1") -> Tuple[list, list]:
    """Aplica a Transformada Discreta de Wavelet (DWT)."""
    cA, cD = pywt.dwt(data, wavelet)
    return cA.tolist(), cD.tolist()

def wavelet_idwt(cA: list, cD: list, wavelet: str = "db1") -> list:
    """Aplica a Transformada Discreta de Wavelet Inversa (IDWT)."""
    return pywt.idwt(np.array(cA), np.array(cD), wavelet).tolist()

def wavelet_wavedec(data: list, level: int = 2, wavelet: str = "db1") -> list:
    """Aplica a decomposição de wavelet multinível."""
    return pywt.wavedec(data, wavelet, level=level)

def wavelet_waverec(coeffs: list, wavelet: str = "db1") -> list:
    """Reconstrói um sinal a partir dos coeficientes de wavelet."""
    return pywt.waverec(coeffs, wavelet).tolist()

def wavelet_energy(data: list, wavelet: str = "db1") -> float:
    """Calcula a energia total de um sinal em diferentes níveis de wavelet."""
    coeffs = pywt.wavedec(data, wavelet)
    return float(sum(np.sum(np.array(c)**2) for c in coeffs))
