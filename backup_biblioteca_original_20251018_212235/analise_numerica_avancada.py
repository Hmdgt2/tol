# lib/funcoes_analiticas/analise_numerica_avancada.py
import numpy as np
from typing import List, Callable
from scipy import integrate, special
import mpmath

# ============================================================
# Transformadas Especiais
# ============================================================

def mellin_transform(f: Callable, s: complex) -> complex:
    """Transformada de Mellin de uma função."""
    result, _ = integrate.quad(lambda x: f(x) * x**(s-1), 0, np.inf)
    return result

def hankel_transform(f: Callable, k: float, order: int = 0) -> float:
    """Transformada de Hankel de ordem n."""
    integrand = lambda r: f(r) * special.jv(order, k * r) * r
    result, _ = integrate.quad(integrand, 0, np.inf)
    return result

def fourier_bessel_transform(seq: List[float]) -> List[float]:
    """Transformada Fourier-Bessel para sequências."""
    n = len(seq)
    result = []
    for k in range(1, n + 1):
        total = sum(seq[j] * special.j0(np.pi * j * k / n) for j in range(n))
        result.append(total)
    return result

# ============================================================
# Funções Hipergeométricas
# ============================================================

def hypergeometric_1f1(a: float, b: float, z: float) -> float:
    """Função hipergeométrica confluente ₁F₁(a;b;z)."""
    return special.hyp1f1(a, b, z)

def hypergeometric_2f1(a: float, b: float, c: float, z: float) -> float:
    """Função hipergeométrica Gaussiana ₂F₁(a,b;c;z)."""
    return special.hyp2f1(a, b, c, z)

def meijer_g_transform(params: List[float], z: float) -> float:
    """Função G de Meijer simplificada."""
    try:
        return float(mpmath.meijerg(params, z))
    except:
        return special.gamma(z)

# ============================================================
# Integrais Especiais
# ============================================================

def fresnel_integral(x: float) -> tuple:
    """Integrais de Fresnel C(x) e S(x)."""
    return special.fresnel(x)

def exponential_integral_e1(z: float) -> float:
    """Integral exponencial E₁(z)."""
    return special.exp1(z)

def sine_integral(x: float) -> float:
    """Integral seno Si(x)."""
    return special.sici(x)[0]

def cosine_integral(x: float) -> float:
    """Integral cosseno Ci(x)."""
    return special.sici(x)[1]

# ============================================================
# Funções de Mathieu
# ============================================================

def mathieu_characteristic(a: float, q: float, n: int) -> float:
    """Coeficiente característico de Mathieu."""
    return special.mathieu_a(n, q) if a > 0 else special.mathieu_b(n, q)

def mathieu_function_even(t: float, a: float, q: float) -> float:
    """Função de Mathieu par."""
    return special.mathieu_cem(1, q, t)[0]

# ============================================================
# Sistemas Dinâmicos
# ============================================================

def lyapunov_exponent(seq: List[float]) -> float:
    """Expoente de Lyapunov para sequências."""
    if len(seq) < 2:
        return 0.0
    differences = [abs(seq[i+1] - seq[i]) for i in range(len(seq)-1)]
    return np.mean(np.log(np.array(differences) + 1e-10))

def takens_embedding(seq: List[float], dimension: int = 3, delay: int = 1) -> List[List[float]]:
    """Embedding de Takens para reconstrução de espaço de estados."""
    embedded = []
    for i in range(len(seq) - (dimension-1)*delay):
        point = [seq[i + j*delay] for j in range(dimension)]
        embedded.append(point)
    return embedded
