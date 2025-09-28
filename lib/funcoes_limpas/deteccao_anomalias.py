
import numpy as np
from typing import List

def z_score_outliers(lst: List[float], threshold: float=2.0) -> List[float]:
    '\n    Detecta outliers usando o método de Z-score.\n    \n    Args:\n        lst (List[float]): Lista de valores.\n        threshold (float): Limite de desvio padrão para considerar outlier.\n    \n    Returns:\n        List[float]: Lista de valores considerados outliers.\n    '
    mean_val = np.mean(lst)
    std_val = np.std(lst)
    return [x for x in lst if ((std_val != 0) and ((abs((x - mean_val)) / std_val) > threshold))]

def rolling_z_score(lst: List[float], window: int=3, threshold: float=2.0) -> List[float]:
    '\n    Detecta outliers usando um Z-score móvel.\n    \n    Args:\n        lst (List[float]): Lista de valores.\n        window (int): Tamanho da janela móvel.\n        threshold (float): Limite de desvio padrão para considerar outlier.\n    \n    Returns:\n        List[float]: Lista de valores considerados outliers, sem duplicados.\n    '
    outliers = []
    for i in range(((len(lst) - window) + 1)):
        sub = lst[i:(i + window)]
        mean_val = np.mean(sub)
        std_val = np.std(sub)
        outliers.extend([x for x in sub if ((std_val != 0) and ((abs((x - mean_val)) / std_val) > threshold))])
    return list(set(outliers))
