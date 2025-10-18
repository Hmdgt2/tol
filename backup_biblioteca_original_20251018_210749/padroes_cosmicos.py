# lib/funcoes_analiticas/padroes_cosmicos.py
import numpy as np
from typing import List, Dict
from scipy import special

def astronomical_cycle_detector(seq: List[float], max_period: int = 1000) -> Dict:
    """Detecta ciclos de longo prazo similares a ciclos astronômicos."""
    n = len(seq)
    if n < 50:
        return {}
    
    # Análise espectral para períodos longos
    frequencies = np.fft.fft(seq)
    power_spectrum = np.abs(frequencies)**2
    
    # Foca em baixas frequências (períodos longos)
    low_freq_indices = range(1, min(max_period, n//2))
    significant_periods = []
    
    for idx in low_freq_indices:
        period = n / idx
        power = power_spectrum[idx]
        
        # Testa significância estatística
        if power > np.mean(power_spectrum) + 2 * np.std(power_spectrum):
            significant_periods.append({
                'period': period,
                'power': power,
                'amplitude': np.abs(frequencies[idx]) / n
            })
    
    # Ordena por poder e retorna os mais significativos
    significant_periods.sort(key=lambda x: x['power'], reverse=True)
    
    return {
        'detected_periods': significant_periods[:5],  # Top 5 períodos
        'dominant_period': significant_periods[0]['period'] if significant_periods else None,
        'spectral_richness': len(significant_periods) / len(low_freq_indices)
    }

def galactic_pattern_analyzer(seq: List[float]) -> Dict:
    """Análise de padrões em escala galáctica - padrões superpostos."""
    if len(seq) < 200:
        return {}
    
    # Decomposição em múltiplas escalas
    scales = [10, 50, 100, 200]  # Diferentes escalas temporais
    decompositions = {}
    
    for scale in scales:
        if len(seq) >= scale * 2:
            # Filtro passa-baixa para esta escala
            smoothed = np.convolve(seq, np.ones(scale)/scale, mode='valid')
            residual = seq[scale-1:] - smoothed
            
            decompositions[f'scale_{scale}'] = {
                'trend': smoothed.tolist(),
                'residual': residual.tolist(),
                'residual_energy': np.sum(residual**2),
                'trend_stability': np.std(np.diff(smoothed)) if len(smoothed) > 1 else 0
            }
    
    # Análise de coerência entre escalas
    coherence_analysis = {}
    scale_keys = list(decompositions.keys())
    for i in range(len(scale_keys)):
        for j in range(i+1, len(scale_keys)):
            scale1 = scale_keys[i]
            scale2 = scale_keys[j]
            
            # Correlação entre tendências de diferentes escalas
            trend1 = decompositions[scale1]['trend']
            trend2 = decompositions[scale2]['trend']
            
            min_len = min(len(trend1), len(trend2))
            if min_len > 10:
                correlation = np.corrcoef(trend1[:min_len], trend2[:min_len])[0,1]
                if not np.isnan(correlation):
                    coherence_analysis[f'{scale1}_vs_{scale2}'] = correlation
    
    return {
        'multi_scale_decomposition': decompositions,
        'inter_scale_coherence': coherence_analysis,
        'hierarchical_complexity': len([c for c in coherence_analysis.values() if abs(c) < 0.3]) / len(coherence_analysis) if coherence_analysis else 0
    }
