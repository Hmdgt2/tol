# lib/funcoes_analiticas/grafos.py
import networkx as nx
import numpy as np
from itertools import combinations
from typing import Dict, List, Set

def create_graph(lst: list) -> nx.Graph:
    """Cria um grafo a partir de uma lista de números, conectando todos os nós."""
    G = nx.Graph()
    for x in lst:
        G.add_node(x)
    for i, j in combinations(lst, 2):
        G.add_edge(i, j)
    return G

def graph_degree(lst: list) -> dict:
    """Calcula o grau (número de conexões) de cada nó no grafo."""
    G = create_graph(lst)
    return dict(G.degree())

def graph_density(lst: list) -> float:
    """Calcula a densidade do grafo."""
    G = create_graph(lst)
    return nx.density(G)

def graph_avg_degree(lst: list) -> float:
    """Calcula o grau médio de todos os nós do grafo."""
    degs = list(graph_degree(lst).values())
    return sum(degs) / len(degs) if degs else 0

def graph_connected_components_count(lst: list) -> int:
    """Conta o número de componentes conectados no grafo."""
    G = create_graph(lst)
    return nx.number_connected_components(G)

def graph_triangle_count(lst: list) -> int:
    """Conta o número de triângulos no grafo."""
    G = create_graph(lst)
    return sum(nx.triangles(G).values()) // 3

def betweenness_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Calcula a centralidade de intermediação de um grafo."""
    return nx.betweenness_centrality(G)

def eigenvector_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Calcula a centralidade de autovetor de um grafo."""
    try:
        return nx.eigenvector_centrality_numpy(G)
    except:
        return {n: 0 for n in G.nodes()}

def closeness_centrality(G: nx.Graph) -> Dict[Any, float]:
    """Calcula a centralidade de proximidade de um grafo."""
    return nx.closeness_centrality(G)

def pagerank_scores(G: nx.Graph, alpha: float = 0.85) -> Dict[Any, float]:
    """Calcula os scores de PageRank de um grafo."""
    return nx.pagerank(G, alpha=alpha)

def shortest_paths_length(G: nx.Graph) -> Dict[Any, Dict[Any, float]]:
    """Calcula os comprimentos dos caminhos mais curtos entre todos os pares de nós."""
    return dict(nx.shortest_path_length(G))

def graph_eigenvalues(G: nx.Graph) -> np.ndarray:
    """Calcula os autovalores da matriz de adjacência de um grafo."""
    return np.linalg.eigvals(nx.adjacency_matrix(G).todense())

def graph_laplacian_spectrum(G: nx.Graph) -> np.ndarray:
    """Calcula o espectro Laplaciano de um grafo."""
    L = nx.laplacian_matrix(G).todense()
    return np.linalg.eigvals(L)

def graph_connected_components(G: nx.Graph) -> List[Set]:
    """Retorna os componentes conectados de um grafo."""
    return list(nx.connected_components(G))
