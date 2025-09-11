# lib/funcoes_analiticas/transformacoes.py

import math
import numpy as np
from typing import List, Optional


# ============================================================
# Operações matemáticas básicas
# ============================================================

def floor_div(a: float, b: float) -> Optional[int]:
    """Calcula a divisão inteira de dois números (floor division)."""
    return a // b if b != 0 else None

def ceil_div(a: float, b: float) -> Optional[int]:
    """Calcula a divisão inteira arredondada para cima (ceil division)."""
    return -(-a // b) if b != 0 else None

def mod_inverse(a: int, k: int) -> Optional[int]:
    """Calcula o inverso modular de 'a' mod 'k' (se existir)."""
    try:
        return pow(a, -1, k)
    except ValueError:
        return None

def floor_val(a: float) -> int:
    """Retorna o maior inteiro menor ou igual a 'a'."""
    return math.floor(a)

def ceil_val(a: float) -> int:
    """Retorna o menor inteiro maior ou igual a 'a'."""
    return math.ceil(a)


# ============================================================
# Transformações matemáticas elementares
# ============================================================

def sqrt_transform(lst: List[float]) -> List[float]:
    """Transformação de raiz quadrada."""
    return [np.sqrt(x) for x in lst]

def cbrt_transform(lst: List[float]) -> List[float]:
    """Transformação de raiz cúbica."""
    return [x ** (1 / 3) for x in lst]

def square_transform(lst: List[float]) -> List[float]:
    """Transformação de potência ao quadrado."""
    return [x ** 2 for x in lst]

def cube_transform(lst: List[float]) -> List[float]:
    """Transformação de potência ao cubo."""
    return [x ** 3 for x in lst]

def exp_transform(lst: List[float]) -> List[float]:
    """Transformação exponencial."""
    return [np.exp(x) for x in lst]

def reciprocal_transform(lst: List[float]) -> List[float]:
    """Transformação recíproca (1/x)."""
    return [1 / x if x != 0 else 0 for x in lst]


# ============================================================
# Transformações logarítmicas
# ============================================================

def log_transform(lst: List[float]) -> List[float]:
    """Transformação logarítmica (base e)."""
    return [np.log(x) if x > 0 else 0 for x in lst]

def log10_transform(lst: List[float]) -> List[float]:
    """Transformação logarítmica (base 10)."""
    return [np.log10(x) if x > 0 else 0 for x in lst]

def log_normalize(lst: List[float]) -> List[float]:
    """Normalização com transformação logarítmica."""
    return [np.log(1 + x) for x in lst]

def sqrt_log_transform(lst: List[float]) -> List[float]:
    """Transformação combinada: raiz da transformação logarítmica."""
    return [np.sqrt(np.log(1 + x)) for x in lst]


# ============================================================
# Transformações trigonométricas
# ============================================================

def sin_transform(lst: List[float]) -> List[float]:
    """Transformação seno."""
    return [np.sin(x) for x in lst]

def cos_transform(lst: List[float]) -> List[float]:
    """Transformação cosseno."""
    return [np.cos(x) for x in lst]

def tan_transform(lst: List[float]) -> List[float]:
    """Transformação tangente."""
    return [np.tan(x) for x in lst]

def arcsin_transform(lst: List[float]) -> List[float]:
    """Transformação arcoseno (normalizada pelo valor máximo)."""
    max_v = max(lst)
    return [np.arcsin(x / max_v) for x in lst] if max_v != 0 else [0 for _ in lst]

def arccos_transform(lst: List[float]) -> List[float]:
    """Transformação arccoseno (normalizada pelo valor máximo)."""
    max_v = max(lst)
    return [np.arccos(x / max_v) for x in lst] if max_v != 0 else [0 for _ in lst]

def arctan_transform(lst: List[float]) -> List[float]:
    """Transformação arctangente."""
    return [np.arctan(x) for x in lst]

def centered_sin(lst: List[float]) -> List[float]:
    """Transformação seno centrada na média."""
    mean = np.mean(lst)
    return [np.sin(x - mean) for x in lst]


# ============================================================
# Outras transformações
# ============================================================

def mod_transform(lst: List[float], m: int = 10) -> List[float]:
    """Transformação de módulo (x % m)."""
    return [x % m for x in lst]


# ============================================================
# Normalizações
# ============================================================

def minmax_normalize(lst: List[float]) -> List[float]:
    """Normalização Min-Max."""
    min_v, max_v = min(lst), max(lst)
    return [(x - min_v) / (max_v - min_v) if max_v != min_v else 0 for x in lst]

def zscore_normalize(lst: List[float]) -> List[float]:
    """Normalização Z-Score."""
    mean = np.mean(lst)
    std = np.std(lst)
    return [(x - mean) / std if std != 0 else 0 for x in lst]
