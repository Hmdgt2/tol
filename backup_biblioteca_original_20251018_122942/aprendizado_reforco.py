# lib/funcoes_analiticas/aprendizado_reforco.py
import numpy as np
from typing import List, Callable
import random

def q_learning_update(q_table: List[List[float]], 
                     state: int, 
                     action: int, 
                     reward: float, 
                     next_state: int, 
                     alpha: float = 0.1, 
                     gamma: float = 0.9) -> List[List[float]]:
    """Atualização Q-learning."""
    if (state < len(q_table) and action < len(q_table[0]) and 
        next_state < len(q_table)):
        best_next = max(q_table[next_state]) if q_table[next_state] else 0
        q_table[state][action] += alpha * (
            reward + gamma * best_next - q_table[state][action]
        )
    return q_table

def policy_gradient_log_prob(policy: Callable[[List[float]], List[float]], 
                           state: List[float], 
                           action: int) -> float:
    """Log-probabilidade de ação sob política."""
    action_probs = policy(state)
    if 0 <= action < len(action_probs) and action_probs[action] > 0:
        return np.log(action_probs[action])
    return -np.inf

def temporal_difference_error(v_values: List[float], 
                            state: int, 
                            next_state: int, 
                            reward: float, 
                            gamma: float = 0.9) -> float:
    """Erro de diferença temporal."""
    if (state < len(v_values) and next_state < len(v_values)):
        return reward + gamma * v_values[next_state] - v_values[state]
    return 0.0

def eligibility_traces_update(eligibility: List[float], 
                            state: int, 
                            lambda_val: float = 0.8, 
                            gamma: float = 0.9) -> List[float]:
    """Atualização de traços de elegibilidade."""
    if state < len(eligibility):
        # Decaimento e incremento
        eligibility = [e * gamma * lambda_val for e in eligibility]
        eligibility[state] += 1
    return eligibility

def bellman_optimality_residual(q_values: List[List[float]], 
                               rewards: List[List[float]], 
                               gamma: float = 0.9) -> float:
    """Resíduo da equação de otimalidade de Bellman."""
    if not q_values or not rewards:
        return 0.0
    
    residual = 0.0
    for state in range(len(q_values)):
        for action in range(len(q_values[state])):
            if (state < len(rewards) and action < len(rewards[state])):
                max_next = max(q_values[state]) if q_values[state] else 0
                bellman_value = rewards[state][action] + gamma * max_next
                residual += abs(q_values[state][action] - bellman_value)
    
    return residual
