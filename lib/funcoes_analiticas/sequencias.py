import pandas as pd
from .estatisticas import mean, std_func
from typing import List

# ============================================================
# Diferenças entre elementos consecutivos
# ============================================================
def diff(lst: List[float]) -> List[float]:
    """Diferença entre elementos consecutivos (x₂ - x₁)."""
    return [lst[i+1] - lst[i] for i in range(len(lst) - 1)]

def diff_abs(lst: List[float]) -> List[float]:
    """Diferença absoluta entre elementos consecutivos."""
    return [abs(lst[i+1] - lst[i]) for i in range(len(lst) - 1)]

def ratio_consecutive(lst: List[float]) -> List[float]:
    """Razão simples entre elementos consecutivos (x₂ / x₁)."""
    return [lst[i+1] / lst[i] if lst[i] != 0 else 0 for i in range(len(lst) - 1)]

# ============================================================
# Janelas deslizantes (rolling)
# ============================================================
def rolling_sum(lst: List[float], window: int) -> List[float]:
    """Soma em janela deslizante."""
    return [sum(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_mean(lst: List[float], window: int) -> List[float]:
    """Média em janela deslizante."""
    return [mean(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_std(lst: List[float], window: int) -> List[float]:
    """Desvio padrão em janela deslizante."""
    return [std_func(lst[i:i+window]) for i in range(len(lst) - window + 1)]

# ============================================================
# Ranking
# ============================================================
def rank_array(lst: List[float]) -> List[float]:
    """Ranking dos elementos de uma lista."""
    return pd.Series(lst).rank().tolist()
