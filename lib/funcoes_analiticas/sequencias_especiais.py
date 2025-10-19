# lib/funcoes_analiticas/sequencias_especiais.py
import numpy as np
from typing import List, Tuple, Dict
from math import gcd, isqrt
import itertools

# ============================================================
# Detecção de Progressões
# ============================================================

def detect_arithmetic_progression(seq: List[int]) -> Dict:
    """Detecta Progressão Aritmética e retorna razão e confiança."""
    if len(seq) < 3:
        return {"is_ap": False, "reason": "Sequência muito curta"}
    
    differences = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    constant_diff = len(set(differences)) == 1
    
    return {
        "is_ap": constant_diff,
        "common_difference": differences[0] if constant_diff else None,
        "variance": np.var(differences) if not constant_diff else 0.0,
        "confidence": 1.0 if constant_diff else max(0, 1 - np.var(differences)/100)
    }

def detect_geometric_progression(seq: List[float]) -> Dict:
    """Detecta Progressão Geométrica e retorna razão e confiança."""
    if len(seq) < 3 or any(x == 0 for x in seq):
        return {"is_gp": False, "reason": "Sequência inválida ou muito curta"}
    
    ratios = [seq[i+1] / seq[i] for i in range(len(seq)-1)]
    constant_ratio = len(set(round(r, 10) for r in ratios)) == 1
    
    return {
        "is_gp": constant_ratio,
        "common_ratio": ratios[0] if constant_ratio else None,
        "ratio_variance": np.var(ratios) if not constant_ratio else 0.0,
        "confidence": 1.0 if constant_ratio else max(0, 1 - np.var(ratios))
    }

def continued_fraction_analysis(n: int, depth: int = 10) -> Dict:
    """Análise de frações contínuas de um número."""
    if n <= 0:
        return {"error": "Número deve ser positivo"}
    
    def get_continued_fraction(x, max_depth):
        result = []
        remainder = x
        for _ in range(max_depth):
            integer_part = int(remainder)
            result.append(integer_part)
            remainder = remainder - integer_part
            if abs(remainder) < 1e-10:
                break
            remainder = 1 / remainder if remainder != 0 else 0
        return result
    
    cf = get_continued_fraction(n, depth)
    
    return {
        "continued_fraction": cf,
        "period_length": len(cf),
        "convergents": len(cf),
        "golden_ratio_similarity": abs(cf[0] - 1.618) if cf else 0
    }

# ============================================================
# Sequências Clássicas
# ============================================================

def look_and_say_analysis(seq: List[int]) -> Dict:
    """Análise de sequências 'look-and-say'."""
    if not seq:
        return {"error": "Sequência vazia"}
    
    def look_and_say_transform(sequence):
        result = []
        i = 0
        while i < len(sequence):
            count = 1
            while i + count < len(sequence) and sequence[i + count] == sequence[i]:
                count += 1
            result.extend([count, sequence[i]])
            i += count
        return result
    
    transformed = look_and_say_transform(seq)
    growth_rate = len(transformed) / len(seq) if seq else 0
    
    return {
        "transformed_sequence": transformed,
        "growth_rate": growth_rate,
        "compression_ratio": len(seq) / len(transformed) if transformed else 0,
        "digit_patterns": len(set(seq)) / len(seq) if seq else 0
    }

def fibonacci_like_analysis(seq: List[int]) -> Dict:
    """Verifica se sequência segue padrão Fibonacci-like."""
    if len(seq) < 4:
        return {"is_fibonacci_like": False, "reason": "Sequência muito curta"}
    
    # Verifica relação F(n) = a*F(n-1) + b*F(n-2)
    errors = []
    for i in range(2, len(seq)-1):
        if seq[i-2] != 0:
            ratio = seq[i] / seq[i-2]
            predicted = ratio * seq[i-1]
            errors.append(abs(predicted - seq[i+1]))
    
    avg_error = np.mean(errors) if errors else float('inf')
    is_fib_like = avg_error < 0.1 * np.mean([abs(x) for x in seq]) if seq else False
    
    return {
        "is_fibonacci_like": is_fib_like,
        "average_error": avg_error,
        "confidence": max(0, 1 - avg_error / (np.mean([abs(x) for x in seq]) if seq else 1))
    }
