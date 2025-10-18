# lib/funcoes_analiticas/analise_similaridade_avancada.py
import numpy as np
from typing import List, Callable
from scipy.spatial.distance import cdist

def dynamic_time_warping_distance(seq1: List[float], seq2: List[float]) -> float:
    """Distância de Dynamic Time Warping entre duas sequências."""
    n, m = len(seq1), len(seq2)
    dtw_matrix = np.zeros((n+1, m+1))
    
    for i in range(1, n+1):
        dtw_matrix[i, 0] = float('inf')
    for j in range(1, m+1):
        dtw_matrix[0, j] = float('inf')
    
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = abs(seq1[i-1] - seq2[j-1])
            dtw_matrix[i, j] = cost + min(dtw_matrix[i-1, j],    # Inserção
                                         dtw_matrix[i, j-1],    # Deleção
                                         dtw_matrix[i-1, j-1])  # Correspondência
    
    return dtw_matrix[n, m]

def sequence_kernel_similarity(seq1: List[float], seq2: List[float], 
                              kernel: Callable = None) -> float:
    """Similaridade baseada em kernels entre sequências."""
    if kernel is None:
        # Kernel RBF padrão
        kernel = lambda x, y: np.exp(-0.1 * np.linalg.norm(np.array(x) - np.array(y))**2)
    
    # Padding para sequências de tamanhos diferentes
    max_len = max(len(seq1), len(seq2))
    seq1_padded = np.pad(seq1, (0, max_len - len(seq1)), mode='constant')
    seq2_padded = np.pad(seq2, (0, max_len - len(seq2)), mode='constant')
    
    return kernel(seq1_padded, seq2_padded)

def pattern_cross_correlation(seq1: List[float], seq2: List[float]) -> Dict:
    """Correlação cruzada com deslocamento para detectar padrões similares."""
    corr_results = {}
    
    # Correlação cruzada
    correlation = signal.correlate(seq1, seq2, mode='full')
    lags = signal.correlation_lags(len(seq1), len(seq2), mode='full')
    
    # Encontra o lag de máxima correlação
    max_corr_idx = np.argmax(np.abs(correlation))
    max_lag = lags[max_corr_idx]
    max_correlation = correlation[max_corr_idx]
    
    corr_results['max_correlation'] = max_correlation
    corr_results['optimal_lag'] = max_lag
    corr_results['normalized_correlation'] = max_correlation / (np.std(seq1) * np.std(seq2) * len(seq1))
    
    return corr_results
