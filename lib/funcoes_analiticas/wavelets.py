# lib/funcoes_analiticas/wavelets.py

import numpy as np
import pywt
from typing import List, Tuple

# ============================================================
# Transformadas Discretas de Wavelet (DWT e IDWT)
# ============================================================

def wavelet_dwt(data: List[float], wavelet: str = "db1") -> Tuple[List[float], List[float]]:
    """Aplica a Transformada Discreta de Wavelet (DWT) de nível 1."""
    cA, cD = pywt.dwt(data, wavelet)
    return cA.tolist(), cD.tolist()

def wavelet_idwt(cA: List[float], cD: List[float], wavelet: str = "db1") -> List[float]:
    """Aplica a Transformada Discreta de Wavelet Inversa (IDWT) de nível 1."""
    return pywt.idwt(np.array(cA), np.array(cD), wavelet).tolist()

# ============================================================
# Decomposição e reconstrução multinível
# ============================================================

def wavelet_wavedec(data: List[float], level: int = 2, wavelet: str = "db1") -> List[List[float]]:
    """Aplica a decomposição de wavelet multinível."""
    coeffs = pywt.wavedec(data, wavelet, level=level)
    return [c.tolist() for c in coeffs]

def wavelet_waverec(coeffs: List[List[float]], wavelet: str = "db1") -> List[float]:
    """Reconstrói um sinal a partir dos coeficientes de wavelet."""
    coeffs_arrays = [np.array(c) for c in coeffs]
    return pywt.waverec(coeffs_arrays, wavelet).tolist()

# ============================================================
# Energia do sinal em diferentes níveis
# ============================================================

def wavelet_energy(data: List[float], wavelet: str = "db1") -> float:
    """Calcula a energia total de um sinal em diferentes níveis de wavelet."""
    coeffs = pywt.wavedec(data, wavelet)
    return float(sum(np.sum(np.array(c)**2) for c in coeffs))
