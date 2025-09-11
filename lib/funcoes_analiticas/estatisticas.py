# lib/funcoes_analiticas/estatisticas.py
import statistics
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import poisson, binom, norm
from typing import List

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

def z_score_list(lst: list) -> list:
    """Calcula a pontuação Z (z-score) para cada elemento em uma lista."""
    arr = np.array(lst)
    return stats.zscore(arr).tolist() if arr.size > 1 and np.std(arr) != 0 else [0] * len(lst)

def min_max_scale(lst: list) -> list:
    """Normaliza uma lista de números para a escala 0-1."""
    mn = min(lst)
    mx = max(lst)
    return [(x - mn) / (mx - mn) if (mx - mn) != 0 else 0 for x in lst]

def percentile_rank(lst: list) -> list:
    """Calcula o percentil de cada elemento em uma lista."""
    return [stats.percentileofscore(lst, x) for x in lst]

def prob_binomial(n, p, k):
    """Calcula a probabilidade de k sucessos em n tentativas de Binomial."""
    return binom.pmf(k, n, p)

def prob_poisson(lam, k):
    """Calcula a probabilidade de k eventos ocorrerem em Poisson."""
    return poisson.pmf(k, lam)

def prob_normal(mu, sigma, x):
    """Calcula a densidade de probabilidade de x em uma distribuição Normal."""
    return norm.pdf(x, mu, sigma)

def cdf_normal(mu, sigma, x):
    """Calcula a probabilidade cumulativa de x em uma distribuição Normal."""
    return norm.cdf(x, mu, sigma)

def count_even(lst: list) -> int:
    """Conta os números pares em uma lista."""
    return sum(1 for x in lst if x % 2 == 0)

def count_odd(lst: list) -> int:
    """Conta os números ímpares em uma lista."""
    return sum(1 for x in lst if x % 2 == 1)

def is_prime(x: int) -> bool:
    """Verifica se um número é primo."""
    if x < 2: return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0: return False
    return True

def count_prime(lst: list) -> int:
    """Conta os números primos em uma lista."""
    return sum(1 for x in lst if is_prime(x))

def conditional_prob_even(lst: list, next_even: bool = True) -> float:
    """Probabilidade de o próximo número ser par, dado que o anterior foi par."""
    total = sum(1 for x in lst[:-1] if x % 2 == 0)
    count = sum(1 for i in range(len(lst) - 1) if lst[i] % 2 == 0 and lst[i+1] % 2 == (0 if next_even else 1))
    return count / total if total > 0 else 0

def conditional_prob_prime(lst: list, next_prime: bool = True) -> float:
    """Probabilidade de o próximo número ser primo, dado que o anterior foi primo."""
    total = sum(1 for x in lst[:-1] if is_prime(x))
    count = sum(1 for i in range(len(lst) - 1) if is_prime(lst[i]) and is_prime(lst[i+1]) == next_prime)
    return count / total if total > 0 else 0
