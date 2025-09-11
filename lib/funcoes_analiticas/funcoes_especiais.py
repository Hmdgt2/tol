# lib/funcoes_analiticas/funcoes_especiais.py
from scipy.special import gamma, beta, zeta, hermite, laguerre
from sympy.functions import factorial
import numpy as np

def gamma_func(x: float) -> float:
    """Calcula a função Gamma."""
    return gamma(x)

def beta_func(a: float, b: float) -> float:
    """Calcula a função Beta."""
    return beta(a, b)

def zeta_func(s: float) -> float:
    """Calcula a função Zeta de Riemann."""
    return zeta(s)

def bessel_j(n: int, x: float) -> float:
    """Calcula a função de Bessel de primeira espécie."""
    from scipy.special import jv
    return jv(n, x)

def legendre_poly(n: int, x: float) -> float:
    """Calcula o polinômio de Legendre."""
    from scipy.special import legendre
    P = legendre(n)
    return P(x)

def chebyshev_T(n: int, x: float) -> float:
    """Calcula o polinômio de Chebyshev de primeira espécie."""
    from scipy.special import eval_chebyt
    return eval_chebyt(n, x)

def chebyshev_U(n: int, x: float) -> float:
    """Calcula o polinômio de Chebyshev de segunda espécie."""
    from scipy.special import eval_chebyu
    return eval_chebyu(n, x)

def hermite_poly(n: int, x: float) -> float:
    """Calcula o polinômio de Hermite."""
    H = hermite(n)
    return H(x)

def laguerre_poly(n: int, x: float) -> float:
    """Calcula o polinômio de Laguerre."""
    L = laguerre(n)
    return L(x)

def discrete_convolution(lst1: list, lst2: list) -> list:
    """Calcula a convolução discreta de duas listas."""
    return np.convolve(lst1, lst2).tolist()

def cross_correlation(lst1: list, lst2: list) -> list:
    """Calcula a correlação cruzada de duas listas."""
    return np.correlate(lst1, lst2, mode='full').tolist()
