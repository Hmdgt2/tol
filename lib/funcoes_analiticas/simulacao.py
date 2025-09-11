# lib/funcoes_analiticas/simulacao.py
import numpy as np
import random
from scipy.stats import poisson, binom, norm
from typing import List, Callable

def sample_binomial(n: int, p: float, size: int = 10) -> list:
    """Gera uma amostra de uma distribuição Binomial."""
    return list(binom.rvs(n, p, size=size))

def sample_poisson(lam: float, size: int = 10) -> list:
    """Gera uma amostra de uma distribuição de Poisson."""
    return list(poisson.rvs(lam, size=size))

def sample_normal(mu: float, sigma: float, size: int = 10) -> list:
    """Gera uma amostra de uma distribuição Normal."""
    return list(norm.rvs(mu, sigma, size=size))

def monte_carlo_sum(target_sum: float, trials: int = 1000) -> float:
    """Simula a probabilidade de uma soma alvo em amostras aleatórias."""
    results = []
    for _ in range(trials):
        x = np.random.randint(1, 50, 5)
        results.append(sum(x) == target_sum)
    return sum(results) / trials

def monte_carlo_even_ratio(trials: int = 1000) -> float:
    """Simula a proporção média de números pares em amostras aleatórias."""
    counts = []
    for _ in range(trials):
        x = np.random.randint(1, 50, 5)
        counts.append(sum(1 for n in x if n % 2 == 0) / 5)
    return np.mean(counts)

def monte_carlo_prime_ratio(trials: int = 1000) -> float:
    """Simula a proporção média de números primos em amostras aleatórias."""
    def is_prime(x):
        if x < 2: return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0: return False
        return True
    
    counts = []
    for _ in range(trials):
        x = np.random.randint(1, 50, 5)
        counts.append(sum(1 for n in x if is_prime(n)) / 5)
    return np.mean(counts)

def monte_carlo_max(trials: int = 1000) -> np.ndarray:
    """Simula o valor máximo de amostras aleatórias."""
    return np.max([np.random.randint(1, 50, 5) for _ in range(trials)], axis=1)

def monte_carlo_min(trials: int = 1000) -> np.ndarray:
    """Simula o valor mínimo de amostras aleatórias."""
    return np.min([np.random.randint(1, 50, 5) for _ in range(trials)], axis=1)

def metropolis_hastings(target_func: Callable, start: float, iterations: int = 1000, proposal_std: float = 1) -> list:
    """Simulação MCMC usando o algoritmo Metropolis-Hastings."""
    x = start
    samples = [x]
    for _ in range(iterations):
        x_new = x + np.random.normal(0, proposal_std)
        alpha = min(1, target_func(x_new) / target_func(x))
        if random.random() < alpha:
            x = x_new
        samples.append(x)
    return samples

def monte_carlo_multistep(lst: list, steps: int = 5, trials: int = 1000) -> list:
    """Simulação Monte Carlo multi-passos, escolhendo elementos aleatoriamente."""
    results = []
    n = len(lst)
    for _ in range(trials):
        s = [lst[random.randint(0, n - 1)] for _ in range(steps)]
        results.append(s)
    return results
