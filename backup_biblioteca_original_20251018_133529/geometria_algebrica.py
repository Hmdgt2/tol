# lib/funcoes_analiticas/geometria_algebrica.py
import numpy as np
from typing import List, Callable
from scipy import optimize

def variety_dimension(polynomials: List[Callable], points: List[List[float]]) -> int:
    """Dimensão de variedade algébrica aproximada."""
    if not points:
        return 0
    
    # Avaliar gradientes nos pontos
    gradients = []
    for point in points:
        grad_at_point = []
        for poly in polynomials:
            # Aproximação numérica do gradiente
            eps = 1e-6
            grad = []
            for i in range(len(point)):
                point_plus = point.copy()
                point_plus[i] += eps
                point_minus = point.copy()
                point_minus[i] -= eps
                derivative = (poly(point_plus) - poly(point_minus)) / (2 * eps)
                grad.append(derivative)
            grad_at_point.append(grad)
        gradients.append(grad_at_point)
    
    # Dimensão ≈ dimensão do espaço menos posto do Jacobiano
    if gradients and gradients[0]:
        avg_rank = np.mean([np.linalg.matrix_rank(np.array(g)) for g in gradients])
        return max(0, len(points[0]) - int(avg_rank))
    return 0

def bezout_theorem_degree(curve1: Callable, curve2: Callable, domain: List[float]) -> int:
    """Número de interseções entre duas curvas (Teorema de Bézout)."""
    # Contar zeros do sistema em uma amostra
    sample_points = np.linspace(domain[0], domain[1], 1000)
    intersections = 0
    
    for i in range(len(sample_points) - 1):
        x1, x2 = sample_points[i], sample_points[i+1]
        y1_1, y1_2 = curve1(x1), curve1(x2)
        y2_1, y2_2 = curve2(x1), curve2(x2)
        
        # Verificar mudança de sinal
        if (y1_1 - y2_1) * (y1_2 - y2_2) < 0:
            intersections += 1
    
    return intersections

def algebraic_curve_genus(degree: int, singular_points: int = 0) -> int:
    """Gênero de curva algébrica (fórmula de Plücker simplificada)."""
    return max(0, (degree - 1) * (degree - 2) // 2 - singular_points)

def projective_space_embedding(points: List[List[float]]) -> List[List[float]]:
    """Embedding em espaço projetivo (homogeneização)."""
    projective_points = []
    for point in points:
        # Adicionar coordenada homogênea
        if point:
            homogeneous = point + [1.0]
            # Normalizar
            norm = np.linalg.norm(homogeneous)
            if norm > 0:
                homogeneous = [x / norm for x in homogeneous]
            projective_points.append(homogeneous)
    return projective_points
