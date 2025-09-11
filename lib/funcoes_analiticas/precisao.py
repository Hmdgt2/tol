# lib/funcoes_analiticas/precisao.py
import mpmath

def mpmath_sqrt(x: float) -> float:
    """Calcula a raiz quadrada com alta precisão."""
    return float(mpmath.sqrt(x))

def mpmath_log(x: float) -> float:
    """Calcula o logaritmo com alta precisão."""
    return float(mpmath.log(x)) if x > 0 else None

def mpmath_sin(x: float) -> float:
    """Calcula o seno com alta precisão."""
    return float(mpmath.sin(x))

def mpmath_prod_list(lst: list) -> float:
    """Calcula o produto de uma lista com alta precisão."""
    p = 1
    for x in lst:
        p *= x
    return float(p)

def mpmath_sum_list(lst: list) -> float:
    """Calcula a soma de uma lista com alta precisão."""
    return float(mpmath.fsum(lst))
