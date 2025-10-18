
import numpy as np
from typing import List, Tuple
from scipy import spatial, optimize
import networkx as nx


def simple_hash_function(data: List[int], mod: int=1000000007) -> int:
    'Função hash simples para lista de inteiros.'
    hash_val = 0
    prime = 31
    for num in data:
        hash_val = (((hash_val * prime) + num) % mod)
    return hash_val


def linear_congruential_generator(seed: int, n: int, a: int=1664525, c: int=1013904223, m: int=(2 ** 32)) -> List[int]:
    'Gerador congruencial linear para números pseudo-aleatórios.'
    result = []
    current = seed
    for _ in range(n):
        current = (((a * current) + c) % m)
        result.append(current)
    return result


def jaccard_similarity(text1: str, text2: str) -> float:
    'Similaridade de Jaccard entre dois textos.'
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = len((words1 & words2))
    union = len((words1 | words2))
    return ((intersection / union) if (union > 0) else 0.0)


def levenshtein_distance_ratio(s1: str, s2: str) -> float:
    'Razão de similaridade baseada na distância de Levenshtein.'
    if ((len(s1) == 0) or (len(s2) == 0)):
        return 0.0
    if (len(s1) < len(s2)):
        return levenshtein_distance_ratio(s2, s1)
    if (len(s2) == 0):
        return len(s1)
    previous_row = list(range((len(s2) + 1)))
    for (i, c1) in enumerate(s1):
        current_row = [(i + 1)]
        for (j, c2) in enumerate(s2):
            insertions = (previous_row[(j + 1)] + 1)
            deletions = (current_row[j] + 1)
            substitutions = (previous_row[j] + (c1 != c2))
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    distance = previous_row[(- 1)]
    max_len = max(len(s1), len(s2))
    return ((1 - (distance / max_len)) if (max_len > 0) else 0.0)

