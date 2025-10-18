# lib/funcoes_analiticas/redes_complexas_temporais.py
import numpy as np
from typing import List, Dict
import networkx as nx

def temporal_network_analysis(seq: List[float], threshold: float = 0.5) -> Dict:
    """Constrói e analisa redes complexas a partir da evolução temporal."""
    if len(seq) < 20:
        return {}
    
    # Constrói matriz de correlação temporal
    n = len(seq)
    correlation_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i, n):
            # Correlação baseada na evolução temporal
            if i == j:
                correlation_matrix[i, j] = 1.0
            else:
                # Considera a evolução até cada ponto
                min_len = min(i, j) + 1
                corr = np.corrcoef(seq[:i+1], seq[:j+1])[0,1] if min_len > 5 else 0
                correlation_matrix[i, j] = corr if not np.isnan(corr) else 0
                correlation_matrix[j, i] = correlation_matrix[i, j]
    
    # Constrói grafo da rede temporal
    G = nx.Graph()
    for i in range(n):
        G.add_node(i, value=seq[i])
    
    for i in range(n):
        for j in range(i+1, n):
            if abs(correlation_matrix[i, j]) > threshold:
                G.add_edge(i, j, weight=correlation_matrix[i, j])
    
    # Métricas da rede
    if len(G.nodes) > 0:
        degree_centrality = nx.degree_centrality(G)
        betweenness = nx.betweenness_centrality(G)
        clustering = nx.average_clustering(G)
        
        # Nós mais importantes (hubs temporais)
        hubs = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'network_density': nx.density(G),
            'average_clustering': clustering,
            'degree_assortativity': nx.degree_assortativity_coefficient(G),
            'temporal_hubs': [{'position': hub[0], 'value': seq[hub[0]], 'centrality': hub[1]} for hub in hubs],
            'community_structure': nx.algorithms.community.modularity(G, nx.algorithms.community.greedy_modularity_communities(G)),
            'small_worldness': clustering / (nx.average_shortest_path_length(G) if nx.is_connected(G) else 1)
        }
    
    return {}
