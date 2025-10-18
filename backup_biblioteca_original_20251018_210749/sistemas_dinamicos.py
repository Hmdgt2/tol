# lib/funcoes_analiticas/sistemas_dinamicos.py
import numpy as np
from typing import List, Callable
from scipy import integrate

def rossler_attractor(a: float = 0.2, b: float = 0.2, c: float = 5.7, steps: int = 1000) -> List[List[float]]:
    """Atractor de Rössler - sistema caótico."""
    def rossler_deriv(t, state):
        x, y, z = state
        return [-y - z, x + a * y, b + z * (x - c)]
    
    solution = integrate.solve_ivp(rossler_deriv, [0, 100], [0.1, 0.1, 0.1], 
                                  t_eval=np.linspace(0, 100, steps))
    return solution.y.T.tolist()

def lyapunov_spectrum(system_func: Callable, initial: List[float], steps: int = 1000) -> List[float]:
    """Espectro de Lyapunov para sistemas dinâmicos."""
    # Implementação simplificada
    trajectory = [initial]
    jacobians = []
    
    for i in range(steps - 1):
        current = trajectory[-1]
        # Aproximação numérica do Jacobiano
        eps = 1e-8
        jac = np.zeros((len(initial), len(initial)))
        for j in range(len(initial)):
            perturbed = current.copy()
            perturbed[j] += eps
            jac[:, j] = (np.array(system_func(perturbed)) - np.array(system_func(current))) / eps
        jacobians.append(jac)
        trajectory.append(system_func(current))
    
    # Cálculo dos expoentes de Lyapunov (simplificado)
    if jacobians:
        Q = np.eye(len(initial))
        lyapunovs = np.zeros(len(initial))
        
        for jac in jacobians:
            Q, R = np.linalg.qr(jac @ Q)
            lyapunovs += np.log(np.abs(np.diag(R)))
        
        return (lyapunovs / len(jacobians)).tolist()
    return [0.0] * len(initial)

def recurrence_plot(series: List[float], threshold: float = 0.1) -> List[List[int]]:
    """Plot de recorrência para análise de sistemas dinâmicos."""
    n = len(series)
    plot = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if abs(series[i] - series[j]) < threshold:
                plot[i][j] = 1
    return plot

def permutation_entropy(series: List[float], order: int = 3, delay: int = 1) -> float:
    """Entropia de permutação para análise de complexidade."""
    n = len(series)
    if n < order:
        return 0.0
    
    # Gerar todas as permutações possíveis
    from itertools import permutations
    perms = list(permutations(range(order)))
    count = {p: 0 for p in perms}
    
    # Contar padrões de permutação
    for i in range(n - (order - 1) * delay):
        # Extrair padrão
        pattern = [series[i + j * delay] for j in range(order)]
        # Ordenar para obter permutação
        sorted_indices = tuple(np.argsort(pattern))
        count[sorted_indices] += 1
    
    # Calcular entropia
    total = sum(count.values())
    if total == 0:
        return 0.0
    
    entropy = 0.0
    for c in count.values():
        if c > 0:
            p = c / total
            entropy -= p * np.log(p)
    
    return entropy / np.log(len(perms))  # Normalizar
