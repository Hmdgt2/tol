# lib/funcoes_analiticas/aritmetica.py
import math

def add(a: float, b: float) -> float:
    """Calcula a soma de dois números."""
    return a + b

def sub(a: float, b: float) -> float:
    """Calcula a subtração de dois números."""
    return a - b

def mul(a: float, b: float) -> float:
    """Calcula a multiplicação de dois números."""
    return a * b

def div(a: float, b: float) -> float:
    """Calcula a divisão de dois números, evitando divisão por zero."""
    if b != 0:
        return a / b
    return None

def mod(a: float, b: float) -> float:
    """Calcula o resto da divisão de dois números, evitando divisão por zero."""
    if b != 0:
        return a % b
    return None

def pow_func(a: float, b: float) -> float:
    """Calcula a potência de um número."""
    return a ** b

def sqrt(a: float) -> float:
    """Calcula a raiz quadrada de um número."""
    return math.sqrt(a)

def cbrt(a: float) -> float:
    """Calcula a raiz cúbica de um número."""
    return a ** (1/3)

def log_func(a: float) -> float:
    """Calcula o logaritmo natural de um número, se for positivo."""
    if a > 0:
        return math.log(a)
    return None

def exp_func(a: float) -> float:
    """Calcula o exponencial de um número."""
    return math.exp(a)

def neg(a: float) -> float:
    """Retorna o negativo de um número."""
    return -a

def inv(a: float) -> float:
    """Calcula o inverso de um número, se não for zero."""
    if a != 0:
        return 1 / a
    return None

def abs_val(a: float) -> float:
    """Calcula o valor absoluto de um número."""
    return abs(a)
