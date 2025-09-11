# lib/funcoes_analiticas/estatisticas.py
import statistics
import numpy as np
import pandas as pd
from scipy import stats

def mean(lst: list) -> float:
    """Calcula a média de uma lista de números."""
    return statistics.mean(lst)

def median(lst: list) -> float:
    """Calcula a mediana de uma lista de números."""
    return statistics.median(lst)

def mode_func(lst: list) -> float:
    """Calcula a moda de uma lista de números, se existir."""
    try:
        return statistics.mode(lst)
    except:
        return None

def std_func(lst: list) -> float:
    """Calcula o desvio padrão de uma lista de números."""
    return statistics.stdev(lst)

def var_func(lst: list) -> float:
    """Calcula a variância de uma lista de números."""
    return statistics.variance(lst)

def sum_list(lst: list) -> float:
    """Calcula a soma de todos os elementos em uma lista."""
    return sum(lst)

def prod_list(lst: list) -> float:
    """Calcula o produto de todos os elementos em uma lista."""
    res = 1
    for x in lst:
        res *= x
    return res

def min_val(lst: list) -> float:
    """Encontra o valor mínimo em uma lista."""
    return min(lst)

def max_val(lst: list) -> float:
    """Encontra o valor máximo em uma lista."""
    return max(lst)

def range_val(lst: list) -> float:
    """Calcula a diferença entre o valor máximo e mínimo."""
    return max(lst) - min(lst)

def geometric_mean(lst: list) -> float:
    """Calcula a média geométrica de uma lista de números."""
    prod = 1
    for x in lst:
        prod *= x
    return prod ** (1 / len(lst)) if lst else None

def harmonic_mean_func(lst: list) -> float:
    """Calcula a média harmônica de uma lista de números."""
    return len(lst) / sum(1 / x for x in lst if x != 0) if lst else None
    
def skewness_func(lst: list) -> float:
    """Calcula a assimetria da distribuição de uma lista."""
    return stats.skew(lst)

def kurtosis_func(lst: list) -> float:
    """Calcula a curtose de uma lista."""
    return stats.kurtosis(lst)

def percentile_func(lst: list, p: int) -> float:
    """Calcula o percentil de uma lista."""
    return np.percentile(lst, p)

def zscore_func(lst: list) -> list:
    """Calcula o z-score para cada elemento de uma lista."""
    return stats.zscore(lst).tolist()

def mad(lst: list) -> float:
    """Calcula o desvio absoluto mediano."""
    med = np.median(lst)
    return np.median([abs(x - med) for x in lst])
