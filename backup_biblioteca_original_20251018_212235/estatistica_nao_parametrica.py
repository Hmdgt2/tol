# lib/funcoes_analiticas/estatistica_nao_parametrica.py
import numpy as np
from scipy.stats import kendalltau, spearmanr, mannwhitneyu, kruskal, wilcoxon
from typing import List, Tuple

# ============================================================
# Estatística Não Paramétrica
# ============================================================

def kendall_tau(x: List[float], y: List[float]) -> float:
    """
    Calcula o coeficiente de correlação de Kendall.
    
    Args:
        x (List[float]): Primeira amostra.
        y (List[float]): Segunda amostra.
    
    Returns:
        float: Coeficiente de Kendall tau.
    """
    return kendalltau(x, y)[0]


def spearman_corr(x: List[float], y: List[float]) -> float:
    """
    Calcula o coeficiente de correlação de Spearman.
    
    Args:
        x (List[float]): Primeira amostra.
        y (List[float]): Segunda amostra.
    
    Returns:
        float: Coeficiente de Spearman.
    """
    return spearmanr(x, y)[0]


def mann_whitney(x: List[float], y: List[float]) -> float:
    """
    Realiza o teste de soma de postos de Mann-Whitney U.
    
    Args:
        x (List[float]): Primeira amostra.
        y (List[float]): Segunda amostra.
    
    Returns:
        float: Estatística U.
    """
    return mannwhitneyu(x, y).statistic


def kruskal_test(*groups: List[float]) -> float:
    """
    Realiza o teste de Kruskal-Wallis H para múltiplos grupos.
    
    Args:
        *groups (List[float]): Um ou mais grupos de amostras.
    
    Returns:
        float: Estatística H.
    """
    return kruskal(*groups).statistic


def wilcoxon_test(x: List[float], y: List[float]) -> float:
    """
    Realiza o teste de soma de postos de Wilcoxon para amostras pareadas.
    
    Args:
        x (List[float]): Primeira amostra.
        y (List[float]): Segunda amostra.
    
    Returns:
        float: Estatística W.
    """
    return wilcoxon(x, y).statistic


def median_test(x: List[float], y: List[float]) -> float:
    """
    Calcula a diferença entre as medianas de duas amostras.
    
    Args:
        x (List[float]): Primeira amostra.
        y (List[float]): Segunda amostra.
    
    Returns:
        float: Diferença entre as medianas.
    """
    return np.median(x) - np.median(y)


def range_stat(lst: List[float]) -> float:
    """
    Calcula a amplitude (range) de uma amostra.
    
    Args:
        lst (List[float]): Lista de valores.
    
    Returns:
        float: Valor máximo menos mínimo.
    """
    return np.ptp(lst)
