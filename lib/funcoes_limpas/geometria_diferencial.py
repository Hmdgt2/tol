
import numpy as np
from typing import List, Callable
from scipy import interpolate


def geodesic_distance(surface_func: Callable, point1: List[float], point2: List[float], steps: int=100) -> float:
    'Distância geodésica aproximada entre dois pontos em uma superfície.'
    t_values = np.linspace(0, 1, steps)
    path = []
    for t in t_values:
        point = [(((1 - t) * p1) + (t * p2)) for (p1, p2) in zip(point1[:2], point2[:2])]
        z = surface_func(point[0], point[1])
        path.append([point[0], point[1], z])
    length = 0.0
    for i in range((len(path) - 1)):
        length += np.linalg.norm((np.array(path[(i + 1)]) - np.array(path[i])))
    return length


def riemann_metric_tensor(surface_func: Callable, u: float, v: float, eps: float=1e-06) -> List[List[float]]:
    'Tensor métrico de Riemann em um ponto da superfície.'
    f_uu = ((surface_func((u + eps), v) - (2 * surface_func(u, v))) + surface_func((u - eps), v))
    f_uv = ((((surface_func((u + eps), (v + eps)) - surface_func((u + eps), (v - eps))) - surface_func((u - eps), (v + eps))) + surface_func((u - eps), (v - eps))) / (4 * (eps ** 2)))
    f_vv = ((surface_func(u, (v + eps)) - (2 * surface_func(u, v))) + surface_func(u, (v - eps)))
    E = (1 + (f_uu ** 2))
    F = (f_uu * f_uv)
    G = (1 + (f_vv ** 2))
    return [[E, F], [F, G]]

