# lib/funcoes_analiticas/geometria_diferencial.py
import numpy as np
from typing import List, Callable
from scipy import interpolate

def gaussian_curvature(surface_points: List[List[float]]) -> List[float]:
    """Curvatura gaussiana aproximada de uma superfície."""
    if len(surface_points) < 9:  # Precisa de vizinhança para cálculo
        return [0.0] * len(surface_points)
    
    curvatures = []
    points = np.array(surface_points)
    
    for i, point in enumerate(points):
        # Encontrar vizinhos próximos
        distances = np.linalg.norm(points - point, axis=1)
        neighbors_idx = np.argsort(distances)[:9]  # 8 vizinhos + próprio ponto
        
        if len(neighbors_idx) >= 5:
            # Ajustar superfície quadrática local
            neighbors = points[neighbors_idx]
            A = np.column_stack([neighbors[:,0]**2, neighbors[:,0]*neighbors[:,1], 
                               neighbors[:,1]**2, neighbors[:,0], neighbors[:,1], np.ones(len(neighbors))])
            z = neighbors[:,2]
            
            try:
                coeffs = np.linalg.lstsq(A, z, rcond=None)[0]
                # Curvatura gaussiana = (4 * a * c - b²) / (1 + d² + e²)²
                a, b, c, d, e, _ = coeffs
                gaussian_curv = (4 * a * c - b**2) / (1 + d**2 + e**2)**2
                curvatures.append(gaussian_curv)
            except:
                curvatures.append(0.0)
        else:
            curvatures.append(0.0)
    
    return curvatures

def geodesic_distance(surface_func: Callable, point1: List[float], point2: List[float], 
                     steps: int = 100) -> float:
    """Distância geodésica aproximada entre dois pontos em uma superfície."""
    # Método de shooting simplificado
    t_values = np.linspace(0, 1, steps)
    path = []
    
    for t in t_values:
        # Interpolação linear na superfície
        point = [(1-t)*p1 + t*p2 for p1, p2 in zip(point1[:2], point2[:2])]
        z = surface_func(point[0], point[1])
        path.append([point[0], point[1], z])
    
    # Comprimento da curva
    length = 0.0
    for i in range(len(path)-1):
        length += np.linalg.norm(np.array(path[i+1]) - np.array(path[i]))
    
    return length

def riemann_metric_tensor(surface_func: Callable, u: float, v: float, eps: float = 1e-6) -> List[List[float]]:
    """Tensor métrico de Riemann em um ponto da superfície."""
    # Derivadas parciais
    f_uu = surface_func(u + eps, v) - 2 * surface_func(u, v) + surface_func(u - eps, v)
    f_uv = (surface_func(u + eps, v + eps) - surface_func(u + eps, v - eps) - 
            surface_func(u - eps, v + eps) + surface_func(u - eps, v - eps)) / (4 * eps**2)
    f_vv = surface_func(u, v + eps) - 2 * surface_func(u, v) + surface_func(u, v - eps)
    
    # Coeficientes da primeira forma fundamental
    E = 1 + f_uu**2
    F = f_uu * f_uv
    G = 1 + f_vv**2
    
    return [[E, F], [F, G]]
