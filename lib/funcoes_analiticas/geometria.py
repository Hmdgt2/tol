# lib/funcoes_analiticas/geometria.py
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine, chebyshev, braycurtis, canberra, minkowski
from typing import List, Union

def euclidean_dist(a: list, b: list) -> float:
    """Calcula a distância euclidiana entre dois pontos."""
    return euclidean(a, b)

def manhattan_dist(a: list, b: list) -> float:
    """Calcula a distância de Manhattan entre dois pontos."""
    return cityblock(a, b)

def chebyshev_dist(a: list, b: list) -> float:
    """Calcula a distância de Chebyshev entre dois pontos."""
    return chebyshev(a, b)

def cosine_dist(a: list, b: list) -> float:
    """Calcula a distância do cosseno entre dois vetores."""
    return cosine(a, b)

def hamming_dist_str(a: str, b: str) -> int:
    """Calcula a distância de Hamming entre duas strings."""
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def levenshtein_dist(a: str, b: str) -> int:
    """Calcula a distância de Levenshtein entre duas strings."""
    rows = len(a) + 1
    cols = len(b) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,      # Deletion
                           dp[i][j - 1] + 1,      # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution
    return dp[rows - 1][cols - 1]

def jaccard_index(a: Union[list, set], b: Union[list, set]) -> float:
    """Calcula o índice de Jaccard entre dois conjuntos."""
    set_a, set_b = set(a), set(b)
    return len(set_a & set_b) / len(set_a | set_b)

def centroid(points: list) -> list:
    """Calcula o centroide de um conjunto de pontos."""
    return np.mean(points, axis=0).tolist()
