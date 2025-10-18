# lib/funcoes_analiticas/analise_astronomica.py
try:
    from astropy import units as u
    from astropy.timeseries import LombScargle
    from astropy.stats import sigma_clip, bayesian_blocks
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
from typing import List, Dict
import numpy as np

def astropy_astronomical_analysis(seq: List[float]) -> Dict:
    """Análise de séries temporais astronômicas."""
    if not ASTROPY_AVAILABLE:
        return {'astropy_analysis': 'astropy_not_available'}
    
    time = np.arange(len(seq))
    
    # Período de Lomb-Scargle (para dados irregularmente espaçados)
    ls = LombScargle(time, seq)
    frequency, power = ls.autopower()
    best_period = 1 / frequency[np.argmax(power)]
    
    # Detecção de blocos bayesianos
    try:
        edges = bayesian_blocks(seq)
        blocks = len(edges) - 1
    except:
        blocks = 0
    
    return {
        'astropy_results': {
            'lomb_scargle_period': float(best_period),
            'bayesian_blocks': blocks,
            'sigma_clipped_mean': float(sigma_clip(seq).mean())
        },
        'astronomy_tools': ['period_detection', 'bayesian_blocks', 'sigma_clipping', 'units_handling']
    }
