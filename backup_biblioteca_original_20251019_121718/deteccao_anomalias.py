# lib/funcoes_analiticas/deteccao_anomalias.py
import numpy as np
from typing import List

# ============================================================
# Detecção de Outliers
# ============================================================

def z_score_outliers(lst: List[float], threshold: float = 2.0) -> List[float]:
    """
    Detecta outliers usando o método de Z-score.
    
    Args:
        lst (List[float]): Lista de valores.
        threshold (float): Limite de desvio padrão para considerar outlier.
    
    Returns:
        List[float]: Lista de valores considerados outliers.
    """
    mean_val = np.mean(lst)
    std_val = np.std(lst)
    return [x for x in lst if std_val != 0 and abs(x - mean_val) / std_val > threshold]


def iqr_outliers(lst: List[float]) -> List[float]:
    """
    Detecta outliers usando o método do Intervalo Interquartil (IQR).
    
    Args:
        lst (List[float]): Lista de valores.
    
    Returns:
        List[float]: Lista de valores considerados outliers.
    """
    q1, q3 = np.percentile(lst, [25, 75])
    iqr = q3 - q1
    return [x for x in lst if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]


def rolling_z_score(lst: List[float], window: int = 3, threshold: float = 2.0) -> List[float]:
    """
    Detecta outliers usando um Z-score móvel.
    
    Args:
        lst (List[float]): Lista de valores.
        window (int): Tamanho da janela móvel.
        threshold (float): Limite de desvio padrão para considerar outlier.
    
    Returns:
        List[float]: Lista de valores considerados outliers, sem duplicados.
    """
    outliers = []
    for i in range(len(lst) - window + 1):
        sub = lst[i:i + window]
        mean_val = np.mean(sub)
        std_val = np.std(sub)
        outliers.extend([x for x in sub if std_val != 0 and abs(x - mean_val) / std_val > threshold])
    return list(set(outliers))
