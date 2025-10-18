# lib/funcoes_analiticas/funcoes_diversas.py
import numpy as np
from typing import List, Tuple
from scipy import spatial, optimize
import networkx as nx

# ============================================================
# Geometria Computacional
# ============================================================

def convex_hull_area(points: List[Tuple[float, float]]) -> float:
    """Área do convex hull de um conjunto de pontos."""
    if len(points) < 3:
        return 0.0
    hull = spatial.ConvexHull(points)
    return hull.volume  # Área em 2D

def smallest_enclosing_circle(points: List[Tuple[float, float]]) -> Tuple:
    """Círculo mínimo que engloba todos os pontos."""
    def circle_radius(cx, cy, points):
        return max(np.hypot(cx - x, cy - y) for x, y in points)
    
    def objective(params):
        return circle_radius(params[0], params[1], points)
    
    # Ponto inicial (centroide)
    centroid = np.mean(points, axis=0)
    result = optimize.minimize(objective, centroid, method='Nelder-Mead')
    
    if result.success:
        cx, cy = result.x
        radius = circle_radius(cx, cy, points)
        return (cx, cy, radius)
    
    return (0.0, 0.0, 0.0)

# ============================================================
# Teoria dos Grafos Avançada
# ============================================================

def graph_spectral_gap(adjacency_matrix: List[List[int]]) -> float:
    """Gap espectral do grafo (diferença entre dois maiores autovalores)."""
    G = nx.from_numpy_array(np.array(adjacency_matrix))
    eigenvalues = sorted(nx.laplacian_spectrum(G), reverse=True)
    return eigenvalues[0] - eigenvalues[1] if len(eigenvalues) > 1 else 0.0

def betweenness_centrality_approx(graph_edges: List[Tuple], num_nodes: int, k: int = 50) -> List[float]:
    """Betweenness centrality aproximada usando amostragem."""
    G = nx.Graph()
    G.add_edges_from(graph_edges)
    
    if len(G.nodes) == 0:
        return [0.0] * num_nodes
    
    # Amostrar k nós para cálculo aproximado
    sample_nodes = random.sample(list(G.nodes), min(k, len(G.nodes)))
    betweenness = nx.betweenness_centrality_subset(G, sample_nodes, sample_nodes)
    
    # Preencher para todos os nós
    result = [betweenness.get(i, 0.0) for i in range(num_nodes)]
    return result

# ============================================================
# Criptografia e Hashing
# ============================================================

def simple_hash_function(data: List[int], mod: int = 1000000007) -> int:
    """Função hash simples para lista de inteiros."""
    hash_val = 0
    prime = 31
    for num in data:
        hash_val = (hash_val * prime + num) % mod
    return hash_val

def linear_congruential_generator(seed: int, n: int, 
                                 a: int = 1664525, 
                                 c: int = 1013904223, 
                                 m: int = 2**32) -> List[int]:
    """Gerador congruencial linear para números pseudo-aleatórios."""
    result = []
    current = seed
    for _ in range(n):
        current = (a * current + c) % m
        result.append(current)
    return result

# ============================================================
# Processamento de Linguagem Natural
# ============================================================

def jaccard_similarity(text1: str, text2: str) -> float:
    """Similaridade de Jaccard entre dois textos."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0

def levenshtein_distance_ratio(s1: str, s2: str) -> float:
    """Razão de similaridade baseada na distância de Levenshtein."""
    if len(s1) == 0 or len(s2) == 0:
        return 0.0
    
    # Implementação da distância de Levenshtein
    if len(s1) < len(s2):
        return levenshtein_distance_ratio(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    max_len = max(len(s1), len(s2))
    return 1 - (distance / max_len) if max_len > 0 else 0.0
