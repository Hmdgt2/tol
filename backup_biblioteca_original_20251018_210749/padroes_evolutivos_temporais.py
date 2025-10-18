# lib/funcoes_analiticas/padroes_evolutivos_temporais.py
import numpy as np
from typing import List, Dict, Tuple
from scipy import optimize, integrate

def evolutionary_fractal_dimension(seq: List[float], window_sizes: List[int] = [10, 20, 50]) -> Dict:
    """Dimensão fractal evolutiva em múltiplas escalas temporais."""
    results = {}
    
    for window in window_sizes:
        if len(seq) >= window * 2:
            # Divide em segmentos temporais
            segments = [seq[i:i+window] for i in range(0, len(seq)-window+1, window//2)]
            
            fractal_dims = []
            for segment in segments:
                if len(segment) > 1:
                    # Método de Higuchi adaptado
                    L = []
                    for k in range(1, min(10, len(segment)//2)):
                        Lk = 0
                        for m in range(k):
                            idx = np.arange(m, len(segment), k)
                            if len(idx) > 1:
                                Lkm = np.sum(np.abs(np.diff([segment[i] for i in idx])))
                                Lkm = Lkm * (len(segment) - 1) / (len(idx) * k)
                                Lk += Lkm
                        L.append(np.log(Lk / k))
                    
                    if len(L) > 1:
                        x = np.log(np.arange(1, len(L)+1))
                        slope = np.polyfit(x, L, 1)[0]
                        fractal_dims.append(slope)
            
            results[f'fractal_window_{window}'] = {
                'mean': np.mean(fractal_dims) if fractal_dims else 0,
                'trend': np.polyfit(range(len(fractal_dims)), fractal_dims, 1)[0] if len(fractal_dims) > 1 else 0
            }
    
    return results

def temporal_pattern_entropy(seq: List[float], time_scales: List[int] = [1, 7, 30, 365]) -> Dict:
    """Entropia de padrões em diferentes escalas temporais (dias, semanas, meses, anos)."""
    entropy_results = {}
    
    for scale in time_scales:
        if len(seq) >= scale * 3:
            # Agrega por escala temporal
            aggregated = []
            for i in range(0, len(seq) - scale + 1, scale):
                segment = seq[i:i + scale]
                aggregated.append({
                    'mean': np.mean(segment),
                    'std': np.std(segment),
                    'range': max(segment) - min(segment)
                })
            
            # Calcula entropia dos padrões agregados
            patterns = []
            for i in range(len(aggregated) - 1):
                pattern = (
                    'up' if aggregated[i+1]['mean'] > aggregated[i]['mean'] else 'down',
                    'volatile' if aggregated[i+1]['std'] > aggregated[i]['std'] else 'stable'
                )
                patterns.append(pattern)
            
            # Entropia de Shannon dos padrões
            pattern_counts = {}
            for pattern in patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            total = len(patterns)
            entropy = -sum((count/total) * np.log(count/total) 
                          for count in pattern_counts.values() if count > 0)
            
            entropy_results[f'temporal_entropy_scale_{scale}'] = entropy
    
    return entropy_results
