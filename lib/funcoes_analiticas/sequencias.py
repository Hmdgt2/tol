# lib/funcoes_analiticas/sequencias.py
import numpy as np
import pandas as pd
from .estatisticas import mean, std_func

def diff(lst: list) -> list:
    """Calcula a diferença entre elementos consecutivos."""
    return [lst[i+1] - lst[i] for i in range(len(lst) - 1)]

def diff_squared(lst: list) -> list:
    """Calcula o quadrado da diferença entre elementos consecutivos."""
    return [(lst[i+1] - lst[i]) ** 2 for i in range(len(lst) - 1)]

def diff_abs(lst: list) -> list:
    """Calcula a diferença absoluta entre elementos consecutivos."""
    return [abs(lst[i+1] - lst[i]) for i in range(len(lst) - 1)]

def diff_ratio(lst: list) -> list:
    """Calcula a proporção entre elementos consecutivos."""
    return [lst[i+1] / lst[i] if lst[i] != 0 else 0 for i in range(len(lst) - 1)]

def cumsum(lst: list) -> list:
    """Calcula a soma cumulativa de uma lista."""
    res = []
    total = 0
    for x in lst:
        total += x
        res.append(total)
    return res

def cumprod(lst: list) -> list:
    """Calcula o produto cumulativo de uma lista."""
    res = []
    total = 1
    for x in lst:
        total *= x
        res.append(total)
    return res

def rolling_sum(lst: list, window: int) -> list:
    """Calcula a soma de uma janela deslizante."""
    return [sum(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_mean(lst: list, window: int) -> list:
    """Calcula a média de uma janela deslizante."""
    return [mean(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rolling_std(lst: list, window: int) -> list:
    """Calcula o desvio padrão de uma janela deslizante."""
    return [std_func(lst[i:i+window]) for i in range(len(lst) - window + 1)]

def rank_array(lst: list) -> list:
    """Calcula o ranking dos elementos em uma lista."""
    return pd.Series(lst).rank().tolist()
