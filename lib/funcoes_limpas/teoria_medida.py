# lib/funcoes_analiticas/teoria_medida.py
import numpy as np
from typing import List, Callable
from scipy import integrate

def lebesgue_integral_approx(f: Callable[[float], float], 
                           domain: List[float], 
                           measure: Callable[[float], float] = lambda x: 1.0,
                           partitions: int = 1000) -> float:
    """Integral de Lebesgue aproximada."""
    a, b = domain
    x_vals = np.linspace(a, b, partitions)
    
    # Amostrar valores da função
    y_vals = [f(x) for x in x_vals]
    unique_vals = sorted(set(y_vals))
    
    integral = 0.0
    for y in unique_vals:
        # Medida do conjunto onde f(x) ≈ y
        measure_set = 0.0
        for i, x in enumerate(x_vals):
            if abs(f(x) - y) < 1e-10:  # Simplificação
                measure_set += measure(x) * (b - a) / partitions
        integral += y * measure_set
    
    return integral

def radon_nikodym_derivative_approx(measure1: Callable, measure2: Callable, 
                                  points: List[float]) -> List[float]:
    """Derivada de Radon-Nikodym aproximada."""
    derivatives = []
    eps = 1e-8
    
    for x in points:
        # Razão das medidas em pequenos intervalos
        interval_measure1 = measure1(x + eps) - measure1(x - eps)
        interval_measure2 = measure2(x + eps) - measure2(x - eps)
        
        if abs(interval_measure2) > 1e-12:
            derivative = interval_measure1 / interval_measure2
        else:
            derivative = 0.0
        derivatives.append(derivative)
    
    return derivatives

def hausdorff_dimension_approx(points: List[List[float]], 
                             scales: List[float] = None) -> float:
    """Dimensão de Hausdorff aproximada de um conjunto."""
    if scales is None:
        scales = np.logspace(-3, 0, 20)
    
    counts = []
    for scale in scales:
        # Contar caixas necessárias
        covered = set()
        for point in points:
            box_coord = tuple(int(coord / scale) for coord in point)
            covered.add(box_coord)
        counts.append(len(covered))
    
    # Regressão linear para encontrar dimensão
    if len(counts) > 1:
        log_scales = np.log(1 / np.array(scales))
        log_counts = np.log(np.array(counts) + 1)
        slope = np.polyfit(log_scales, log_counts, 1)[0]
        return slope
    return 0.0
