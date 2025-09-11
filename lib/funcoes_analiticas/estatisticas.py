# lib/funcoes_analiticas/estatisticas.py
import statistics
import numpy as np
import math
import pandas as pd
from scipy import stats
from scipy.stats import poisson, binom, norm, iqr, median_abs_deviation, trim_mean, gmean, hmean, kurtosis, skew, mode, gstd, rankdata
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

def mean_absolute_deviation(lst: list) -> float:
    """Calcula o desvio médio absoluto de uma lista."""
    return np.mean(np.abs(np.array(lst) - np.mean(lst)))

def median_absolute_deviation(lst: list) -> float:
    """Calcula o desvio absoluto mediano de uma lista."""
    med = np.median(lst)
    return np.median([abs(x - med) for x in lst])

def weighted_mean(lst: list, weights: list) -> float:
    """Calcula a média ponderada de uma lista."""
    return np.average(lst, weights=weights)

def variance_ratio(lst1: list, lst2: list) -> float:
    """Calcula a razão das variâncias de duas listas."""
    var2 = np.var(lst2)
    return np.var(lst1) / var2 if var2 != 0 else 0

def normalized_std(lst: list) -> float:
    """Calcula o desvio padrão normalizado (coeficiente de variação)."""
    mean_val = np.mean(lst)
    return np.std(lst) / mean_val if mean_val != 0 else 0

def trimmed_mean(lst: list, percent: float = 0.1) -> float:
    """Calcula a média aparada (trimmed mean) de uma lista."""
    sorted_lst = sorted(lst)
    n = int(len(lst) * percent)
    return np.mean(sorted_lst[n:-n])

def interquartile_range(lst: list) -> float:
    """Calcula o intervalo interquartil de uma lista."""
    q75, q25 = np.percentile(lst, [75, 25])
    return q75 - q25

def percentile_diff(lst: list, p1: float, p2: float) -> float:
    """Calcula a diferença entre dois percentis de uma lista."""
    return np.percentile(lst, p2) - np.percentile(lst, p1)

def median_ratio(lst: list) -> float:
    """Calcula a razão entre a mediana e a média."""
    mean_val = np.mean(lst)
    return np.median(lst) / mean_val if mean_val != 0 else 0

def weighted_std(lst: list, weights: list) -> float:
    """Calcula o desvio padrão ponderado."""
    average = np.average(lst, weights=weights)
    variance = np.average((np.array(lst) - average) ** 2, weights=weights)
    return np.sqrt(variance)

def percentile_rank(lst: list, value: float) -> float:
    """Calcula a classificação percentual de um valor em uma lista."""
    return np.sum([1 for x in lst if x <= value]) / len(lst) if lst else 0

# Inverso do desvio padrão
def inv_std(lst: list) -> float:
    """Calcula o inverso do desvio padrão de uma lista."""
    std = np.std(lst)
    return 1 / std if std != 0 else 0

# Inverso do desvio médio absoluto
def inv_mad(lst: list) -> float:
    """Calcula o inverso do desvio médio absoluto (MAD) de uma lista."""
    mad = np.mean(np.abs(np.array(lst) - np.mean(lst)))
    return 1 / mad if mad != 0 else 0

# Soma de quadrados normalizada
def normalized_square_sum(lst: list) -> list:
    """Calcula a soma de quadrados normalizada de uma lista."""
    squares = [x**2 for x in lst]
    total = sum(squares)
    return [x / total if total != 0 else 0 for x in squares]

# Estatística robusta
def trimmed_mean_func(lst: list, proportion: float = 0.1) -> float:
    """Calcula a média aparada (trimmed mean) de uma lista."""
    return trim_mean(lst, proportion)

# Estatística robusta
def interquartile_range(lst: list) -> float:
    """Calcula o intervalo interquartil (IQR)."""
    return iqr(lst)

def mad(lst: list) -> float:
    """Calcula o desvio absoluto da mediana (MAD)."""
    return median_abs_deviation(lst)

def trimmed_mean(lst: list) -> float:
    """Calcula a média aparada (trimmed mean) com proporção padrão de 0.1."""
    return trim_mean(lst, 0.1)

def geometric_mean(lst: list) -> float:
    """Calcula a média geométrica."""
    return gmean(lst)

def harmonic_mean(lst: list) -> float:
    """Calcula a média harmônica."""
    return hmean(lst)

