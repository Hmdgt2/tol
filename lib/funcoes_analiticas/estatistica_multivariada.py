# lib/funcoes_analiticas/estatistica_multivariada.py
import numpy as np
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score, silhouette_score
from typing import List

def covariance_matrix(X: list) -> list:
    """Calcula a matriz de covariância de um conjunto de dados."""
    return np.cov(np.array(X), rowvar=False).tolist()

def correlation_matrix(X: list) -> list:
    """Calcula a matriz de correlação de um conjunto de dados."""
    return np.corrcoef(np.array(X), rowvar=False).tolist()

def mutual_info(x: list, y: list) -> float:
    """Calcula a informação mútua entre duas variáveis discretas."""
    return mutual_info_score(x, y)

def normalized_mutual_info(x: list, y: list) -> float:
    """Calcula a informação mútua normalizada."""
    return normalized_mutual_info_score(x, y)

def silhouette(X: list, labels: list) -> float:
    """Calcula o coeficiente de silhueta para avaliar a qualidade de um agrupamento."""
    return silhouette_score(np.array(X), np.array(labels))

def pca_eigenvalues(X: list) -> list:
    """Calcula os autovalores da matriz de covariância para a Análise de Componentes Principais (PCA)."""
    return np.linalg.eigvals(np.cov(np.array(X), rowvar=False)).tolist()

def gini_index(values: list) -> float:
    """Calcula o índice de Gini para medir a desigualdade."""
    arr = np.array(values)
    arr_sorted = np.sort(arr)
    n = len(arr)
    cum = np.cumsum(arr_sorted) / np.sum(arr_sorted) if np.sum(arr_sorted) != 0 else np.zeros_like(arr)
    return 1 - 2 * np.sum(cum) / n
