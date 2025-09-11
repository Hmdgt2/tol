# lib/funcoes_analiticas/estatistica_nao_parametrica.py
import numpy as np
from scipy.stats import kendalltau, spearmanr, mannwhitneyu, kruskal, wilcoxon
from typing import List, Tuple

def kendall_tau(x: list, y: list) -> float:
    """Calcula o coeficiente de correlação de Kendall."""
    return kendalltau(x, y)[0]

def spearman_corr(x: list, y: list) -> float:
    """Calcula o coeficiente de correlação de Spearman."""
    return spearmanr(x, y)[0]

def mann_whitney(x: list, y: list) -> float:
    """Realiza o teste de soma de postos de Mann-Whitney U."""
    return mannwhitneyu(x, y).statistic

def kruskal_test(*groups: list) -> float:
    """Realiza o teste de Kruskal-Wallis H."""
    return kruskal(*groups).statistic

def wilcoxon_test(x: list, y: list) -> float:
    """Realiza o teste de soma de postos de Wilcoxon (para amostras pareadas)."""
    return wilcoxon(x, y).statistic

def median_test(x: list, y: list) -> float:
    """Calcula a diferença entre as medianas de duas listas."""
    return np.median(x) - np.median(y)

def range_stat(lst: list) -> float:
    """Calcula a amplitude (range)."""
    return np.ptp(lst)
