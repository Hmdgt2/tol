# lib/funcoes_analiticas/redes_especializadas.py
import numpy as np
from typing import List, Dict, Tuple
import networkx as nx
from collections import defaultdict

# ============================================================
# Redes Temporais e Multiplex
# ============================================================

def temporal_network_metrics(edges_time_series: List[List[Tuple]]) -> Dict:
    """Calcula métricas para redes temporais."""
    if not edges_time_series:
        return {"error": "Série temporal de arestas vazia"}
    
    # Constrói rede temporal
    temporal_graph = build_temporal_network(edges_time_series)
    
    # Métricas temporais
    temporal_metrics = calculate_temporal_metrics(temporal_graph)
    
    # Componentes temporais
    temporal_components = find_temporal_components(temporal_graph)
    
    # Centralidade temporal
    temporal_centrality = calculate_temporal_centrality(temporal_graph)
    
    return {
        "temporal_structure": {
            "time_steps": len(edges_time_series),
            "total_edges": sum(len(edges) for edges in edges_time_series),
            "edge_activity_distribution": analyze_edge_activity(edges_time_series)
        },
        "temporal_metrics": temporal_metrics,
        "temporal_components": temporal_components,
        "centrality_measures": temporal_centrality,
        "dynamics_analysis": {
            "burstiness": calculate_burstiness(edges_time_series),
            "memory_effects": analyze_memory_effects(edges_time_series),
            "seasonality": detect_seasonality(edges_time_series)
        },
        "causal_paths": find_causal_paths(temporal_graph)
    }

def multiplex_network_analysis(layers: List[Dict]) -> Dict:
    """Analisa rede multiplex com múltiplas camadas."""
    if len(layers) < 2:
        return {"error": "Pelo menos duas camadas necessárias para análise multiplex"}
    
    # Constrói rede multiplex
    multiplex_graph = build_multiplex_network(layers)
    
    # Correlação entre camadas
    layer_correlation = calculate_layer_correlation(layers)
    
    # Centralidade multiplex
    multiplex_centrality = calculate_multiplex_centrality(multiplex_graph, layers)
    
    # Comunidades multiplex
    multiplex_communities = detect_multiplex_communities(multiplex_graph)
    
    return {
        "multiplex_structure": {
            "number_of_layers": len(layers),
            "nodes_per_layer": [len(layer.get('nodes', [])) for layer in layers],
            "edges_per_layer": [len(layer.get('edges', [])) for layer in layers]
        },
        "layer_correlation": layer_correlation,
        "multiplex_centrality": multiplex_centrality,
        "community_structure": multiplex_communities,
        "interlayer_analysis": {
            "coupling_strength": calculate_interlayer_coupling(layers),
            "structural_similarity": calculate_structural_similarity(layers),
            "functional_redundancy": calculate_functional_redundancy(layers)
        },
        "robustness_analysis": analyze_multiplex_robustness(multiplex_graph, layers)
    }

def hypergraph_clustering_coefficient(hypergraph: Dict) -> Dict:
    """Calcula coeficiente de agrupamento para hipergrafo."""
    nodes = hypergraph.get('nodes', [])
    hyperedges = hypergraph.get('hyperedges', [])
    
    if not nodes or not hyperedges:
        return {"error": "Hipergrafo vazio ou mal definido"}
    
    # Coeficiente de agrupamento hipergraph
    clustering_coefficient = calculate_hypergraph_clustering(nodes, hyperedges)
    
    # Overlap analysis
    overlap_analysis = analyze_hyperedge_overlap(hyperedges)
    
    # Core-periphery structure
    core_periphery = identify_hypergraph_core_periphery(nodes, hyperedges)
    
    return {
        "hypergraph_properties": {
            "number_of_nodes": len(nodes),
            "number_of_hyperedges": len(hyperedges),
            "average_hyperedge_size": np.mean([len(he) for he in hyperedges]),
            "hyperedge_size_distribution": [len(he) for he in hyperedges]
        },
        "clustering_analysis": {
            "global_clustering_coefficient": clustering_coefficient,
            "local_clustering_distribution": calculate_local_hypergraph_clustering(nodes, hyperedges),
            "transitivity_measure": calculate_hypergraph_transitivity(hyperedges)
        },
        "overlap_analysis": overlap_analysis,
        "core_periphery_structure": core_periphery,
        "higher_order_connections": analyze_higher_order_connections(hyperedges),
        "applications": identify_hypergraph_applications(hypergraph)
    }

def build_temporal_network(edges_time_series: List[List[Tuple]]) -> Dict:
    """Constrói representação de rede temporal."""
    temporal_graph = {
        'time_steps': len(edges_time_series),
        'nodes': set(),
        'temporal_edges': []
    }
    
    for t, edges in enumerate(edges_time_series):
        for edge in edges:
            u, v = edge
            temporal_graph['nodes'].add(u)
            temporal_graph['nodes'].add(v)
            temporal_graph['temporal_edges'].append((u, v, t))
    
    temporal_graph['nodes'] = list(temporal_graph['nodes'])
    return temporal_graph

def calculate_temporal_metrics(temporal_graph: Dict) -> Dict:
    """Calcula métricas temporais para rede."""
    return {
        "temporal_density": len(temporal_graph['temporal_edges']) / (len(temporal_graph['nodes']) * temporal_graph['time_steps']),
        "temporal_clustering": estimate_temporal_clustering(temporal_graph),
        "temporal_efficiency": calculate_temporal_efficiency(temporal_graph),
        "latency": calculate_network_latency(temporal_graph)
    }

def build_multiplex_network(layers: List[Dict]) -> Dict:
    """Constrói rede multiplex a partir de camadas."""
    multiplex = {
        'layers': [],
        'interlayer_edges': [],
        'node_mapping': {}
    }
    
    node_counter = 0
    for i, layer in enumerate(layers):
        layer_data = {
            'layer_id': i,
            'nodes': layer.get('nodes', []),
            'edges': layer.get('edges', []),
            'start_index': node_counter
        }
        multiplex['layers'].append(layer_data)
        
        # Mapeamento de nós
        for node in layer['nodes']:
            multiplex['node_mapping'][(i, node)] = node_counter
            node_counter += 1
    
    return multiplex
