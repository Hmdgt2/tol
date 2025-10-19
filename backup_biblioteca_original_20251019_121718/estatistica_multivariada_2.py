# lib/funcoes_analiticas/estatistica_multivariada.py
import numpy as np
from typing import List, Tuple
from scipy import stats, linalg
from sklearn.decomposition import PCA, FastICA

# ============================================================
# Análise de Componentes
# ============================================================

def mahalanobis_distance(X: List[List[float]]) -> List[float]:
    """Distância de Mahalanobis para cada ponto."""
    X_arr = np.array(X)
    mean = np.mean(X_arr, axis=0)
    cov = np.cov(X_arr, rowvar=False)
    try:
        inv_cov = linalg.inv(cov)
    except linalg.LinAlgError:
        inv_cov = np.linalg.pinv(cov)
    
    distances = []
    for x in X_arr:
        diff = x - mean
        distance = np.sqrt(diff @ inv_cov @ diff.T)
        distances.append(distance)
    
    return distances

def hotelling_t2_test(X: List[List[float]], Y: List[List[float]]) -> Tuple[float, float]:
    """Teste T² de Hotelling para duas amostras multivariadas."""
    X_arr, Y_arr = np.array(X), np.array(Y)
    n1, n2 = len(X_arr), len(Y_arr)
    
    mean1, mean2 = np.mean(X_arr, axis=0), np.mean(Y_arr, axis=0)
    cov1, cov2 = np.cov(X_arr, rowvar=False), np.cov(Y_arr, rowvar=False)
    
    pooled_cov = ((n1 - 1) * cov1 + (n2 - 1) * cov2) / (n1 + n2 - 2)
    
    try:
        inv_pooled = linalg.inv(pooled_cov)
    except linalg.LinAlgError:
        inv_pooled = np.linalg.pinv(pooled_cov)
    
    diff = mean1 - mean2
    T2 = (n1 * n2 / (n1 + n2)) * (diff @ inv_pooled @ diff.T)
    
    # Estatística F
    p = X_arr.shape[1]
    F_stat = (n1 + n2 - p - 1) * T2 / ((n1 + n2 - 2) * p)
    p_value = 1 - stats.f.cdf(F_stat, p, n1 + n2 - p - 1)
    
    return float(F_stat), float(p_value)

# ============================================================
# Análise de Correlação
# ============================================================

def canonical_correlation(X: List[List[float]], Y: List[List[float]]) -> Tuple:
    """Correlação canônica entre dois conjuntos de variáveis."""
    X_arr, Y_arr = np.array(X), np.array(Y)
    
    # Centrar os dados
    X_centered = X_arr - np.mean(X_arr, axis=0)
    Y_centered = Y_arr - np.mean(Y_arr, axis=0)
    
    # Matrizes de covariância
    Cxx = np.cov(X_centered, rowvar=False)
    Cyy = np.cov(Y_centered, rowvar=False)
    Cxy = np.cov(X_centered, Y_centered, rowvar=False)[:X_arr.shape[1], X_arr.shape[1]:]
    
    try:
        # Resolver problema de autovalor generalizado
        inv_Cxx = linalg.inv(Cxx)
        inv_Cyy = linalg.inv(Cyy)
        
        M = inv_Cxx @ Cxy @ inv_Cyy @ Cxy.T
        eigenvalues = linalg.eigvals(M)
        
        # Correlações canônicas são raízes quadradas dos autovalores
        canonical_corrs = np.sqrt(np.real(eigenvalues))
        return canonical_corrs.tolist()
    except:
        return [0.0]

# ============================================================
# Análise de Discriminante
# ============================================================

def linear_discriminant_analysis(X: List[List[float]], y: List[int]) -> Tuple:
    """Análise de Discriminante Linear simplificada."""
    X_arr, y_arr = np.array(X), np.array(y)
    classes = np.unique(y_arr)
    
    # Médias globais e por classe
    overall_mean = np.mean(X_arr, axis=0)
    
    # Matriz de dispersão entre classes
    Sb = np.zeros((X_arr.shape[1], X_arr.shape[1]))
    # Matriz de dispersão dentro das classes
    Sw = np.zeros((X_arr.shape[1], X_arr.shape[1]))
    
    for c in classes:
        X_c = X_arr[y_arr == c]
        mean_c = np.mean(X_c, axis=0)
        n_c = len(X_c)
        
        # Between-class scatter
        diff = (mean_c - overall_mean).reshape(-1, 1)
        Sb += n_c * (diff @ diff.T)
        
        # Within-class scatter
        Sw += np.cov(X_c, rowvar=False) * (n_c - 1)
    
    try:
        # Resolver problema de autovalor generalizado
        eigenvalues, eigenvectors = linalg.eig(Sb, Sw)
        # Ordenar por autovalor
        idx = np.argsort(np.real(eigenvalues))[::-1]
        eigenvectors = eigenvectors[:, idx]
        
        return np.real(eigenvectors).tolist(), np.real(eigenvalues[idx]).tolist()
    except:
        return [], []
