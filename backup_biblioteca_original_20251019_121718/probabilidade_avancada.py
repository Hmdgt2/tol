# lib/funcoes_analiticas/probabilidade_avancada.py
import numpy as np
from typing import List, Callable
from scipy import stats, integrate

def levy_process_increments(times: List[float], alpha: float = 1.5) -> List[float]:
    """Incrementos de processo de Lévy estável."""
    increments = []
    for i in range(1, len(times)):
        dt = times[i] - times[i-1]
        # Distribuição estável simétrica
        increment = dt ** (1/alpha) * np.random.standard_cauchy()
        increments.append(increment)
    return increments

def martingale_property(process: List[float]) -> bool:
    """Verifica propriedade de martingale."""
    if len(process) < 2:
        return True
    
    # Esperança condicional ≈ média dos incrementos
    increments = [process[i] - process[i-1] for i in range(1, len(process))]
    return abs(np.mean(increments)) < 0.1  # Threshold

def brownian_bridge_probability(brownian_path: List[float], 
                               target: float, 
                               tolerance: float = 0.1) -> float:
    """Probabilidade de ponte browniana atingir valor."""
    if not brownian_path:
        return 0.0
    
    start, end = brownian_path[0], brownian_path[-1]
    # Probabilidade usando fórmula de ponte browniana
    t = len(brownian_path)
    variance = t / 4  # Variação aproximada
    prob = np.exp(-(target - (start + end)/2)**2 / (2 * variance))
    return min(1.0, prob)

def stochastic_integral_approx(integrand: Callable[[float], float], 
                             brownian_path: List[float]) -> float:
    """Integral estocástica aproximada (Itô)."""
    if len(brownian_path) < 2:
        return 0.0
    
    integral = 0.0
    times = list(range(len(brownian_path)))
    
    for i in range(len(brownian_path) - 1):
        t = times[i]
        dB = brownian_path[i+1] - brownian_path[i]
        integral += integrand(t) * dB
    
    return integral

def girsanov_theorem_density(brownian_path: List[float], 
                            drift: Callable[[float], float]) -> float:
    """Densidade de Girsanov para mudança de medida."""
    if len(brownian_path) < 2:
        return 1.0
    
    times = list(range(len(brownian_path)))
    exponent = 0.0
    quadratic_var = 0.0
    
    for i in range(len(brownian_path) - 1):
        t = times[i]
        dB = brownian_path[i+1] - brownian_path[i]
        dt = times[i+1] - times[i]
        
        exponent += drift(t) * dB
        quadratic_var += drift(t)**2 * dt
    
    density = np.exp(exponent - 0.5 * quadratic_var)
    return density
