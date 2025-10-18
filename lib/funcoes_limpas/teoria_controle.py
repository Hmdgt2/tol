# lib/funcoes_analiticas/teoria_controle.py
import numpy as np
from typing import List, Callable
from scipy import linalg

def controllability_matrix(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
    """Matriz de controlabilidade."""
    A_arr, B_arr = np.array(A), np.array(B)
    n = A_arr.shape[0]
    
    # C = [B, AB, A²B, ..., A^(n-1)B]
    C = B_arr.copy()
    current = B_arr
    
    for i in range(1, n):
        current = A_arr @ current
        C = np.hstack([C, current])
    
    return C.tolist()

def observability_matrix(A: List[List[float]], C: List[List[float]]) -> List[List[float]]:
    """Matriz de observabilidade."""
    A_arr, C_arr = np.array(A), np.array(C)
    n = A_arr.shape[0]
    
    # O = [C, CA, CA², ..., CA^(n-1)]^T
    O = C_arr.copy()
    current = C_arr
    
    for i in range(1, n):
        current = current @ A_arr
        O = np.vstack([O, current])
    
    return O.tolist()

def lyapunov_equation_solution(A: List[List[float]], Q: List[List[float]]) -> List[List[float]]:
    """Solução da equação de Lyapunov AᵀP + PA = -Q."""
    A_arr, Q_arr = np.array(A), np.array(Q)
    
    try:
        # Resolver usando scipy
        P = linalg.solve_continuous_lyapunov(A_arr.T, -Q_arr)
        return P.tolist()
    except:
        return [[0.0] * len(A[0]) for _ in range(len(A))]

def kalman_filter_gain(A: List[List[float]], 
                      C: List[List[float]], 
                      Q: List[List[float]], 
                      R: List[List[float]]) -> List[List[float]]:
    """Ganho do filtro de Kalman."""
    try:
        # Equação de Riccati simplificada
        A_arr, C_arr = np.array(A), np.array(C)
        Q_arr, R_arr = np.array(Q), np.array(R)
        
        # P = APAᵀ + Q
        P = A_arr @ A_arr.T + Q_arr
        
        # K = PCᵀ(CPCᵀ + R)⁻¹
        K = P @ C_arr.T @ linalg.inv(C_arr @ P @ C_arr.T + R_arr)
        return K.tolist()
    except:
        return [[0.0] * len(C[0]) for _ in range(len(A))]