def percentile90(lst: list) -> float:
    """Retorna o 90º percentil."""
    return np.percentile(lst, 90)

def percentile10(lst: list) -> float:
    """Retorna o 10º percentil."""
    return np.percentile(lst, 10)

def robust_zscore(lst: list) -> list:
    """Calcula o z-score robusto usando a mediana e o MAD."""
    med = np.median(lst)
    mad_val = median_abs_deviation(lst)
    return [(x - med) / mad_val for x in lst]

# Estatística avançada
def sample_variance(lst: list) -> float:
    """Calcula a variância da amostra."""
    return np.var(lst, ddof=1)

def sample_std(lst: list) -> float:
    """Calcula o desvio padrão da amostra."""
    return np.std(lst, ddof=1)

def population_variance(lst: list) -> float:
    """Calcula a variância da população."""
    return np.var(lst)

def population_std(lst: list) -> float:
    """Calcula o desvio padrão da população."""
    return np.std(lst)

def coefficient_variation(lst: list) -> float:
    """Calcula o coeficiente de variação."""
    return np.std(lst) / np.mean(lst) if np.mean(lst) != 0 else 0

def skewness(lst: list) -> float:
    """Calcula a assimetria (skewness)."""
    return skew(lst)

def kurtosis_excess(lst: list) -> float:
    """Calcula a curtose de excesso."""
    return kurtosis(lst)

def geometric_std(lst: list) -> float:
    """Calcula o desvio padrão geométrico."""
    return gstd(lst)

def mode_value(lst: list) -> float:
    """Retorna a moda de uma lista."""
    return mode(lst, keepdims=True).mode[0]

def trimmed_mean_20(lst: list) -> float:
    """Calcula a média aparada com proporção de 20%."""
    return trim_mean(lst, 0.2)

# Estatística Robusta & Outliers
def median_absolute_deviation(lst: list) -> float:
    """Calcula o Desvio Absoluto da Mediana (MAD)."""
    med = np.median(lst)
    return np.median(np.abs(np.array(lst) - med))

def iqr(lst: list) -> float:
    """Calcula o Intervalo Interquartil (IQR)."""
    q1, q3 = np.percentile(lst, [25, 75])
    return q3 - q1

def bowley_skewness(lst: list) -> float:
    """Calcula a assimetria de Bowley."""
    q1, q2, q3 = np.percentile(lst, [25, 50, 75])
    return (q3 + q1 - 2 * q2) / (q3 - q1)

def iqr_outliers(lst: list) -> list:
    """Encontra os índices dos outliers usando a regra do IQR."""
    q1, q3 = np.percentile(lst, [25, 75])
    iqr_val = q3 - q1
    return [i for i, x in enumerate(lst) if x < q1 - 1.5 * iqr_val or x > q3 + 1.5 * iqr_val]

# Séries Numéricas Especiais (não-SymPy)
def arith_series_sum(a: Union[int, float], d: Union[int, float], n: int) -> Union[int, float]:
    """Soma de uma série aritmética."""
    return n / 2 * (2 * a + (n - 1) * d)

def geom_series_sum(a: Union[int, float], r: Union[int, float], n: int) -> Union[int, float]:
    """Soma de uma série geométrica."""
    if r == 1:
        return a * n
    return a * (1 - r ** n) / (1 - r)

def alt_harmonic_sum(n: int) -> float:
    """Soma de uma série harmônica alternada."""
    return sum((-1) ** (k + 1) / k for k in range(1, n + 1))

# Funções de análise de Outliers
def zscore_outliers(lst: list, thr: float = 3.0) -> list:
    """Identifica outliers usando o Z-score."""
    z = (np.array(lst) - np.mean(lst)) / np.std(lst)
    return np.where(np.abs(z) > thr)[0].tolist()

def iqr_outliers(lst: list) -> list:
    """Identifica outliers usando o método do IQR."""
    q1, q3 = np.percentile(lst, [25, 75])
    iqr_val = q3 - q1
    lower_bound = q1 - 1.5 * iqr_val
    upper_bound = q3 + 1.5 * iqr_val
    return [i for i, x in enumerate(lst) if x < lower_bound or x > upper_bound]

def winsorize_series(lst: list, alpha: float = 0.05) -> list:
    """Winsoriza uma série para limitar o efeito de outliers."""
    s = np.sort(lst)
    k = int(len(s) * alpha)
    return np.clip(lst, s[k], s[-k - 1]).tolist()
