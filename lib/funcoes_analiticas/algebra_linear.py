# lib/funcoes_analiticas/algebra_linear.py
import numpy as np
from typing import List, Tuple

def matrix_determinant(mat: list) -> float:
    """Calcula o determinante de uma matriz."""
    return float(np.linalg.det(mat))

def matrix_rank(mat: list) -> int:
    """Calcula o posto de uma matriz."""
    return np.linalg.matrix_rank(mat)

def matrix_inverse(mat: list) -> list:
    """Calcula a inversa de uma matriz."""
    return np.linalg.inv(mat).tolist()

def matrix_eigenvalues(mat: list) -> list:
    """Calcula os autovalores de uma matriz."""
    return np.linalg.eigvals(mat).tolist()

def matrix_eigenvectors(mat: list) -> list:
    """Calcula os autovetores de uma matriz."""
    return np.linalg.eig(mat)[1].tolist()

def matrix_trace(mat: list) -> float:
    """Calcula o traço de uma matriz."""
    return np.trace(mat)

def matrix_norm_fro(mat: list) -> float:
    """Calcula a norma de Frobenius de uma matriz."""
    return np.linalg.norm(mat, 'fro')

def matrix_norm_inf(mat: list) -> float:
    """Calcula a norma do infinito de uma matriz."""
    return np.linalg.norm(mat, np.inf)

def matrix_condition_number(mat: list) -> float:
    """Calcula o número de condição de uma matriz."""
    return np.linalg.cond(mat)

def matrix_pinv(mat: list) -> list:
    """Calcula a pseudoinversa de uma matriz."""
    return np.linalg.pinv(mat).tolist()

def solve_linear_system(A: list, b: list) -> list:
    """Resolve um sistema de equações lineares Ax=b."""
    return np.linalg.solve(A, b).tolist()

def cholesky_decomposition(mat: list) -> list:
    """Realiza a decomposição de Cholesky."""
    return np.linalg.cholesky(mat).tolist()

def qr_decomposition(mat: list) -> Tuple[list, list]:
    """Realiza a decomposição QR."""
    Q, R = np.linalg.qr(mat)
    return Q.tolist(), R.tolist()

def svd_u(mat: list) -> list:
    """Retorna a matriz U da SVD."""
    return np.linalg.svd(mat)[0].tolist()

def svd_s(mat: list) -> list:
    """Retorna os valores singulares da SVD."""
    return np.linalg.svd(mat)[1].tolist()
