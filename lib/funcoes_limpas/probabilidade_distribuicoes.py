# lib/funcoes_analiticas/probabilidade_distribuicoes.py
import numpy as np
from numpy.random import multivariate_normal, dirichlet
from typing import List, Dict

def simulate_multinomial_prob(lst: list, probabilities: list, trials: int = 1000) -> list:
    """Simula uma distribuição multinomial."""
    return np.random.multinomial(trials, probabilities).tolist()

def simulate_dirichlet(alpha: list, size: int = 1000) -> list:
    """Simula uma distribuição de Dirichlet."""
    return dirichlet(alpha, size=size).tolist()

def simulate_multivariate_wishart(df: int, scale: list, size: int = 1000) -> np.ndarray:
    """Simula uma distribuição de Wishart multivariada (avançada)."""
    return np.array([np.dot(np.random.randn(df, df), np.random.randn(df, df).T) for _ in range(size)])
