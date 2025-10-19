# lib/funcoes_analiticas/teoria_catastrofe.py
import numpy as np
from typing import List, Dict
from scipy import optimize

def catastrophe_theory_analyzer(seq: List[float]) -> Dict:
    """Aplica teoria das catástrofes para detectar pontos de virada brusca."""
    if len(seq) < 30:
        return {}
    
    # Calcula derivadas de alta ordem
    first_deriv = np.gradient(seq)
    second_deriv = np.gradient(first_deriv)
    
    # Procura por pontos de inflexão catastróficos
    catastrophe_points = []
    for i in range(2, len(second_deriv)-2):
        # Mudança brusca na segunda derivada
        if (abs(second_deriv[i]) > 3 * np.std(second_deriv) and
            np.sign(second_deriv[i]) != np.sign(second_deriv[i-1])):
            
            catastrophe_points.append({
                'position': i,
                'value': seq[i],
                'first_derivative': first_deriv[i],
                'second_derivative': second_deriv[i],
                'catastrophe_strength': abs(second_deriv[i]) / (np.std(second_deriv) + 1e-10)
            })
    
    # Classifica tipos de catástrofe
    catastrophe_types = {}
    for point in catastrophe_points:
        if point['first_derivative'] > 0 and point['second_derivative'] > 0:
            cat_type = "fold_positive"
        elif point['first_derivative'] < 0 and point['second_derivative'] < 0:
            cat_type = "fold_negative"
        else:
            cat_type = "cusp"
        
        catastrophe_types[cat_type] = catastrophe_types.get(cat_type, 0) + 1
    
    return {
        'catastrophe_points': catastrophe_points,
        'catastrophe_frequency': len(catastrophe_points) / len(seq),
        'catastrophe_types': catastrophe_types,
        'system_volatility': np.std(second_deriv) / (np.std(seq) + 1e-10)
    }

def tipping_point_early_warning(seq: List[float]) -> Dict:
    """Sistema de alerta antecipado para pontos de virada."""
    if len(seq) < 100:
        return {'warning_level': 'insufficient_data'}
    
    warning_signals = {}
    
    # 1. Aumento na autocorrelação (desaceleração crítica)
    autocorrs = []
    window_size = 20
    for i in range(len(seq) - window_size):
        window = seq[i:i+window_size]
        if np.std(window) > 0:
            autocorr = np.corrcoef(window[:-1], window[1:])[0,1]
            autocorrs.append(autocorr if not np.isnan(autocorr) else 0)
    
    autocorr_trend = np.polyfit(range(len(autocorrs)), autocorrs, 1)[0]
    warning_signals['autocorrelation_increase'] = autocorr_trend > 0.01
    
    # 2. Aumento na variância
    rolling_var = [np.var(seq[i:i+window_size]) for i in range(len(seq) - window_size)]
    var_trend = np.polyfit(range(len(rolling_var)), rolling_var, 1)[0]
    warning_signals['variance_increase'] = var_trend > 0
    
    # 3. Mudança no espectro de potência
    early_spectrum = np.abs(np.fft.fft(seq[:len(seq)//2]))**2
    late_spectrum = np.abs(np.fft.fft(seq[len(seq)//2:]))**2
    
    # Compara distribuição de energia em baixas frequências
    early_low_freq = np.mean(early_spectrum[:len(early_spectrum)//10])
    late_low_freq = np.mean(late_spectrum[:len(late_spectrum)//10])
    warning_signals['spectral_shift'] = late_low_freq > early_low_freq * 1.5
    
    # Nível de alerta consolidado
    warning_count = sum(warning_signals.values())
    if warning_count >= 2:
        warning_level = "HIGH"
    elif warning_count == 1:
        warning_level = "MEDIUM"
    else:
        warning_level = "LOW"
    
    return {
        'warning_signals': warning_signals,
        'warning_level': warning_level,
        'composite_risk_score': warning_count / len(warning_signals)
    }
