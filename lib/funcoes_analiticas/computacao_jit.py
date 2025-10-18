# lib/funcoes_analiticas/computacao_jit.py
from numba import jit, njit, vectorize
import numba
import numpy as np
from typing import List, Dict

@njit(fastmath=True, parallel=True)
def numba_optimized_operations(arr):
    """Operações matemáticas otimizadas com Numba."""
    n = len(arr)
    result = np.zeros(n)
    
    # Loop paralelizado e otimizado
    for i in numba.prange(n):
        # Operações complexas otimizadas
        if i >= 2:
            result[i] = (arr[i] + arr[i-1] * 0.5 + arr[i-2] * 0.25) * np.sin(arr[i])
        else:
            result[i] = arr[i]
    
    return result

@vectorize(['float64(float64)'], nopython=True)
def numba_vectorized_transform(x):
    """Transformação vetorizada com Numba."""
    if x > 0:
        return np.log1p(x) * np.cos(x)
    else:
        return np.exp(x) * np.sin(x)

def jit_compiled_analysis(seq: List[float]) -> Dict:
    """Análise com compilação Just-In-Time para máxima performance."""
    arr = np.array(seq, dtype=np.float64)
    
    # Benchmark vs NumPy puro
    import time
    
    # Numba
    start = time.time()
    numba_result = numba_optimized_operations(arr)
    numba_time = time.time() - start
    
    # NumPy equivalente
    start = time.time()
    numpy_result = np.zeros(len(arr))
    for i in range(len(arr)):
        if i >= 2:
            numpy_result[i] = (arr[i] + arr[i-1] * 0.5 + arr[i-2] * 0.25) * np.sin(arr[i])
        else:
            numpy_result[i] = arr[i]
    numpy_time = time.time() - start
    
    # Transformação vetorizada
    vectorized_result = numba_vectorized_transform(arr)
    
    return {
        'numba_optimized': numba_result.tolist(),
        'vectorized_transform': vectorized_result.tolist(),
        'performance_speedup': numpy_time / numba_time if numba_time > 0 else 1.0,
        'compilation_advantage': 'enabled' if len(seq) > 100 else 'minimal',
        'numba_features': {
            'parallel': True,
            'fastmath': True,
            'vectorize': True
        }
    }
