# lib/funcoes_analiticas/gpu_computing.py
try:
    import cupy as cp
    import cupyx.scipy.fft
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    import numpy as cp
from typing import List, Dict

def cupy_gpu_analysis(seq: List[float]) -> Dict:
    """Análise acelerada por GPU usando CuPy."""
    if not CUPY_AVAILABLE:
        return {'gpu_analysis': 'cupy_not_available'}
    
    # Transfere dados para GPU
    gpu_array = cp.asarray(seq, dtype=cp.float64)
    
    # Operações na GPU
    gpu_operations = {
        'gpu_fft': cp.abs(cupyx.scipy.fft.fft(gpu_array)).get().tolist(),
        'gpu_convolution': cp.convolve(gpu_array, cp.ones(5)/5, mode='same').get().tolist(),
        'gpu_matrix_ops': _cupy_matrix_operations(gpu_array),
        'gpu_linear_algebra': _cupy_linear_algebra(gpu_array)
    }
    
    # Benchmark de performance
    import time
    start = time.time()
    _ = cp.fft.fft(gpu_array)
    gpu_time = time.time() - start
    
    # Comparação com CPU
    cpu_array = np.array(seq)
    start = time.time()
    _ = np.fft.fft(cpu_array)
    cpu_time = time.time() - start
    
    return {
        'gpu_operations': gpu_operations,
        'performance_metrics': {
            'gpu_speedup': cpu_time / gpu_time if gpu_time > 0 else 1.0,
            'memory_bandwidth': 'high' if len(seq) > 10000 else 'moderate',
            'gpu_utilization': True
        },
        'cupy_features': ['GPU_FFT', 'CUDA_kernels', 'memory_pooling']
    }

def _cupy_matrix_operations(gpu_array):
    """Operações matriciais na GPU."""
    n = len(gpu_array)
    # Cria matriz de Toeplitz
    toeplitz_matrix = cp.zeros((n, n))
    for i in range(n):
        toeplitz_matrix[i, :] = cp.roll(gpu_array, i)
    
    eigenvalues = cp.linalg.eigvals(toeplitz_matrix)
    
    return {
        'matrix_rank': int(cp.linalg.matrix_rank(toeplitz_matrix)),
        'largest_eigenvalue': float(cp.abs(eigenvalues).max()),
        'condition_number': float(cp.linalg.cond(toeplitz_matrix))
    }

def _cupy_linear_algebra(gpu_array):
    """Álgebra linear acelerada por GPU."""
    # Decomposição QR na GPU
    Q, R = cp.linalg.qr(gpu_array.reshape(-1, 1))
    
    return {
        'qr_decomposition': {
            'Q_norm': float(cp.linalg.norm(Q)),
            'R_diagonal': float(R[0, 0])
        },
        'gpu_memory_usage': f"{gpu_array.nbytes / 1e6:.2f} MB"
    }
