# lib/funcoes_analiticas/otimizacao_convexa.py
import numpy as np
from typing import List, Callable
from scipy import optimize

def convex_function_test(f: Callable[[float], float], 
                        domain: List[float], 
                        samples: int = 100) -> bool:
    """Testa se função é convexa."""
    x_vals = np.linspace(domain[0], domain[1], samples)
    
    for i in range(1, len(x_vals) - 1):
        x1, x2, x3 = x_vals[i-1], x_vals[i], x_vals[i+1]
        f1, f2, f3 = f(x1), f(x2), f(x3)
        
        # Teste de convexidade: f(x2) ≤ (f(x1) + f(x3))/2
        if f2 > (f1 + f3) / 2 + 1e-6:
            return False
    
    return True

def subgradient_method(f: Callable[[List[float]], float], 
                      subgrad: Callable[[List[float]], List[float]], 
                      x0: List[float], 
                      steps: int = 100) -> List[float]:
    """Método do subgradiente para otimização não-suave."""
    x = np.array(x0)
    best_x = x.copy()
    best_f = f(x)
    
    for k in range(steps):
        g = np.array(subgrad(x))
        step_size = 1.0 / (k + 1)
        x = x - step_size * g
        
        current_f = f(x)
        if current_f < best_f:
            best_f = current_f
            best_x = x.copy()
    
    return best_x.tolist()

def lagrange_duality(primal_obj: Callable, 
                    constraints: List[Callable], 
                    x0: List[float]) -> float:
    """Valor dual de problema de otimização."""
    # Função Lagrangeana simplificada
    def lagrangian(x, lambdas):
        penalty = sum(lambdas[i] * max(0, constraints[i](x)) 
                     for i in range(len(constraints)))
        return primal_obj(x) + penalty
    
    # Otimização sobre lambdas (simplificado)
    best_dual = -np.inf
    for lambda_val in [0.1, 1.0, 10.0]:
        lambdas = [lambda_val] * len(constraints)
        dual_val = -lagrangian(x0, lambdas)  # Negativo para minimização
        best_dual = max(best_dual, dual_val)
    
    return best_dual

def barrier_method(f: Callable[[List[float]], float], 
                  constraints: List[Callable], 
                  x0: List[float], 
                  mu: float = 10.0) -> List[float]:
    """Método de barreira para otimização com restrições."""
    def barrier_function(x):
        barrier = 0.0
        for constr in constraints:
            if constr(x) >= 0:
                barrier += -np.log(-constr(x))
            else:
                barrier += 1e10  # Penalidade grande
        return f(x) + mu * barrier
    
    result = optimize.minimize(barrier_function, x0, method='BFGS')
    return result.x.tolist() if result.success else x0
