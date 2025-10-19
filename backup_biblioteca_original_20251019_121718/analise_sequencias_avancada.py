# lib/funcoes_analiticas/analise_sequencias_avancada.py
import numpy as np
from typing import List, Tuple, Dict
from scipy import stats
import sympy as sp

def sequence_autocorrelation_pattern(seq: List[float], max_lag: int = 10) -> Dict:
    """Padrão de autocorrelação multi-lag para detectar periodicidades complexas."""
    patterns = {}
    for lag in range(1, min(max_lag, len(seq)//2)):
        if len(seq) > lag:
            corr = np.corrcoef(seq[:-lag], seq[lag:])[0,1]
            patterns[f"lag_{lag}"] = corr if not np.isnan(corr) else 0
    return patterns

def number_theory_pattern_detector(seq: List[int]) -> Dict:
    """Detecta padrões baseados em teoria dos números."""
    primes = [x for x in seq if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5)+1))]
    evens = [x for x in seq if x % 2 == 0]
    squares = [x for x in seq if int(x**0.5)**2 == x]
    cubes = [x for x in seq if round(x**(1/3))**3 == x]
    
    return {
        "prime_ratio": len(primes)/len(seq) if seq else 0,
        "even_odd_ratio": len(evens)/len(seq) if seq else 0,
        "perfect_squares": len(squares)/len(seq) if seq else 0,
        "perfect_cubes": len(cubes)/len(seq) if seq else 0,
        "modular_patterns": {f"mod_{i}": len([x for x in seq if x % 5 == i])/len(seq) for i in range(5)}
    }

def recursive_sequence_analyzer(seq: List[float]) -> Dict:
    """Analisa relações recursivas na sequência."""
    if len(seq) < 3:
        return {}
    
    # Tenta encontrar relações lineares: a_n = p*a_{n-1} + q*a_{n-2}
    X = np.column_stack([seq[1:-1], seq[:-2]])
    y = seq[2:]
    
    try:
        coeffs, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        predicted = X @ coeffs
        mse = np.mean((y - predicted)**2)
        
        return {
            "recursive_coeffs": coeffs.tolist(),
            "recursive_mse": mse,
            "is_linear_recursive": mse < 0.1 * np.var(seq)
        }
    except:
        return {}
