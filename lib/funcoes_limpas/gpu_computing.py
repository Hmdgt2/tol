
try:
    import cupy as cp
    import cupyx.scipy.fft
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    import numpy as cp
from typing import List, Dict


def _cupy_matrix_operations(gpu_array):
    'Operações matriciais na GPU.'
    n = len(gpu_array)
    toeplitz_matrix = cp.zeros((n, n))
    for i in range(n):
        toeplitz_matrix[(i, :)] = cp.roll(gpu_array, i)
    eigenvalues = cp.linalg.eigvals(toeplitz_matrix)
    return {'matrix_rank': int(cp.linalg.matrix_rank(toeplitz_matrix)), 'largest_eigenvalue': float(cp.abs(eigenvalues).max()), 'condition_number': float(cp.linalg.cond(toeplitz_matrix))}


def _cupy_linear_algebra(gpu_array):
    'Álgebra linear acelerada por GPU.'
    (Q, R) = cp.linalg.qr(gpu_array.reshape((- 1), 1))
    return {'qr_decomposition': {'Q_norm': float(cp.linalg.norm(Q)), 'R_diagonal': float(R[(0, 0)])}, 'gpu_memory_usage': f'{(gpu_array.nbytes / 1000000.0):.2f} MB'}

