# lib/funcoes_analiticas/matematica_especial.py
from scipy.special import gamma, beta, digamma, jn, jv, yv, erf, erfc, ellipj, eval_legendre, eval_chebyt
from sympy import totient, divisors
from scipy import special as spc
from typing import List, Tuple, Union

# ============================================================
# Funções especiais de listas
# ============================================================
def gamma_transform(lst: List[float]) -> List[float]:
    """Aplica a função Gamma a cada elemento positivo da lista."""
    return [gamma(x) for x in lst if x > 0]

def bessel_j_list(lst: List[float], n: int = 0) -> List[float]:
    """Calcula a função de Bessel de primeira espécie para uma lista."""
    return [jn(n, x) for x in lst]

# ============================================================
# Funções baseadas em teoria dos números
# ============================================================
def euler_totient(lst: List[int]) -> List[int]:
    """Calcula a função totiente de Euler para cada elemento positivo."""
    return [totient(x) for x in lst if x > 0]

def sum_divisors(lst: List[int]) -> List[int]:
    """Calcula a soma dos divisores de cada elemento."""
    return [sum(divisors(x)) for x in lst]

# ============================================================
# Funções especiais individuais
# ============================================================
def gamma_func(x: float) -> float:
    """Calcula a função Gamma."""
    return spc.gamma(x)

def loggamma_func(x: float) -> float:
    """Calcula o logaritmo da função Gamma."""
    return spc.loggamma(x)

def digamma_func(x: float) -> float:
    """Calcula a função Digamma."""
    return spc.digamma(x)

def beta_func(x: float, y: float) -> float:
    """Calcula a função Beta."""
    return beta(x, y)

def bessel_j(n: int, x: float) -> float:
    """Calcula a função de Bessel de primeira espécie."""
    return jv(n, x)

def bessel_y(n: int, x: float) -> float:
    """Calcula a função de Bessel de segunda espécie."""
    return yv(n, x)

def bessel_j0(x: float) -> float:
    """Função de Bessel de primeira espécie de ordem 0."""
    return spc.j0(x)

def bessel_y0(x: float) -> float:
    """Função de Bessel de segunda espécie de ordem 0."""
    return spc.y0(x)

def error_func(x: float) -> float:
    """Função de erro (erf)."""
    return erf(x)

def error_func_c(x: float) -> float:
    """Função de erro complementar (erfc)."""
    return erfc(x)

def elliptic_j(u: float, m: float) -> Tuple[float, float, float]:
    """Funções elípticas de Jacobi (sn, cn, dn)."""
    sn, cn, dn = ellipj(u, m)
    return sn, cn, dn

def legendre_p(n: int, x: float) -> float:
    """Polinômio de Legendre de ordem n."""
    return eval_legendre(n, x)

def chebyshev_t(n: int, x: float) -> float:
    """Polinômio de Chebyshev de primeira espécie de ordem n."""
    return eval_chebyt(n, x)

def airy_ai(x: float) -> float:
    """Função Airy Ai."""
    return spc.airy(x)[0]

def airy_bi(x: float) -> float:
    """Função Airy Bi."""
    return spc.airy(x)[2]
