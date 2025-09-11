# lib/funcoes_analiticas/analise_numerica.py
import numpy as np
from scipy.integrate import quad
from scipy.special import airy

def laplace_transform(f: Callable, a: float) -> float:
    """Calcula a transformada de Laplace de uma função."""
    result, _ = quad(lambda t: f(t) * np.exp(-a * t), 0, np.inf)
    return result

def z_transform(lst: list) -> list:
    """Calcula a transformada Z de uma sequência discreta."""
    return [sum([lst[n] * z ** (-n) for n in range(len(lst))]) for z in range(1, len(lst) + 1)]

def airy_func(x: float) -> float:
    """Calcula a função Airy."""
    return airy(x)[0]

def product_primes(lst: list) -> float:
    """Calcula o produto dos números primos em uma lista."""
    from sympy import isprime
    res = 1
    for x in lst:
        if isprime(x):
            res *= x
    return res

def product_prime_gaps(lst: list) -> float:
    """Calcula o produto dos gaps entre primos em uma lista."""
    from sympy import isprime
    primes = [x for x in lst if isprime(x)]
    gaps = [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]
    res = 1
    for g in gaps:
        res *= g
    return res if gaps else 0
