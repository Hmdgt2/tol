# lib/funcoes_analiticas/estatistica_multivariada.py
import numpy as np
from sklearn.metrics import mutual_info_score, normalized_mutual_info_score, silhouette_score
from typing import List

# ============================================================
# Estatística Multivariada
# ============================================================

def covariance_matrix(X: List[List[float]]) -> List[List[float]]:
    """
    Calcula a matriz de covariância de um conjunto de dados.
    
    Args:
        X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.
    
    Returns:
        List[List[float]]: Matriz de covariância.
    """
    return np.cov(np.array(X), rowvar=False).tolist()


def correlation_matrix(X: List[List[float]]) -> List[List[float]]:
    """
    Calcula a matriz de correlação de um conjunto de dados.
    
    Args:
        X (List[List[float]]): Matriz de dados, linhas = amostras, colunas = variáveis.
    
    Returns:
        List[List[float]]: Matriz de correlação.
    """
    return np.corrcoef(np.array(X), rowvar=False).tolist()


def mutual_info(x: List[int], y: List[int]) -> float:
    """
    Calcula a informação mútua entre duas variáveis discretas.
    
    Args:
        x (List[int]): Primeira variável discreta.
        y (List[int]): Segunda variável discreta.
    
    Returns:
        float: Informação mútua.
    """
    return mutual_info_score(x, y)


def normalized_mutual_info(x: List[int], y: List[int]) -> float:
    """
    Calcula a informação mútua normalizada entre duas variáveis discretas.
    
    Args:
        x (List[int]): Primeira variável discreta.
        y (List[int]): Segunda variável discreta.
    
    Returns:
        float: Informação mútua normalizada.
    """
    return normalized_mutual_info_score(x, y)


def silhouette(X: List[List[float]], labels: List[int]) -> float:
    """
    Calcula o coeficiente de silhueta para avaliar a qualidade de um agrupamento.
    
    Args:
        X (List[List[float]]): Matriz de dados.
        labels (List[int]): Rótulos de cluster para cada ponto.
    
    Returns:
        float: Coeficiente de silhueta.
    """
    return silhouette_score(np.array(X), np.array(labels))


def pca_eigenvalues(X: List[List[float]]) -> List[float]:
    """
    Calcula os autovalores da matriz de covariância para a Análise de Componentes Principais (PCA).
    
    Args:
        X (List[List[float]]): Matriz de dados.
    
    Returns:
        List[float]: Autovalores da matriz de covariância.
    """
    return np.linalg.eigvals(np.cov(np.array(X), rowvar=False)).tolist()


def gini_index(values: List[float]) -> float:
    """
    Calcula o índice de Gini para medir a desigualdade.
    
    Args:
        values (List[float]): Lista de valores.
    
    Returns:
        float: Índice de Gini (0 = igualdade perfeita, 1 = desigualdade máxima).
    """
    arr = np.array(values)
    arr_sorted = np.sort(arr)
    n = len(arr)
    cum = np.cumsum(arr_sorted) / np.sum(arr_sorted) if np.sum(arr_sorted) != 0 else np.zeros_like(arr)
    return 1 - 2 * np.sum(cum) / n
