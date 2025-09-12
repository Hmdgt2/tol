# lib/funcoes_analiticas/sequencias.py
import numpy as np
import pandas as pd
from .estatisticas import mean, std_func
from typing import List

# ===================== Diferenças =====================
def diff(lst: List[float]) -> List[float]:
    """Calcula a diferença entre elementos consecutivos."""
    return [lst[i+1] - lst[i] for i in range(len(lst) - 1)]

def diff_squared(lst: List[float]) -> List[float]:
    """Calcula o quadrado da diferença entre elementos consecutivos."""
    return [(lst[i+1] - lst[i])**2 for i in range(len(lst) - 1)]

def diff_abs(lst: List[float]) -> List[float]:
    """Calcula a diferença absoluta entre elementos consecutivos."""
    return [abs(lst[i+1] - lst[i]) for i in range(len(lst) - 1)]

def diff_ratio(lst: List[float]) -> List[float]:
    """Calcula a razão entre elementos consecutivos."""
    return [lst[i+1] / lst[i] if lst[i] != 0 else 0 for i in range(len(lst) - 1)]

# ===================== Cumulativos =====================
def cumsum(lst: List[float]) -> List[float]:
    """Calcula a soma cumulativa de uma lista."""
    res = []
    total = 0
    for x in lst:
        total += x
        res.append(total)
    return res

def cumprod(lst: List[float]) -> List[float]:
    """Calcula o produto cumulativo de uma lista."""
    res = []
    total = 1
    for x in lst:
        total *= x
        res.append(total)
    return res

# ===================== Janelas deslizantes =====================
def rolling_sum(lst: List[float], window: int) -> List[float]:
    """Calcula a soma de uma janela deslizante."""
    return [sum(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_mean(lst: List[float], window: int) -> List[float]:
    """Calcula a média de uma janela deslizante."""
    return [mean(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_std(lst: List[float], window: int) -> List[float]:
    """Calcula o desvio padrão de uma janela deslizante."""
    return [std_func(lst[i:i+window]) for i in range(len(lst) - window + 1)]

# ===================== Ranking =====================
def rank_array(lst: List[float]) -> List[float]:
    """Calcula o ranking dos elementos em uma lista."""
    return pd.Series(lst).rank().tolist()
