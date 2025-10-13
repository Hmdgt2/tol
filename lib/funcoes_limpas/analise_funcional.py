# lib/funcoes_analiticas/analise_funcional.py
import numpy as np
from typing import List, Callable
from scipy import linalg

def sobolev_norm(f: Callable[[float], float], 
                domain: List[float], 
                order: int = 1, 
                p: int = 2) -> float:
    """Norma de Sobolev W^{k,p} aproximada."""
    a, b = domain
    
    def derivative_approx(x, k):
        if k == 0:
            return f(x)
        # Diferenças finitas para derivadas
        h = 1e-6
        if k == 1:
            return (f(x + h) - f(x - h)) / (2 * h)
        elif k == 2:
            return (f(x + h) - 2 * f(x) + f(x - h)) / (h ** 2)
        else:
            return 0.0
    
    # Integrar |f^{(k)}(x)|^p
    integral = 0.0
    x_vals = np.linspace(a, b, 1000)
    for x in x_vals:
        deriv_sum = 0.0
        for k in range(order + 1):
            deriv_sum += abs(derivative_approx(x, k)) ** 2
        integral += deriv_sum ** (p / 2)
    
    return (integral * (b - a) / len(x_vals)) ** (1 / p)

def operator_norm_approx(operator: Callable, 
                        basis: List[Callable], 
                        domain: List[float]) -> float:
    """Norma de operador aproximada."""
    # Avaliar operador na base
    outputs = []
    for func in basis:
        try:
            output_func = operator(func)
            # Calcular norma L2 da saída
            norm = np.sqrt(integrate.quad(lambda x: output_func(x)**2, domain[0], domain[1])[0])
            outputs.append(norm)
        except:
            outputs.append(0.0)
    
    return max(outputs) if outputs else 0.0

def spectral_radius_approx(operator: Callable, 
                         iterations: int = 10) -> float:
    """Raio espectral aproximado de um operador."""
    # Método de potência simplificado
    test_func = lambda x: np.sin(x)  # Função teste
    
    current = test_func
    for i in range(iterations):
        try:
            current = operator(current)
            # Normalizar
            norm = np.sqrt(integrate.quad(lambda x: current(x)**2, 0, 2*np.pi)[0])
            if norm > 0:
                current = lambda x: current(x) / norm
        except:
            break
    
    # Último fator de escala como aproximação do raio espectral
    try:
        scaled = operator(current)
        original_norm = np.sqrt(integrate.quad(lambda x: current(x)**2, 0, 2*np.pi)[0])
        scaled_norm = np.sqrt(integrate.quad(lambda x: scaled(x)**2, 0, 2*np.pi)[0])
        return scaled_norm / original_norm if original_norm > 0 else 0.0
    except:
        return 0.0
