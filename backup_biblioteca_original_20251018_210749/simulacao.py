# lib/funcoes_analiticas/simulacao.py
import numpy as np
import random
from scipy.stats import poisson, binom, norm
from typing import List, Callable, Union

# ===================== Amostras de distribuições =====================
def sample_binomial(n: int, p: float, size: int = 10) -> List[int]:
    """Gera uma amostra de uma distribuição Binomial."""
    return list(binom.rvs(n, p, size=size))

def sample_poisson(lam: float, size: int = 10) -> List[int]:
    """Gera uma amostra de uma distribuição de Poisson."""
    return list(poisson.rvs(lam, size=size))

def sample_normal(mu: float, sigma: float, size: int = 10) -> List[float]:
    """Gera uma amostra de uma distribuição Normal."""
    return list(norm.rvs(mu, sigma, size=size))

# ===================== Simulações Monte Carlo =====================
def monte_carlo_sum(target_sum: float, trials: int = 1000) -> float:
    """Calcula a probabilidade de atingir uma soma alvo em amostras aleatórias."""
    hits = [sum(np.random.randint(1, 50, 5)) == target_sum for _ in range(trials)]
    return sum(hits) / trials

def monte_carlo_even_ratio(trials: int = 1000) -> float:
    """Simula a proporção média de números pares em amostras aleatórias."""
    ratios = [
        sum(1 for n in np.random.randint(1, 50, 5) if n % 2 == 0) / 5
        for _ in range(trials)
    ]
    return np.mean(ratios)

def monte_carlo_prime_ratio(trials: int = 1000) -> float:
    """Simula a proporção média de números primos em amostras aleatórias."""
    def is_prime(x: int) -> bool:
        if x < 2: return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0: return False
        return True

    ratios = [
        sum(1 for n in np.random.randint(1, 50, 5) if is_prime(n)) / 5
        for _ in range(trials)
    ]
    return np.mean(ratios)

def monte_carlo_max(trials: int = 1000) -> np.ndarray:
    """Simula os valores máximos de amostras aleatórias."""
    samples = np.random.randint(1, 50, (trials, 5))
    return np.max(samples, axis=1)

def monte_carlo_min(trials: int = 1000) -> np.ndarray:
    """Simula os valores mínimos de amostras aleatórias."""
    samples = np.random.randint(1, 50, (trials, 5))
    return np.min(samples, axis=1)

def monte_carlo_multistep(lst: List[Union[int, float]], steps: int = 5, trials: int = 1000) -> List[List[Union[int, float]]]:
    """Simulação Monte Carlo multi-passos, selecionando elementos aleatórios."""
    n = len(lst)
    return [[lst[random.randint(0, n - 1)] for _ in range(steps)] for _ in range(trials)]

# ===================== MCMC =====================
def metropolis_hastings(
    target_func: Callable[[float], float],
    start: float,
    iterations: int = 1000,
    proposal_std: float = 1.0
) -> List[float]:
    """Geração de amostras MCMC usando o algoritmo Metropolis-Hastings."""
    x = start
    samples = [x]
    for _ in range(iterations):
        x_new = x + np.random.normal(0, proposal_std)
        alpha = min(1, target_func(x_new) / target_func(x))
        if random.random() < alpha:
            x = x_new
        samples.append(x)
    return samples
