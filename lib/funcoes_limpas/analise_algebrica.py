# lib/funcoes_analiticas/analise_algebrica.py
import numpy as np
from typing import List, Optional
from scipy.optimize import curve_fit

def polynomial_pattern_fitter(seq: List[float], max_degree: int = 5) -> Dict:
    """Encontra o melhor polinômio que se ajusta à sequência."""
    x = np.arange(len(seq))
    y = np.array(seq)
    
    best_fit = {}
    for degree in range(1, min(max_degree + 1, len(seq))):
        try:
            coeffs = np.polyfit(x, y, degree)
            predicted = np.polyval(coeffs, x)
            r_squared = 1 - np.sum((y - predicted)**2) / np.sum((y - np.mean(y))**2)
            
            if not best_fit or r_squared > best_fit.get('r_squared', -1):
                best_fit = {
                    'degree': degree,
                    'coefficients': coeffs.tolist(),
                    'r_squared': r_squared,
                    'mse': np.mean((y - predicted)**2)
                }
        except:
            continue
    
    return best_fit

def exponential_pattern_detector(seq: List[float]) -> Dict:
    """Detecta padrões exponenciais e logarítmicos."""
    if len(seq) < 3 or any(x <= 0 for x in seq):
        return {}
    
    x = np.arange(len(seq))
    y = np.array(seq)
    
    patterns = {}
    
    # Padrão exponencial: y = a * exp(b * x)
    try:
        def exp_func(x, a, b):
            return a * np.exp(b * x)
        
        popt, pcov = curve_fit(exp_func, x, y, p0=[y[0], 0.1])
        predicted = exp_func(x, *popt)
        r_squared = 1 - np.sum((y - predicted)**2) / np.sum((y - np.mean(y))**2)
        patterns['exponential'] = {
            'parameters': popt.tolist(),
            'r_squared': r_squared
        }
    except:
        pass
    
    # Padrão logarítmico: y = a * log(b * x + c)
    try:
        def log_func(x, a, b, c):
            return a * np.log(b * x + c)
        
        popt, pcov = curve_fit(log_func, x, y, p0=[y[0], 1, 1])
        predicted = log_func(x, *popt)
        r_squared = 1 - np.sum((y - predicted)**2) / np.sum((y - np.mean(y))**2)
        patterns['logarithmic'] = {
            'parameters': popt.tolist(),
            'r_squared': r_squared
        }
    except:
        pass
    
    return patterns
