# lib/funcoes_analiticas/analise_padroes.py
import numpy as np
from itertools import combinations, permutations
from collections import Counter
import networkx as nx
from typing import List, Dict, Tuple

def sum_of_pairs(lst: list) -> list:
    """Calcula a soma de todas as combinações de pares."""
    return [sum(c) for c in combinations(lst, 2)]

def sum_of_triples(lst: list) -> list:
    """Calcula a soma de todas as combinações de trios."""
    return [sum(c) for c in combinations(lst, 3)]

def diff_of_pairs(lst: list) -> list:
    """Calcula a diferença absoluta de todos os pares."""
    return [abs(c[0] - c[1]) for c in combinations(lst, 2)]

def count_pair_sums_equal(lst: list, value: int) -> int:
    """Conta os pares cuja soma é igual a um valor."""
    return sum(1 for c in combinations(lst, 2) if sum(c) == value)

def score_even_odd(lst: list) -> float:
    """Pontua a lista com base na paridade de seus elementos."""
    return sum([1 if x % 2 == 0 else 0.5 for x in lst])

def score_prime(lst: list) -> float:
    """Pontua a lista com base na presença de números primos."""
    def is_prime(x: int) -> bool:
        if x < 2: return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0: return False
        return True
    return sum([2 if is_prime(x) else 0 for x in lst])

def score_pairs_sum_mod(lst: list, k: int) -> int:
    """Pontua a lista com base na soma dos pares módulo k."""
    return sum(1 for c in combinations(lst, 2) if sum(c) % k == 0)

def score_cumulative_diff(lst: list) -> float:
    """Pontua a lista com base na soma das diferenças absolutas consecutivas."""
    return sum(abs(lst[i + 1] - lst[i]) for i in range(len(lst) - 1))

def most_frequent_pairs(lst: list) -> List[Tuple[Tuple, int]]:
    """Encontra os pares mais frequentes na lista."""
    pairs = [tuple(sorted(c)) for c in combinations(lst, 2)]
    return Counter(pairs).most_common()

def cluster_by_diff(lst: list, max_diff: int = 2) -> list:
    """Agrupa números que estão próximos uns dos outros."""
    clusters = []
    sorted_lst = sorted(lst)
    if not sorted_lst: return []
    cluster = [sorted_lst[0]]
    for x in sorted_lst[1:]:
        if x - cluster[-1] <= max_diff:
            cluster.append(x)
        else:
            clusters.append(cluster)
            cluster = [x]
    clusters.append(cluster)
    return clusters
