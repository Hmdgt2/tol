


def mahalanobis_distance(X: List[List[float]]) -> List[float]:
    'Distância de Mahalanobis para cada ponto.\n\n\n🔬 **Categoria**: Função Analítica\n🎯 **Propósito**: Análise de padrões matemáticos\n'
    X_arr = np.array(X)
    mean = np.mean(X_arr, axis=0)
    cov = np.cov(X_arr, rowvar=False)
    try:
        inv_cov = linalg.inv(cov)
    except linalg.LinAlgError:
        inv_cov = np.linalg.pinv(cov)
    distances = []
    for x in X_arr:
        diff = (x - mean)
        distance = np.sqrt(((diff @ inv_cov) @ diff.T))
        distances.append(distance)
    return distances

