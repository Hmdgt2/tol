# lib/funcoes_analiticas/matematica_especial.py
from scipy.special import gamma, beta, digamma, jn
from sympy import totient, divisors
from typing import List

# Funções especiais
def gamma_transform(lst: list) -> list:
    """Aplica a função Gamma a cada elemento da lista."""
    return [gamma(x) for x in lst if x > 0]

def bessel_j(lst: list, n: int = 0) -> list:
    """Calcula a função de Bessel de primeira espécie."""
    return [jn(n, x) for x in lst]

# Funções baseadas em teoria dos números
def euler_totient(lst: list) -> list:
    """Calcula a função totiente de Euler para cada elemento."""
    return [totient(x) for x in lst if x > 0]

def sum_divisors(lst: list) -> list:
    """Calcula a soma dos divisores de cada elemento."""
    return [sum(divisors(x)) for x in lst]
