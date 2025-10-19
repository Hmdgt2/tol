# lib/funcoes_analiticas/teoria_analitica_numeros.py
import numpy as np
from typing import List, Dict, Tuple
from math import gcd, isqrt
import sympy as sp

# ============================================================
# Funções L e Caracteres
# ============================================================

def l_function_analysis(s: complex, character: Dict, terms: int = 1000) -> Dict:
    """Análise de função L com caracteres de Dirichlet."""
    real_part, imag_part = s.real, s.imag
    
    def dirichlet_character(n, modulus, values):
        if gcd(n, modulus) != 1:
            return 0
        return values.get(n % modulus, 0)
    
    # Calcula série L
    l_value = 0
    convergence_data = []
    
    for n in range(1, terms + 1):
        char_val = dirichlet_character(n, character.get('modulus', 1), character.get('values', {}))
        term = char_val / (n ** s)
        l_value += term
        convergence_data.append(abs(term))
    
    # Zeros e propriedades analíticas
    critical_line_zeros = []
    if character.get('modulus') == 1:  # Função zeta de Riemann
        # Zeros triviais (simplificado)
        critical_line_zeros = [-2, -4, -6, -8, -10]  # Zeros triviais
    
    return {
        "l_function_value": l_value,
        "convergence_rate": np.mean(convergence_data[-100:]),
        "analytic_continuation": {
            "functional_equation": True,
            "critical_strip": (0, 1),
            "trivial_zeros": critical_line_zeros
        },
        "character_properties": {
            "modulus": character.get('modulus', 1),
            "primitive": character.get('primitive', True),
            "order": len(set(character.get('values', {}).values()))
        }
    }

def dirichlet_character_values(modulus: int) -> Dict:
    """Gera caracteres de Dirichlet para um dado módulo."""
    if modulus <= 1:
        return {"error": "Módulo deve ser maior que 1"}
    
    characters = {}
    
    # Caracter principal
    principal_char = {i: 1 for i in range(1, modulus) if gcd(i, modulus) == 1}
    characters['principal'] = {
        'modulus': modulus,
        'values': principal_char,
        'primitive': modulus == 1,
        'order': 1
    }
    
    # Caracteres não-principais (simplificado)
    for k in range(2, min(modulus, 6)):  # Limita para demonstração
        if gcd(k, modulus) == 1:
            char_values = {}
            for i in range(1, modulus):
                if gcd(i, modulus) == 1:
                    # Caracter real simples
                    char_values[i] = 1 if pow(i, (modulus-1)//2, modulus) == 1 else -1
            characters[f'character_{k}'] = {
                'modulus': modulus,
                'values': char_values,
                'primitive': len(char_values) == modulus - 1,
                'order': 2  # Para caracteres quadráticos
            }
    
    return {
        "modulus": modulus,
        "euler_phi": len([i for i in range(1, modulus) if gcd(i, modulus) == 1]),
        "characters": characters,
        "number_of_characters": len(characters)
    }

def modular_form_weight(seq: List[int], k: float) -> Dict:
    """Analisa propriedades de formas modulares."""
    if len(seq) < 10:
        return {"error": "Sequência muito curta para análise modular"}
    
    # Transformada modular (simplificada)
    def modular_transform(sequence, a, b, c, d):
        if c == 0:
            return sequence
        transformed = []
        for n in range(len(sequence)):
            new_val = ((c*n + d) ** k) * sequence[n] if n < len(sequence) else 0
            transformed.append(new_val)
        return transformed
    
    # Testa invariância sob transformação modular
    transformations = [
        (0, -1, 1, 0),   # S-transform
        (1, 1, 0, 1),    # T-transform
    ]
    
    invariance_scores = []
    for transform in transformations:
        a, b, c, d = transform
        transformed_seq = modular_transform(seq, a, b, c, d)
        if len(transformed_seq) == len(seq):
            correlation = np.corrcoef(seq, transformed_seq)[0,1]
            invariance_scores.append(abs(correlation))
    
    return {
        "weight": k,
        "modular_invariance_score": np.mean(invariance_scores) if invariance_scores else 0,
        "fourier_coefficients": {
            "first_10": seq[:10],
            "growth_rate": np.std(seq) / np.mean(seq) if np.mean(seq) != 0 else 0,
            "sign_pattern": [1 if x > 0 else -1 if x < 0 else 0 for x in seq[:20]]
        },
        "level_estimation": estimate_modular_level(seq),
        "cusp_form": is_cusp_form(seq)
    }

def estimate_modular_level(seq: List[int]) -> int:
    """Estima nível da forma modular (heurística simples)."""
    if not seq:
        return 1
    
    # Heurística baseada em periodicidade
    autocorrelations = []
    for lag in range(1, min(20, len(seq)//2)):
        corr = np.corrcoef(seq[:-lag], seq[lag:])[0,1] if len(seq) > lag else 0
        autocorrelations.append((lag, abs(corr)))
    
    # Encontra lags com alta correlação
    significant_lags = [lag for lag, corr in autocorrelations if corr > 0.7]
    return max(significant_lags) if significant_lags else 1

def is_cusp_form(seq: List[int]) -> bool:
    """Verifica se a sequência sugere uma forma cuspidal."""
    if not seq:
        return False
    
    # Formas cuspidais geralmente têm primeiro coeficiente zero
    return abs(seq[0] if seq else 0) < 1e-10
