# lib/funcoes_analiticas/algebra_linear.py

import numpy as np
from typing import List, Tuple


# ============================================================
# Operações básicas com matrizes
# ============================================================

def matrix_determinant(mat: List[List[float]]) -> float:
    """Calcula o determinante de uma matriz."""
    return float(np.linalg.det(mat))

def matrix_rank(mat: List[List[float]]) -> int:
    """Calcula o posto de uma matriz."""
    return int(np.linalg.matrix_rank(mat))

def matrix_inverse(mat: List[List[float]]) -> List[List[float]]:
    """Calcula a inversa de uma matriz."""
    return np.linalg.inv(mat).tolist()

def matrix_trace(mat: List[List[float]]) -> float:
    """Calcula o traço de uma matriz."""
    return float(np.trace(mat))

def matrix_condition_number(mat: List[List[float]]) -> float:
    """Calcula o número de condição de uma matriz."""
    return float(np.linalg.cond(mat))


# ============================================================
# Normas de matrizes
# ============================================================

def matrix_norm_fro(mat: List[List[float]]) -> float:
    """Calcula a norma de Frobenius de uma matriz."""
    return float(np.linalg.norm(mat, "fro"))

def matrix_norm_inf(mat: List[List[float]]) -> float:
    """Calcula a norma do infinito de uma matriz."""
    return float(np.linalg.norm(mat, np.inf))


# ============================================================
# Autovalores e Autovetores
# ============================================================

def matrix_eigenvalues(mat: List[List[float]]) -> List[float]:
    """Calcula os autovalores de uma matriz."""
    return np.linalg.eigvals(mat).tolist()

def matrix_eigenvectors(mat: List[List[float]]) -> List[List[float]]:
    """Calcula os autovetores de uma matriz."""
    return np.linalg.eig(mat)[1].tolist()


# ============================================================
# Sistemas lineares
# ============================================================

def solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    """Resolve um sistema de equações lineares Ax=b."""
    return np.linalg.solve(A, b).tolist()


# ============================================================
# Decomposições
# ============================================================

def cholesky_decomposition(mat: List[List[float]]) -> List[List[float]]:
    """Realiza a decomposição de Cholesky."""
    return np.linalg.cholesky(mat).tolist()

def qr_decomposition(mat: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
    """Realiza a decomposição QR."""
    Q, R = np.linalg.qr(mat)
    return Q.tolist(), R.tolist()

def svd_u(mat: List[List[float]]) -> List[List[float]]:
    """Retorna a matriz U da SVD."""
    return np.linalg.svd(mat)[0].tolist()

def svd_s(mat: List[List[float]]) -> List[float]:
    """Retorna os valores singulares da SVD."""
    return np.linalg.svd(mat)[1].tolist()

def matrix_pinv(mat: List[List[float]]) -> List[List[float]]:
    """Calcula a pseudoinversa de uma matriz."""
    return np.linalg.pinv(mat).tolist()
