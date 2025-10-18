# lib/funcoes_analiticas/analise_combinatoria_avancada.py
import numpy as np
from typing import List, Dict
from itertools import combinations
from collections import Counter

def combinatorial_pattern_density(seq: List[int]) -> Dict:
    """Calcula densidade de padrões combinatórios em subconjuntos."""
    if len(seq) < 3:
        return {}
    
    patterns = {}
    
    # Padrões em pares
    pairs = list(combinations(seq, 2))
    pair_sums = [sum(pair) for pair in pairs]
    pair_products = [pair[0] * pair[1] for pair in pairs]
    
    patterns['pair_patterns'] = {
        'sum_variance': np.var(pair_sums),
        'product_variance': np.var(pair_products),
        'common_sum': Counter(pair_sums).most_common(1)[0] if pair_sums else (0, 0),
        'common_product': Counter(pair_products).most_common(1)[0] if pair_products else (0, 0)
    }
    
    # Padrões em trios
    if len(seq) >= 3:
        triples = list(combinations(seq, 3))
        triple_sums = [sum(triple) for triple in triples]
        triple_products = [triple[0] * triple[1] * triple[2] for triple in triples]
        
        patterns['triple_patterns'] = {
            'sum_variance': np.var(triple_sums),
            'product_variance': np.var(triple_products)
        }
    
    return patterns

def sequence_complexity_measure(seq: List[float]) -> Dict:
    """Medidas de complexidade baseadas em compressão e informação."""
    if not seq:
        return {}
    
    # Entropia aproximada
    def approximate_entropy(data, m=2, r=None):
        if r is None:
            r = 0.2 * np.std(data)
        
        def _maxdist(x_i, x_j):
            return max([abs(ua - va) for ua, va in zip(x_i, x_j)])
        
        def _phi(m):
            n = len(data)
            x = [[data[j] for j in range(i, i + m)] for i in range(n - m + 1)]
            C = [len([1 for x_j in x if _maxdist(x_i, x_j) <= r]) / (n - m + 1.0) for x_i in x]
            return (n - m + 1.0)**(-1) * sum(np.log(C))
        
        return _phi(m) - _phi(m + 1)
    
    # Complexidade de Lempel-Ziv (aproximada)
    def lempel_ziv_complexity(binary_seq):
        i, n, c = 0, 1, 1
        while i + n <= len(binary_seq):
            if binary_seq[i:i+n] in binary_seq[:i+n-1]:
                n += 1
            else:
                c += 1
                i += n
                n = 1
        return c
    
    # Binarização da sequência
    median_val = np.median(seq)
    binary_seq = [1 if x > median_val else 0 for x in seq]
    
    return {
        'approximate_entropy': approximate_entropy(seq),
        'lempel_ziv_complexity': lempel_ziv_complexity(binary_seq),
        'normalized_complexity': lempel_ziv_complexity(binary_seq) / len(seq)
    }
