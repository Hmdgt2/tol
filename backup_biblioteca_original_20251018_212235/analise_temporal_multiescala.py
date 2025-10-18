# lib/funcoes_analiticas/analise_temporal_multiescala.py
import numpy as np
from typing import List, Dict
from scipy import signal

def multi_scale_entropy_analysis(seq: List[float], max_scale: int = 5) -> Dict:
    """Análise de entropia em múltiplas escalas temporais."""
    entropies = {}
    
    for scale in range(1, min(max_scale + 1, len(seq) // 2)):
        # Coarse-graining da série temporal
        coarse_grained = []
        for i in range(0, len(seq) - scale + 1, scale):
            coarse_grained.append(np.mean(seq[i:i + scale]))
        
        if len(coarse_grained) >= 10:  # Mínimo para cálculo de entropia
            # Entropia aproximada na escala
            def _phi(data, m):
                n = len(data)
                patterns = []
                for i in range(n - m + 1):
                    patterns.append(tuple(data[i:i + m]))
                
                counts = {}
                for pattern in patterns:
                    counts[pattern] = counts.get(pattern, 0) + 1
                
                probabilities = [count / (n - m + 1) for count in counts.values()]
                return -sum(p * np.log(p) for p in probabilities if p > 0)
            
            entropy = _phi(coarse_grained, 2) - _phi(coarse_grained, 3)
            entropies[f'scale_{scale}'] = entropy
    
    return entropies

def wavelet_multiresolution_analysis(seq: List[float]) -> Dict:
    """Análise de multi-resolução usando wavelets."""
    if len(seq) < 8:
        return {}
    
    # Coeficientes de wavelet (aproximação e detalhe)
    coeffs = {}
    
    # Simples decomposição em alta e baixa frequência
    half_len = len(seq) // 2
    low_freq = [np.mean(seq[i:i+2]) for i in range(0, len(seq)-1, 2)]
    high_freq = [seq[i] - seq[i+1] for i in range(0, len(seq)-1, 2)]
    
    coeffs['approximation'] = {
        'mean': np.mean(low_freq),
        'variance': np.var(low_freq),
        'energy': np.sum(np.array(low_freq)**2)
    }
    
    coeffs['detail'] = {
        'mean': np.mean(high_freq),
        'variance': np.var(high_freq),
        'energy': np.sum(np.array(high_freq)**2)
    }
    
    # Razão de energia entre bandas
    total_energy = coeffs['approximation']['energy'] + coeffs['detail']['energy']
    if total_energy > 0:
        coeffs['energy_ratio'] = coeffs['approximation']['energy'] / total_energy
    else:
        coeffs['energy_ratio'] = 0
    
    return coeffs
