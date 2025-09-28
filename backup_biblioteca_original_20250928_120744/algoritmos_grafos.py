# lib/grafos/algoritmos_grafos.py

import networkx as nx
from typing import Any, List, Optional, Dict


# ============================================================
# Algoritmos de caminhos
# ============================================================

def dijkstra_path(
    G: nx.Graph, source: Any, target: Any, weight: Optional[str] = "weight"
) -> List[Any]:
    """Encontra o caminho mais curto entre origem e destino (Dijkstra)."""
    return nx.dijkstra_path(G, source, target, weight=weight)


def dijkstra_length(
    G: nx.Graph, source: Any, target: Any, weight: Optional[str] = "weight"
) -> float:
    """Calcula o comprimento do caminho mais curto entre origem e destino (Dijkstra)."""
    return nx.dijkstra_path_length(G, source, target, weight=weight)


def shortest_path_all_pairs(G: nx.Graph) -> Dict[Any, Dict[Any, int]]:
    """Encontra o comprimento do caminho mais curto entre todos os pares de nós."""
    return dict(nx.shortest_path_length(G))


# ============================================================
# Propriedades do grafo
# ============================================================

def is_connected(G: nx.Graph) -> bool:
    """Verifica se o grafo é conexo."""
    return nx.is_connected(G)


def has_cycle(G: nx.Graph) -> bool:
    """Verifica se o grafo contém pelo menos um ciclo."""
    try:
        nx.find_cycle(G)
        return True
    except nx.NetworkXNoCycle:
        return False
