# lib/funcoes_analiticas/combinatoria_avancada.py
import numpy as np
from typing import List, Tuple
from scipy.special import comb, factorial
import itertools
from collections import Counter

# ============================================================
# Coeficientes Especiais
# ============================================================

def multinomial_coefficient(params: List[int]) -> int:
    """Coeficiente multinomial."""
    total = sum(params)
    result = factorial(total)
    for p in params:
        result //= factorial(p)
    return result

def catalan_number(n: int) -> int:
    """Número de Catalan C_n."""
    return comb(2 * n, n) // (n + 1)

def stirling_first(n: int, k: int) -> int:
    """Números de Stirling de primeiro tipo s(n,k)."""
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return stirling_first(n-1, k-1) - (n-1) * stirling_first(n-1, k)

def stirling_second(n: int, k: int) -> int:
    """Números de Stirling de segundo tipo S(n,k)."""
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return k * stirling_second(n-1, k) + stirling_second(n-1, k-1)

# ============================================================
# Partições Combinatórias
# ============================================================

def integer_partitions(n: int) -> List[Tuple[int]]:
    """Gera todas as partições inteiras de n."""
    result = []
    def generate_partition(remaining, max_part, current):
        if remaining == 0:
            result.append(tuple(current))
            return
        for i in range(min(max_part, remaining), 0, -1):
            generate_partition(remaining - i, i, current + [i])
    
    generate_partition(n, n, [])
    return result

def set_partitions_count(n: int, k: int) -> int:
    """Número de partições de conjunto de n elementos em k blocos."""
    return stirling_second(n, k)

def young_tableaux_count(shape: List[int]) -> int:
    """Número de tableaux de Young para uma dada forma."""
    # Implementação simplificada usando a fórmula do gancho
    total_cells = sum(shape)
    numerator = factorial(total_cells)
    denominator = 1
    
    for i, row_len in enumerate(shape):
        for j in range(row_len):
            hook_length = row_len - j
            for k in range(i + 1, len(shape)):
                if j < shape[k]:
                    hook_length += 1
            denominator *= hook_length
    
    return numerator // denominator

# ============================================================
# Permutações Especiais
# ============================================================

def derangements_count(n: int) -> int:
    """Número de desarranjos (permutações sem pontos fixos)."""
    if n == 0:
        return 1
    if n == 1:
        return 0
    return (n - 1) * (derangements_count(n - 1) + derangements_count(n - 2))

def involution_count(n: int) -> int:
    """Número de involuções (permutações que são suas próprias inversas)."""
    if n == 0:
        return 1
    if n == 1:
        return 1
    return involution_count(n - 1) + (n - 1) * involution_count(n - 2)

# ============================================================
# Grafos Combinatórios
# ============================================================

def complete_graph_edges(n: int) -> int:
    """Número de arestas em grafo completo K_n."""
    return n * (n - 1) // 2

def tree_count(n: int) -> int:
    """Número de árvores rotuladas (Fórmula de Cayley)."""
    return n ** (n - 2) if n >= 1 else 0

def bipartite_graph_count(m: int, n: int) -> int:
    """Número de grafos bipartidos completos entre conjuntos de tamanhos m e n."""
    return 2 ** (m * n)
