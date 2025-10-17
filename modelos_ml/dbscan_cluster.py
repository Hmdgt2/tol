from sklearn.cluster import DBSCAN

def get_model(eps=0.5, min_samples=5):
    """
    Retorna uma instância do modelo DBSCAN para clustering denso.
    """
    return DBSCAN(eps=eps, min_samples=min_samples)
