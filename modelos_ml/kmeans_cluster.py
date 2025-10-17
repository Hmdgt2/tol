from sklearn.cluster import KMeans

def get_model(n_clusters=5):
    """
    Retorna uma instância do modelo KMeans para clustering.
    """
    return KMeans(n_clusters=n_clusters, random_state=42)
