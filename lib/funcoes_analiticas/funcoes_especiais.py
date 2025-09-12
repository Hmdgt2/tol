# lib/funcoes_analiticas/funcoes_especiais.py

import numpy as np
from typing import List
from scipy.special import (
    gamma,
    beta,
    zeta,
    jv,
    legendre,
    eval_chebyt,
    eval_chebyu,
    hermite,
    laguerre,
)


# ============================================================
# Funções especiais
# ============================================================

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
    return jv(n, x)


# ============================================================
# Polinómios ortogonais
# ============================================================

def legendre_poly(n: int, x: float) -> float:
    """Calcula o polinómio de Legendre."""
    P = legendre(n)
    return P(x)


def chebyshev_T(n: int, x: float) -> float:
    """Calcula o polinómio de Chebyshev de primeira espécie."""
    return eval_chebyt(n, x)


def chebyshev_U(n: int, x: float) -> float:
    """Calcula o polinómio de Chebyshev de segunda espécie."""
    return eval_chebyu(n, x)


def hermite_poly(n: int, x: float) -> float:
    """Calcula o polinómio de Hermite."""
    H = hermite(n)
    return H(x)


def laguerre_poly(n: int, x: float) -> float:
    """Calcula o polinómio de Laguerre."""
    L = laguerre(n)
    return L(x)


# ============================================================
# Operações discretas
# ============================================================

def discrete_convolution(lst1: List[float], lst2: List[float]) -> List[float]:
    """Calcula a convolução discreta de duas listas."""
    return np.convolve(lst1, lst2).tolist()


def cross_correlation(lst1: List[float], lst2: List[float]) -> List[float]:
    """Calcula a correlação cruzada de duas listas."""
    return np.correlate(lst1, lst2, mode="full").tolist()
