# lib/funcoes_analiticas/grafos.py
import networkx as nx
from itertools import combinations
from typing import List

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
