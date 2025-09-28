
import numpy as np
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score, silhouette_score
from typing import List

def covariance_matrix(X: List[List[float]]) -> List[List[float]]:
    '\n    Calcula a matriz de covariância de um conjunto de dados.\n    \n    Args:\n        X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.\n    \n    Returns:\n        List[List[float]]: Matriz de covariância.\n    '
    return np.cov(np.array(X), rowvar=False).tolist()

def correlation_matrix(X: List[List[float]]) -> List[List[float]]:
    '\n    Calcula a matriz de correlação de um conjunto de dados.\n    \n    Args:\n        X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.\n    \n    Returns:\n        List[List[float]]: Matriz de correlação.\n    '
    return np.corrcoef(np.array(X), rowvar=False).tolist()

def silhouette(X: List[List[float]], labels: List[int]) -> float:
    '\n    Calcula o coeficiente de silhueta para avaliar a qualidade de um agrupamento.\n    \n    Args:\n        X (List[List[float]]): Matriz de dados.\n        labels (List[int]): Rótulos de cluster para cada ponto.\n    \n    Returns:\n        float: Coeficiente de silhueta.\n    '
    return silhouette_score(np.array(X), np.array(labels))

def pca_eigenvalues(X: List[List[float]]) -> List[float]:
    '\n    Calcula os autovalores da matriz de covariância para a Análise de Componentes Principais (PCA).\n    \n    Args:\n        X (List[List[float]]): Matriz de dados.\n    \n    Returns:\n        List[float]: Autovalores da matriz de covariância.\n    '
    return np.linalg.eigvals(np.cov(np.array(X), rowvar=False)).tolist()

def gini_index(values: List[float]) -> float:
    '\n    Calcula o índice de Gini para medir a desigualdade.\n    \n    Args:\n        values (List[float]): Lista de valores.\n    \n    Returns:\n        float: Índice de Gini (0 = igualdade perfeita, 1 = desigualdade máxima).\n    '
    arr = np.array(values)
    arr_sorted = np.sort(arr)
    n = len(arr)
    cum = ((np.cumsum(arr_sorted) / np.sum(arr_sorted)) if (np.sum(arr_sorted) != 0) else np.zeros_like(arr))
    return (1 - ((2 * np.sum(cum)) / n))
