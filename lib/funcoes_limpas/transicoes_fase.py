# lib/funcoes_analiticas/transicoes_fase.py
import numpy as np
from typing import List, Dict
from scipy.signal import find_peaks

def phase_transition_detector(seq: List[float], sensitivity: float = 2.0) -> Dict:
    """Detecta transições de fase em séries temporais longas."""
    if len(seq) < 50:
        return {}
    
    # Análise de mudanças de regime
    window_size = max(10, len(seq) // 20)
    regimes = []
    
    for i in range(0, len(seq) - window_size + 1, window_size // 2):
        window = seq[i:i + window_size]
        regimes.append({
            'mean': np.mean(window),
            'std': np.std(window),
            'start': i,
            'end': i + window_size
        })
    
    # Detecta mudanças significativas
    transitions = []
    for i in range(1, len(regimes)):
        prev = regimes[i-1]
        curr = regimes[i]
        
        mean_change = abs(curr['mean'] - prev['mean']) / (prev['std'] + 1e-10)
        std_change = abs(curr['std'] - prev['std']) / (prev['std'] + 1e-10)
        
        if mean_change > sensitivity or std_change > sensitivity:
            transitions.append({
                'position': curr['start'],
                'mean_change': mean_change,
                'std_change': std_change,
                'type': 'volatility' if std_change > mean_change else 'level'
            })
    
    return {
        'transition_count': len(transitions),
        'transitions': transitions,
        'regime_stability': len(transitions) / (len(regimes) - 1) if len(regimes) > 1 else 0
    }

def critical_slowdown_analysis(seq: List[float]) -> Dict:
    """Análise de desaceleração crítica antes de transições de fase."""
    if len(seq) < 100:
        return {}
    
    # Calcula autocorrelação em janelas deslizantes
    window_size = len(seq) // 10
    autocorrs = []
    variances = []
    
    for i in range(0, len(seq) - window_size + 1, window_size // 5):
        window = seq[i:i + window_size]
        if len(window) > 1:
            # Autocorrelação no lag 1
            autocorr = np.corrcoef(window[:-1], window[1:])[0,1] if np.std(window) > 0 else 0
            autocorrs.append(autocorr if not np.isnan(autocorr) else 0)
            variances.append(np.var(window))
    
    # Procura por aumento na autocorrelação (sinal de desaceleração crítica)
    critical_signals = []
    for i in range(5, len(autocorrs)):
        recent_autocorr = np.mean(autocorrs[max(0, i-5):i])
        if recent_autocorr > np.mean(autocorrs[:i]) + 2 * np.std(autocorrs[:i]):
            critical_signals.append({
                'position': i * (window_size // 5),
                'autocorrelation': recent_autocorr,
                'variance': variances[i]
            })
    
    return {
        'critical_slowdown_detected': len(critical_signals) > 0,
        'slowdown_signals': critical_signals,
        'autocorrelation_trend': np.polyfit(range(len(autocorrs)), autocorrs, 1)[0] if autocorrs else 0
    }
