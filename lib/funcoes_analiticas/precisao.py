# lib/funcoes_analiticas/precisao.py
import mpmath
from typing import List, Optional

# ============================================================
# Funções de cálculo com alta precisão
# ============================================================

def mpmath_sqrt(x: float) -> float:
    """Calcula a raiz quadrada de x com alta precisão."""
    return float(mpmath.sqrt(x))

def mpmath_log(x: float) -> Optional[float]:
    """Calcula o logaritmo natural de x com alta precisão.
    
    Retorna None se x <= 0.
    """
    return float(mpmath.log(x)) if x > 0 else None

def mpmath_sin(x: float) -> float:
    """Calcula o seno de x com alta precisão."""
    return float(mpmath.sin(x))

def mpmath_prod_list(lst: List[float]) -> float:
    """Calcula o produto dos elementos de uma lista com alta precisão."""
    p = 1
    for x in lst:
        p *= x
    return float(p)

def mpmath_sum_list(lst: List[float]) -> float:
    """Calcula a soma dos elementos de uma lista com alta precisão."""
    return float(mpmath.fsum(lst))
