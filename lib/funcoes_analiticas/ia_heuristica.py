# lib/funcoes_analiticas/ia_heuristica.py
import random
import numpy as np
from typing import List, Callable, Dict, Any

def mutate_list(lst: list, mutation_rate: float = 0.1, max_val: int = 49) -> list:
    """Aplica mutação a uma lista, trocando elementos aleatoriamente."""
    return [x if random.random() > mutation_rate else random.randint(1, max_val) for x in lst]

def crossover_lists(lst1: list, lst2: list) -> list:
    """Combina duas listas em um ponto de cruzamento."""
    point = random.randint(1, len(lst1) - 1)
    return lst1[:point] + lst2[point:]

def fitness_sum(lst: list, target: float = 100) -> float:
    """Calcula o 'fitness' de uma lista com base em sua soma."""
    return -abs(sum(lst) - target)

def fitness_even_ratio(lst: list, target_ratio: float = 0.5) -> float:
    """Calcula o 'fitness' com base na proporção de números pares."""
    if not lst: return -1
    ratio = sum(1 for x in lst if x % 2 == 0) / len(lst)
    return -abs(ratio - target_ratio)

def select_best_population(population: List[list], fitness_func: Callable, k: int = 5) -> List[list]:
    """Seleciona a melhor parte de uma população com base em uma função de fitness."""
    scored = [(fitness_func(lst), lst) for lst in population]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [lst for _, lst in scored[:k]]

def combined_score(lst: list, heuristics: List[Callable]) -> float:
    """Combina o score de múltiplas heurísticas para uma lista."""
    return sum(h(lst) for h in heuristics)

def weighted_score(lst: list, heuristics: List[Callable], weights: List[float]) -> float:
    """Calcula o score combinado de heurísticas com pesos."""
    return sum(h(lst) * w for h, w in zip(heuristics, weights))

def rank_heuristics(lst: list, heuristics: List[Callable]) -> list:
    """Classifica heurísticas com base em seu desempenho em uma lista."""
    scores = [h(lst) for h in heuristics]
    return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

def generate_heuristic_from_library(lst: list, funcs: List[Callable]) -> Any:
    """Gera um valor a partir de uma heurística aleatória da biblioteca."""
    f = random.choice(funcs)
    return f(lst)

def integrated_heuristic_test(lst: list, heuristics: List[Callable]) -> List[Callable]:
    """Testa e retorna heurísticas ordenadas por score."""
    scores = [h(lst) for h in heuristics]
    ranked = np.argsort(scores)[::-1]
    return [heuristics[i] for i in ranked]

def top_k_integrated(lst: list, heuristics: List[Callable], k: int = 5) -> List[Callable]:
    """Retorna as top K heurísticas integradas."""
    ranked = integrated_heuristic_test(lst, heuristics)
    return ranked[:k]

def generate_new_combined_heuristic(heuristics: List[Callable], transforms: List[Callable]) -> Callable:
    """Gera uma nova heurística combinando uma função com uma transformação."""
    h = random.choice(heuristics)
    t = random.choice(transforms or [lambda x: x])
    return lambda x: h(t(x))

def stochastic_score(lst: list, heuristics: List[Callable], trials: int = 100) -> float:
    """Calcula o score estocástico de uma lista."""
    results = []
    for _ in range(trials):
        h = random.choice(heuristics)
        results.append(h(lst))
    return np.mean(results)

def combined_stochastic_score(lst: list, heuristics: List[Callable], weights: List[float] = None, trials: int = 100) -> float:
    """Calcula o score estocástico combinado com pesos."""
    results = []
    weights = weights or [1] * len(heuristics)
    for _ in range(trials):
        h = random.choice(heuristics)
        w = random.choice(weights)
        results.append(h(lst) * w)
    return np.mean(results)
