"""
Funções estatísticas gerais e avançadas, incluindo medidas de tendência central,
dispersão, forma, normalização, probabilidade, séries especiais e detecção de outliers.
"""

import statistics
import numpy as np
from scipy import stats
from scipy.stats import poisson, binom, norm, trim_mean, gmean, hmean, kurtosis, skew, median_abs_deviation
from typing import List, Union

# -----------------------------
# Tendência central
# -----------------------------
def mean(lst: list) -> float:
    """Calcula a média de uma lista de números."""
    return statistics.mean(lst)

def median(lst: list) -> float:
    """Calcula a mediana de uma lista de números."""
    return statistics.median(lst)

def mode_func(lst: list) -> Union[float, None]:
    """Calcula a moda de uma lista, se existir."""
    try:
        return statistics.mode(lst)
    except:
        return None

def geometric_mean(lst: list) -> float:
    """Calcula a média geométrica."""
    return gmean(lst)

def harmonic_mean(lst: list) -> float:
    """Calcula a média harmónica."""
    return hmean(lst)

def weighted_mean(lst: list, weights: list) -> float:
    """Calcula a média ponderada."""
    return np.average(lst, weights=weights)

# -----------------------------
# Dispersão
# -----------------------------
def std_func(lst: list) -> float:
    """Calcula o desvio padrão da amostra."""
    return statistics.stdev(lst)

def var_func(lst: list) -> float:
    """Calcula a variância da amostra."""
    return statistics.variance(lst)

def sample_std(lst: list) -> float:
    """Desvio padrão da amostra (ddof=1)."""
    return np.std(lst, ddof=1)

def sample_variance(lst: list) -> float:
    """Variância da amostra (ddof=1)."""
    return np.var(lst, ddof=1)

def population_std(lst: list) -> float:
    """Desvio padrão da população."""
    return np.std(lst)

def population_variance(lst: list) -> float:
    """Variância da população."""
    return np.var(lst)

def coefficient_variation(lst: list) -> float:
    """Coeficiente de variação (desvio/média)."""
    mean_val = np.mean(lst)
    return np.std(lst) / mean_val if mean_val != 0 else 0

def mean_absolute_deviation(lst: list) -> float:
    """Desvio médio absoluto."""
    return np.mean(np.abs(np.array(lst) - np.mean(lst)))

def median_absolute_deviation(lst: list) -> float:
    """Desvio absoluto mediano (MAD)."""
    return median_abs_deviation(lst)

def interquartile_range(lst: list) -> float:
    """Intervalo interquartil (IQR)."""
    return np.percentile(lst, 75) - np.percentile(lst, 25)

# -----------------------------
# Forma da distribuição
# -----------------------------
def skewness(lst: list) -> float:
    """Assimetria (skewness)."""
    return skew(lst)

def kurtosis_excess(lst: list) -> float:
    """Curtose de excesso."""
    return kurtosis(lst)

def bowley_skewness(lst: list) -> float:
    """Assimetria de Bowley."""
    q1, q2, q3 = np.percentile(lst, [25, 50, 75])
    return (q3 + q1 - 2*q2) / (q3 - q1)

# -----------------------------
# Normalização e z-score
# -----------------------------
def z_score_list(lst: list) -> list:
    """Calcula o Z-score para cada elemento."""
    arr = np.array(lst)
    return stats.zscore(arr).tolist() if arr.size > 1 and np.std(arr) != 0 else [0]*len(lst)

def min_max_scale(lst: list) -> list:
    """Normaliza valores para escala 0-1."""
    mn, mx = min(lst), max(lst)
    return [(x - mn)/(mx-mn) if mx-mn != 0 else 0 for x in lst]

def normalized_std(lst: list) -> float:
    """Desvio padrão normalizado (coeficiente de variação)."""
    mean_val = np.mean(lst)
    return np.std(lst)/mean_val if mean_val != 0 else 0

def robust_zscore(lst: list) -> list:
    """Z-score robusto usando mediana e MAD."""
    med = np.median(lst)
    mad_val = median_abs_deviation(lst)
    return [(x - med)/mad_val for x in lst]

# -----------------------------
# Probabilidade
# -----------------------------
def prob_binomial(n, p, k):
    """Probabilidade de k sucessos em n tentativas (Binomial)."""
    return binom.pmf(k, n, p)

def prob_poisson(lam, k):
    """Probabilidade de k eventos (Poisson)."""
    return poisson.pmf(k, lam)

def prob_normal(mu, sigma, x):
    """Densidade de probabilidade Normal."""
    return norm.pdf(x, mu, sigma)

def cdf_normal(mu, sigma, x):
    """Função cumulativa Normal."""
    return norm.cdf(x, mu, sigma)

# -----------------------------
# Contagens e números especiais
# -----------------------------
def count_even(lst: list) -> int:
    """Conta números pares."""
    return sum(1 for x in lst if x%2==0)

def count_odd(lst: list) -> int:
    """Conta números ímpares."""
    return sum(1 for x in lst if x%2==1)

def is_prime(x: int) -> bool:
    """Verifica se x é primo."""
    if x < 2: return False
    for i in range(2,int(x**0.5)+1):
        if x % i == 0: return False
    return True

def count_prime(lst: list) -> int:
    """Conta números primos."""
    return sum(1 for x in lst if is_prime(x))

# -----------------------------
# Séries especiais
# -----------------------------
def arith_series_sum(a: Union[int,float], d: Union[int,float], n:int) -> float:
    """Soma de série aritmética."""
    return n/2*(2*a + (n-1)*d)

def geom_series_sum(a: Union[int,float], r: Union[int,float], n:int) -> float:
    """Soma de série geométrica."""
    if r==1: return a*n
    return a*(1-r**n)/(1-r)

def alt_harmonic_sum(n:int) -> float:
    """Soma de série harmónica alternada."""
    return sum((-1)**(k+1)/k for k in range(1,n+1))

# -----------------------------
# Detecção de outliers
# -----------------------------
def zscore_outliers(lst: list, thr: float = 3.0) -> list:
    """Índices de outliers usando Z-score."""
    z = (np.array(lst)-np.mean(lst))/np.std(lst)
    return np.where(np.abs(z)>thr)[0].tolist()

def iqr_outliers(lst: list) -> list:
    """Índices de outliers usando IQR."""
    q1,q3 = np.percentile(lst,[25,75])
    iqr_val = q3-q1
    lower, upper = q1-1.5*iqr_val, q3+1.5*iqr_val
    return [i for i,x in enumerate(lst) if x<lower or x>upper]

def winsorize_series(lst: list, alpha: float = 0.05) -> list:
    """Winsoriza uma série para limitar outliers."""
    s = np.sort(lst)
    k = int(len(s)*alpha)
    return np.clip(lst, s[k], s[-k-1]).tolist()
