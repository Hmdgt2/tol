


def convex_hull_area(points: List[Tuple[(float, float)]]) -> float:
    'Área do convex hull de um conjunto de pontos.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (len(points) < 3):
        return 0.0
    hull = spatial.ConvexHull(points)
    return hull.volume


def smallest_enclosing_circle(points: List[Tuple[(float, float)]]) -> Tuple:
    'Círculo mínimo que engloba todos os pontos.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'

    def circle_radius(cx, cy, points):
        return max((np.hypot((cx - x), (cy - y)) for (x, y) in points))

    def objective(params):
        return circle_radius(params[0], params[1], points)
    centroid = np.mean(points, axis=0)
    result = optimize.minimize(objective, centroid, method='Nelder-Mead')
    if result.success:
        (cx, cy) = result.x
        radius = circle_radius(cx, cy, points)
        return (cx, cy, radius)
    return (0.0, 0.0, 0.0)


def gaussian_curvature(surface_points: List[List[float]]) -> List[float]:
    'Curvatura gaussiana aproximada de uma superfície.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    if (len(surface_points) < 9):
        return ([0.0] * len(surface_points))
    curvatures = []
    points = np.array(surface_points)
    for (i, point) in enumerate(points):
        distances = np.linalg.norm((points - point), axis=1)
        neighbors_idx = np.argsort(distances)[:9]
        if (len(neighbors_idx) >= 5):
            neighbors = points[neighbors_idx]
            A = np.column_stack([(neighbors[(:, 0)] ** 2), (neighbors[(:, 0)] * neighbors[(:, 1)]), (neighbors[(:, 1)] ** 2), neighbors[(:, 0)], neighbors[(:, 1)], np.ones(len(neighbors))])
            z = neighbors[(:, 2)]
            try:
                coeffs = np.linalg.lstsq(A, z, rcond=None)[0]
                (a, b, c, d, e, _) = coeffs
                gaussian_curv = ((((4 * a) * c) - (b ** 2)) / (((1 + (d ** 2)) + (e ** 2)) ** 2))
                curvatures.append(gaussian_curv)
            except:
                curvatures.append(0.0)
        else:
            curvatures.append(0.0)
    return curvatures

