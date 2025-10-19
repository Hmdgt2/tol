# lib/funcoes_analiticas/geometria_computacional.py
import numpy as np
from typing import List, Tuple, Dict
from scipy.spatial import ConvexHull, Delaunay, Voronoi
import math

# ============================================================
# Análise de Padrões Geométricos
# ============================================================

def spiral_coordinate_analysis(seq: List[int]) -> Dict:
    """Analisa sequências em espiral (Ulam, Arquimedes, etc)."""
    if len(seq) < 4:
        return {"error": "Sequência muito curta para análise de espiral"}
    
    # Converte sequência em coordenadas espirais
    def spiral_coordinates(n):
        if n == 0:
            return (0, 0)
        k = math.ceil((math.sqrt(n) - 1) / 2)
        t = 2 * k + 1
        m = t ** 2
        t -= 1
        if n >= m - t:
            return (k - (m - n), -k)
        m -= t
        if n >= m - t:
            return (-k, -k + (m - n))
        m -= t
        if n >= m - t:
            return (-k + (m - n), k)
        return (k, k - (m - n - t))
    
    points = [spiral_coordinates(x) for x in seq]
    x_coords, y_coords = zip(*points)
    
    # Análise de padrão espiral
    angles = [math.atan2(y, x) for x, y in points if x != 0 or y != 0]
    radii = [math.sqrt(x**2 + y**2) for x, y in points]
    
    return {
        "spiral_points": points,
        "angular_variance": np.var(angles) if angles else 0,
        "radial_variance": np.var(radii),
        "center_of_mass": (np.mean(x_coords), np.mean(y_coords)),
        "is_archimedean": np.var(radii) > 0.1  # Simplificado
    }

def voronoi_tessellation_analysis(seq: List[float]) -> Dict:
    """Análise de tesselação de Voronoi gerada pela sequência."""
    if len(seq) < 3:
        return {"error": "Sequência muito curta para tesselação"}
    
    # Converte sequência 1D em pontos 2D
    points = np.array([[x, x**2] for x in seq])  # Transformação simples para 2D
    
    try:
        vor = Voronoi(points)
        
        # Estatísticas da tesselação
        areas = []
        for region in vor.regions:
            if not region or -1 in region:
                continue
            polygon = [vor.vertices[i] for i in region]
            if len(polygon) >= 3:
                area = ConvexHull(polygon).volume  # Área em 2D
                areas.append(area)
        
        return {
            "num_regions": len([r for r in vor.regions if r and -1 not in r]),
            "num_vertices": len(vor.vertices),
            "area_statistics": {
                "mean": np.mean(areas) if areas else 0,
                "std": np.std(areas) if areas else 0,
                "min": min(areas) if areas else 0,
                "max": max(areas) if areas else 0
            },
            "ridge_lengths": [np.linalg.norm(vor.vertices[i] - vor.vertices[j]) 
                            for ridge in vor.ridge_vertices 
                            for i, j in itertools.combinations(ridge, 2) 
                            if i != -1 and j != -1]
        }
    except Exception as e:
        return {"error": f"Erro na tesselação: {str(e)}"}

def convex_hull_evolution(seq: List[Tuple[float, float]]) -> Dict:
    """Evolução do convex hull em sequências de pontos."""
    if len(seq) < 3:
        return {"error": "Mínimo 3 pontos necessários"}
    
    points = np.array(seq)
    hull_evolution = []
    area_evolution = []
    
    for i in range(3, len(seq) + 1):
        try:
            subset = points[:i]
            hull = ConvexHull(subset)
            hull_evolution.append(hull.vertices.tolist())
            area_evolution.append(hull.volume)  # Área em 2D
        except:
            continue
    
    return {
        "hull_evolution": hull_evolution,
        "area_evolution": area_evolution,
        "area_growth_rate": np.gradient(area_evolution) if area_evolution else [],
        "final_hull_area": area_evolution[-1] if area_evolution else 0,
        "stability_metric": np.std(area_evolution[-5:]) if len(area_evolution) >= 5 else 0
    }
