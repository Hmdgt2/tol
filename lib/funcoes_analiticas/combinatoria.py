# lib/funcoes_analiticas/combinatoria.py

import math
from typing import List
from sympy import factorial
from scipy.special import comb, perm


# ============================================================
# Fatoriais
# ============================================================

def factorial_func(a: int) -> int:
    """Calcula o fatorial de um número inteiro não negativo."""
    return factorial(a) if a >= 0 and int(a) == a else None


# ============================================================
# Combinações e permutações
# ============================================================

def comb_func(n: int, k: int) -> int:
    """Calcula as combinações de n elementos em grupos de k."""
    return comb(n, k)


def perm_func(n: int, k: int) -> int:
    """Calcula as permutações de n elementos em grupos de k."""
    return perm(n, k)


# ============================================================
# Coeficiente multinomial
# ============================================================

def multinomial_coef(lst: List[int]) -> int:
    """Calcula o coeficiente multinomial de uma lista de números."""
    n = sum(lst)
    res = factorial(n)
    for x in lst:
        res //= factorial(int(x))
    return res
