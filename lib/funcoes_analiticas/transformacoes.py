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

# Raiz cúbica
def cbrt_transform(lst: list) -> list:
    """Aplica a transformação de raiz cúbica."""
    return [x**(1/3) for x in lst]

# Potência 2
def square_transform(lst: list) -> list:
    """Aplica a transformação de potência 2."""
    return [x**2 for x in lst]

# Potência 3
def cube_transform(lst: list) -> list:
    """Aplica a transformação de potência 3."""
    return [x**3 for x in lst]

# Logaritmo base 10
def log10_transform(lst: list) -> list:
    """Aplica a transformação de logaritmo base 10."""
    return [np.log10(x) if x > 0 else 0 for x in lst]

# Transformação exponencial
def exp_transform(lst: list) -> list:
    """Aplica a transformação exponencial."""
    return [np.exp(x) for x in lst]

# Transformação arcoseno
def arcsin_transform(lst: list) -> list:
    """Aplica a transformação arcoseno, normalizando a entrada."""
    max_v = max(lst)
    return [np.arcsin(x / max_v) for x in lst if max_v != 0]

# Transformação arccoseno
def arccos_transform(lst: list) -> list:
    """Aplica a transformação arccoseno, normalizando a entrada."""
    max_v = max(lst)
    return [np.arccos(x / max_v) for x in lst if max_v != 0]

# Transformação arctangente
def arctan_transform(lst: list) -> list:
    """Aplica a transformação arctangente."""
    return [np.arctan(x) for x in lst]

# Normalização Min-Max
def minmax_normalize(lst: list) -> list:
    """Normaliza uma lista usando o método Min-Max."""
    min_v, max_v = min(lst), max(lst)
    return [(x - min_v) / (max_v - min_v) if max_v != min_v else 0 for x in lst]

# Normalização Z-Score
def zscore_normalize(lst: list) -> list:
    """Normaliza uma lista usando o método Z-Score."""
    mean = np.mean(lst)
    std = np.std(lst)
    return [(x - mean) / std if std != 0 else 0 for x in lst]

# Normalização log
def log_normalize(lst: list) -> list:
    """Normaliza uma lista usando a transformação logarítmica."""
    return [np.log(1 + x) for x in lst]

# Transformação raiz log
def sqrt_log_transform(lst: list) -> list:
    """Aplica a transformação de raiz logarítmica."""
    return [np.sqrt(np.log(1 + x)) for x in lst]

# Transformação trigonométrica centrada
def centered_sin(lst: list) -> list:
    """Aplica a transformação seno centrada na média."""
    mean = np.mean(lst)
    return [np.sin(x - mean) for x in lst]
