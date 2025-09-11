# lib/funcoes_analiticas/analise_numerica.py

import numpy as np
from typing import Callable, List
from scipy.integrate import quad
from scipy.special import airy
from sympy import isprime


# ============================================================
# Transformadas
# ============================================================

def laplace_transform(f: Callable[[float], float], a: float) -> float:
    """Calcula a transformada de Laplace de uma função."""
    result, _ = quad(lambda t: f(t) * np.exp(-a * t), 0, np.inf)
    return result


def z_transform(lst: List[float]) -> List[complex]:
    """Calcula a transformada Z de uma sequência discreta."""
    return [
        sum(lst[n] * z ** (-n) for n in range(len(lst)))
        for z in range(1, len(lst) + 1)
    ]


# ============================================================
# Funções especiais
# ============================================================

def airy_func(x: float) -> float:
    """Calcula a função Airy."""
    return airy(x)[0]


# ============================================================
# Operações com primos
# ============================================================

def product_primes(lst: List[int]) -> int:
    """Calcula o produto dos números primos numa lista."""
    res = 1
    for x in lst:
        if isprime(x):
            res *= x
    return res


def product_prime_gaps(lst: List[int]) -> int:
    """Calcula o produto dos gaps entre primos numa lista."""
    primes = [x for x in lst if isprime(x)]
    gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
    res = 1
    for g in gaps:
        res *= g
    return res if gaps else 0
