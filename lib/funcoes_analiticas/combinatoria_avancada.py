# lib/funcoes_analiticas/combinatoria_avancada.py
from itertools import combinations, permutations, product, accumulate
from functools import reduce
from typing import List, Callable, Tuple, Dict, Any
import operator
import math
from .aritmetica import prod_list
import random
import numpy as np
from itertools import combinations, permutations
from scipy.special import comb, perm

def combinations_sum(lst: list, r: int = 2) -> list:
    """Calcula a soma de todas as combinações de r elementos da lista."""
    return [sum(c) for c in combinations(lst, r)]

def permutations_sum(lst: list, r: int = 2) -> list:
    """Calcula a soma de todas as permutações de r elementos da lista."""
    return [sum(p) for p in permutations(lst, r)]

def reduce_sum(lst: list) -> float:
    """Calcula a soma de uma lista usando reduce."""
    return reduce(operator.add, lst)

def reduce_prod(lst: list) -> float:
    """Calcula o produto de uma lista usando reduce."""
    return reduce(operator.mul, lst)

def reduce_max(lst: list) -> float:
    """Encontra o máximo de uma lista usando reduce."""
    return reduce(max, lst)

def prod_ratio(lst: list) -> float:
    """Calcula o produto das proporções entre elementos consecutivos."""
    ratios = [lst[i + 1] / lst[i] if lst[i] != 0 else 1 for i in range(len(lst) - 1)]
    return prod_list(ratios)

def conditional_permutations(lst: list, condition: Callable) -> List[Tuple]:
    """Retorna permutações que satisfazem uma condição."""
    return [p for p in permutations(lst) if all(condition(i) for i in p)]

def combinations_with_sum(lst: list, target: float) -> List[Tuple]:
    """Retorna combinações de soma alvo."""
    return [c for r in range(1, len(lst) + 1) for c in combinations(lst, r) if sum(c) == target]

def count_combinations_with_sum(lst: list, target: float) -> int:
    """Conta as combinações de soma alvo."""
    return len(combinations_with_sum(lst, target))

def permuted_sums(lst: list) -> list:
    """Calcula a soma de todas as permutações de uma lista."""
    return [sum(p) for p in permutations(lst)]

# Soma de combinações de 2 elementos
def sum_combinations2(lst: list) -> list:
    """Calcula a soma de todas as combinações de 2 elementos."""
    return [sum(c) for c in combinations(lst, 2)]

# Soma de combinações de 3 elementos
def sum_combinations3(lst: list) -> list:
    """Calcula a soma de todas as combinações de 3 elementos."""
    return [sum(c) for c in combinations(lst, 3)]

# Soma de todas as permutações
def sum_permutations(lst: list) -> list:
    """Calcula a soma de todas as permutações de uma lista."""
    return [sum(p) for p in permutations(lst)]

# Máximo de permutações
def max_permutation_sum(lst: list) -> float:
    """Calcula a soma máxima de todas as permutações de uma lista."""
    return max([sum(p) for p in permutations(lst)])

# Mínimo de permutações
def min_permutation_sum(lst: list) -> float:
    """Calcula a soma mínima de todas as permutações de uma lista."""
    return min([sum(p) for p in permutations(lst)])

# Média de combinações
def mean_combinations(lst: list, k: int = 2) -> float:
    """Calcula a média das somas de todas as combinações de k elementos."""
    return np.mean([sum(c) for c in combinations(lst, k)])

# Diferença máxima de combinações
def max_diff_combinations(lst: list, k: int = 2) -> float:
    """Calcula a diferença entre a soma máxima e a mínima das combinações."""
    sums = [sum(c) for c in combinations(lst, k)]
    return max(sums) - min(sums)

# Produto de combinações
def prod_combinations(lst: list, k: int = 2) -> float:
    """Calcula o produto das somas de todas as combinações."""
    res = 1
    for c in combinations(lst, k):
        res *= sum(c)
    return res

# Soma de quadrados das combinações
def sumsq_combinations(lst: list, k: int = 2) -> list:
    """Calcula a soma dos quadrados de todas as combinações."""
    return [sum(c)**2 for c in combinations(lst, k)]

# Combinações avançadas
def combination_count(n: int, k: int) -> int:
    """Calcula o número de combinações."""
    return comb(n, k, exact=True)

def permutation_count(n: int, k: int) -> int:
    """Calcula o número de permutações."""
    return perm(n, k, exact=True)
