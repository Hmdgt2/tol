# lib/funcoes_analiticas/teoria_informacao.py

import numpy as np
from scipy.stats import entropy
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score
from typing import List

# ============================================================
# Entropia
# ============================================================

def shannon_entropy(lst: List[float]) -> float:
    """Calcula a entropia de Shannon de uma distribuição de probabilidade."""
    return entropy(lst)

def normalized_entropy(lst: List[float]) -> float:
    """Calcula a entropia de Shannon normalizada."""
    ent = entropy(lst)
    return ent / np.log(len(lst)) if len(lst) > 1 else 0

# ============================================================
# Informação mútua
# ============================================================

def mutual_info(x: List[int], y: List[int]) -> float:
    """Calcula a informação mútua entre duas listas."""
    return mutual_info_score(x, y)

def normalized_mutual_info(x: List[int], y: List[int]) -> float:
    """Calcula a informação mútua normalizada."""
    return normalized_mutual_info_score(x, y)

# ============================================================
# Divergências
# ============================================================

def kl_divergence(p: List[float], q: List[float]) -> float:
    """Calcula a divergência de Kullback-Leibler entre duas distribuições."""
    return entropy(p, q)

def jensen_shannon(p: List[float], q: List[float]) -> float:
    """Calcula a divergência de Jensen-Shannon entre duas distribuições."""
    p_arr, q_arr = np.array(p), np.array(q)
    m = 0.5 * (p_arr + q_arr)
    return 0.5 * (entropy(p_arr, m) + entropy(q_arr, m))

# ============================================================
# Impureza
# ============================================================

def gini_impurity(lst: List[float]) -> float:
    """Calcula a impureza de Gini de uma distribuição."""
    p = np.array(lst) / np.sum(lst)
    return 1 - np.sum(p ** 2)
