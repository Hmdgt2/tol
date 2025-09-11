# lib/funcoes_analiticas/algebra_simbolica.py
import sympy as sp
from typing import Any

x = sp.symbols('x')

def sym_derivative(expr: Any) -> Any:
    """Calcula a derivada de uma expressão simbólica."""
    return sp.diff(expr, x)

def sym_integral(expr: Any) -> Any:
    """Calcula a integral indefinida de uma expressão simbólica."""
    return sp.integrate(expr, x)

def sym_series_expansion(expr: Any, n: int = 5) -> Any:
    """Expande uma expressão em série de Taylor."""
    return expr.series(x, 0, n)

def sym_limit(expr: Any, point: float) -> Any:
    """Calcula o limite de uma expressão."""
    return sp.limit(expr, x, point)

def sym_roots(expr: Any) -> Any:
    """Encontra as raízes de uma expressão."""
    return sp.solve(expr, x)

def sym_simplify(expr: Any) -> Any:
    """Simplifica uma expressão."""
    return sp.simplify(expr)

def sym_expand(expr: Any) -> Any:
    """Expande uma expressão."""
    return sp.expand(expr)

def sym_factor(expr: Any) -> Any:
    """Fatora uma expressão."""
    return sp.factor(expr)
