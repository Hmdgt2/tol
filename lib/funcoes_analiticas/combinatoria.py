# lib/funcoes_analiticas/combinatoria.py
import math
from sympy import factorial, binomial
from scipy.special import comb, perm

def factorial_func(a: int) -> int:
    """Calcula o fatorial de um número inteiro não negativo."""
    return factorial(a) if a >= 0 and int(a) == a else None

def comb_func(n: int, k: int) -> int:
    """Calcula as combinações de n elementos em grupos de k."""
    return comb(n, k)

def perm_func(n: int, k: int) -> int:
    """Calcula as permutações de n elementos em grupos de k."""
    return perm(n, k)

def multinomial_coef(lst: list) -> int:
    """Calcula o coeficiente multinomial de uma lista de números."""
    n = sum(lst)
    res = factorial(n)
    for x in lst:
        res //= factorial(int(x))
    return res
