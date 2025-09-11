# lib/funcoes_analiticas/transformacoes.py
import math
import numpy as np
from typing import List

def floor_div(a: float, b: float) -> int:
    """Calcula a divisão inteira de dois números."""
    if b != 0:
        return a // b
    return None

def ceil_div(a: float, b: float) -> int:
    """Calcula a divisão inteira arredondada para cima."""
    if b != 0:
        return -(-a // b)
    return None

def mod_inverse(a: float, k: float) -> float:
    """Calcula o inverso modular de 'a' mod 'k'."""
    try:
        return pow(a, -1, k)
    except:
        return None
        
def floor_val(a: float) -> int:
    """Retorna o maior inteiro menor ou igual a 'a'."""
    return math.floor(a)

def ceil_val(a: float) -> int:
    """Retorna o menor inteiro maior ou igual a 'a'."""
    return math.ceil(a)

def sqrt_transform(lst: list) -> list:
    """Aplica a transformação de raiz quadrada."""
    return [np.sqrt(x) for x in lst]

def log_transform(lst: list) -> list:
    """Aplica a transformação logarítmica (ln)."""
    return [np.log(x) if x > 0 else 0 for x in lst]

def reciprocal_transform(lst: list) -> list:
    """Aplica a transformação recíproca (1/x)."""
    return [1 / x if x != 0 else 0 for x in lst]

def sin_transform(lst: list) -> list:
    """Aplica a transformação seno."""
    return [np.sin(x) for x in lst]

def cos_transform(lst: list) -> list:
    """Aplica a transformação cosseno."""
    return [np.cos(x) for x in lst]

def tan_transform(lst: list) -> list:
    """Aplica a transformação tangente."""
    return [np.tan(x) for x in lst]

def mod_transform(lst: list, m: int = 10) -> list:
    """Aplica a transformação de módulo."""
    return [x % m for x in lst]
