# lib/funcoes_analiticas/matematica_especial.py
from scipy.special import gamma, beta, digamma, jn, jv, yv, erf, erfc, ellipj, legendre, chebyt
from sympy import totient, divisors
import sympy as sp
from scipy import special as spc
from typing import List, Union

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

def gamma_func(x: float) -> float:
    """Aplica a função Gamma."""
    return gamma(x)

def beta_func(x: float, y: float) -> float:
    """Aplica a função Beta."""
    return beta(x, y)

def bessel_j(n: int, x: float) -> float:
    """Calcula a função de Bessel de primeira espécie."""
    return jv(n, x)

def bessel_y(n: int, x: float) -> float:
    """Calcula a função de Bessel de segunda espécie."""
    return yv(n, x)

def error_func(x: float) -> float:
    """Calcula a função de erro."""
    return erf(x)

def error_func_c(x: float) -> float:
    """Calcula a função de erro complementar."""
    return erfc(x)

def elliptic_j(u: float, m: float) -> tuple:
    """Calcula as funções elípticas de Jacobi."""
    sn, cn, dn = ellipj(u, m)
    return sn, cn, dn

def legendre_p(n: int, x: float) -> float:
    """Calcula o polinômio de Legendre."""
    return legendre(n)(x)

def chebyshev_t(n: int, x: float) -> float:
    """Calcula o polinômio de Chebyshev de primeira espécie."""
    return chebyt(n)(x)

def airy_ai(x: float) -> float:
    """Calcula a função Airy Ai."""
    return spc.airy(x)[0]

def airy_bi(x: float) -> float:
    """Calcula a função Airy Bi."""
    return spc.airy(x)[2]

def bessel_j0(x: float) -> float:
    """Calcula a função de Bessel de primeira espécie de ordem 0."""
    return spc.j0(x)

def bessel_y0(x: float) -> float:
    """Calcula a função de Bessel de segunda espécie de ordem 0."""
    return spc.y0(x)

def gamma_func(x: float) -> float:
    """Calcula a função Gamma."""
    return spc.gamma(x)

def loggamma_func(x: float) -> float:
    """Calcula o logaritmo da função Gamma."""
    return spc.loggamma(x)

def digamma_func(x: float) -> float:
    """Calcula a função Digamma."""
    return spc.digamma(x)

def legendre_p(n: int, x: float) -> float:
    """Calcula o polinômio de Legendre de ordem n."""
    return spc.eval_legendre(n, x)

def chebyshev_t(n: int, x: float) -> float:
    """Calcula o polinômio de Chebyshev de primeira espécie de ordem n."""
    return spc.eval_chebyt(n, x)
