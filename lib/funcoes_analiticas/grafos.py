# lib/funcoes_analiticas/grafos.py
import networkx as nx
import numpy as np
from itertools import combinations
from typing import Dict, List, Set, Any

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

# Criar grafo a partir de lista
def create_graph(lst: list) -> nx.Graph:
    """Cria um grafo completo a partir de uma lista de nós."""
    G = nx.Graph()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            G.add_edge(lst[i], lst[j])
    return G

# Número de nós
def num_nodes(lst: list) -> int:
    """Retorna o número de nós de um grafo criado a partir de uma lista."""
    return create_graph(lst).number_of_nodes()

# Número de arestas
def num_edges(lst: list) -> int:
    """Retorna o número de arestas de um grafo completo."""
    return create_graph(lst).number_of_edges()

# Graus dos nós
def node_degrees(lst: list) -> list:
    """Calcula os graus de cada nó em um grafo."""
    G = create_graph(lst)
    return [d for n, d in G.degree()]

# Grafo completo?
def is_complete(lst: list) -> bool:
    """Verifica se um grafo criado a partir da lista é completo."""
    G = create_graph(lst)
    n = G.number_of_nodes()
    return G.number_of_edges() == n * (n - 1) / 2

# Diâmetro do grafo
def graph_diameter(lst: list) -> float:
    """Calcula o diâmetro do grafo (maior caminho mais curto)."""
    G = create_graph(lst)
    if nx.is_connected(G):
        return nx.diameter(G)
    else:
        return 0

# Média dos graus
def mean_degree(lst: list) -> float:
    """Calcula o grau médio de um grafo."""
    return np.mean(node_degrees(lst))

# Desvio padrão dos graus
def std_degree(lst: list) -> float:
    """Calcula o desvio padrão dos graus de um grafo."""
    return np.std(node_degrees(lst))

# Centralidade de grau
def degree_centrality(lst: list) -> list:
    """Calcula a centralidade de grau de cada nó."""
    G = create_graph(lst)
    return list(nx.degree_centrality(G).values())

# Centralidade de proximidade
def closeness_centrality(lst: list) -> list:
    """Calcula a centralidade de proximidade de cada nó."""
    G = create_graph(lst)
    return list(nx.closeness_centrality(G).values())

# Densidade do grafo
def graph_density(lst: list) -> float:
    """Calcula a densidade do grafo."""
    G = create_graph(lst)
    return nx.density(G)
