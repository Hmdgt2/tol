import numpy as np
from typing import List

# ============================================================
# Análises exploratórias (não-gráficas)
# ============================================================

def linear_trend_slope(lst: List[float]) -> float:
    """Calcula a inclinação da tendência linear de uma lista."""
    n = len(lst)
    if n < 2:
        return 0.0
    x = np.arange(n)
    y = np.array(lst)
    slope = np.polyfit(x, y, 1)[0]
    return float(slope)

def successive_diff(lst: List[float]) -> List[float]:
    """Calcula a diferença entre elementos sucessivos."""
    return [lst[i] - lst[i - 1] for i in range(1, len(lst))]
