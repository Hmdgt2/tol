# lib/funcoes_analiticas/deteccao_anomalias.py
import numpy as np
from typing import List

def z_score_outliers(lst: list, threshold: float = 2) -> list:
    """Detecta outliers usando o método de Z-score."""
    mean_val = np.mean(lst)
    std_val = np.std(lst)
    return [x for x in lst if std_val != 0 and abs(x - mean_val) / std_val > threshold]

def iqr_outliers(lst: list) -> list:
    """Detecta outliers usando o método do Intervalo Interquartil (IQR)."""
    q1, q3 = np.percentile(lst, [25, 75])
    iqr = q3 - q1
    return [x for x in lst if x < q1 - 1.5 * iqr or x > q3 + 1.5 * iqr]

def rolling_z_score(lst: list, window: int = 3, threshold: float = 2) -> list:
    """Detecta outliers usando um Z-score móvel."""
    outliers = []
    for i in range(len(lst) - window + 1):
        sub = lst[i:i + window]
        mean_val = np.mean(sub)
        std_val = np.std(sub)
        for x in sub:
            if std_val != 0 and abs(x - mean_val) / std_val > threshold:
                outliers.append(x)
    return list(set(outliers))  # Retorna valores únicos
