# lib/funcoes_analiticas/transformacoes.py
import math

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
