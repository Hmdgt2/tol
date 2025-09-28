# lib/funcoes_analiticas/combinatoria_avancada.py

from itertools import combinations, permutations, product
from functools import reduce
from typing import List, Callable, Tuple
import operator
import numpy as np
from scipy.special import comb, perm, factorial
from .aritmetica import prod_list


# ============================================================
# Soma e produtos de combinações e permutações
# ============================================================

def combinations_sum(lst: List[float], r: int = 2) -> List[float]:
    """Soma todas as combinações de r elementos da lista."""
    return [sum(c) for c in combinations(lst, r)]


def permutations_sum(lst: List[float], r: int = 2) -> List[float]:
    """Soma todas as permutações de r elementos da lista."""
    return [sum(p) for p in permutations(lst, r)]


def sum_combinations2(lst: List[float]) -> List[float]:
    """Soma de todas as combinações de 2 elementos."""
    return [sum(c) for c in combinations(lst, 2)]


def sum_combinations3(lst: List[float]) -> List[float]:
    """Soma de todas as combinações de 3 elementos."""
    return [sum(c) for c in combinations(lst, 3)]


def sum_permutations2(lst: List[float]) -> List[float]:
    """Soma de todas as permutações de 2 elementos."""
    return [sum(p) for p in permutations(lst, 2)]


def prod_combinations2(lst: List[float]) -> float:
    """Produto das somas de todas as combinações de 2 elementos."""
    res = 1
    for c in combinations(lst, 2):
        res *= sum(c)
    return res


def prod_permutations2(lst: List[float]) -> float:
    """Produto das somas de todas as permutações de 2 elementos."""
    res = 1
    for p in permutations(lst, 2):
        res *= sum(p)
    return res


def max_diff_combinations(lst: List[float], k: int = 2) -> float:
    """Diferença entre a soma máxima e mínima das combinações."""
    sums = [sum(c) for c in combinations(lst, k)]
    return max(sums) - min(sums)


def mean_combinations2(lst: List[float]) -> float:
    """Média das somas de todas as combinações de 2 elementos."""
    return np.mean([sum(c) for c in combinations(lst, 2)])


# ============================================================
# Operações gerais com listas
# ============================================================

def reduce_sum(lst: List[float]) -> float:
    """Soma de uma lista usando reduce."""
    return reduce(operator.add, lst)


def reduce_prod(lst: List[float]) -> float:
    """Produto de uma lista usando reduce."""
    return reduce(operator.mul, lst)


def reduce_max(lst: List[float]) -> float:
    """Máximo de uma lista usando reduce."""
    return reduce(max, lst)


def prod_ratio(lst: List[float]) -> float:
    """Produto das proporções entre elementos consecutivos."""
    ratios = [lst[i + 1] / lst[i] if lst[i] != 0 else 1 for i in range(len(lst) - 1)]
    return prod_list(ratios)


# ============================================================
# Combinações condicionais
# ============================================================

def conditional_permutations(lst: List[float], condition: Callable) -> List[Tuple]:
    """Permutações que satisfazem uma condição."""
    return [p for p in permutations(lst) if all(condition(i) for i in p)]


def combinations_with_sum(lst: List[float], target: float) -> List[Tuple]:
    """Combinações cuja soma é igual ao valor alvo."""
    return [c for r in range(1, len(lst) + 1) for c in combinations(lst, r) if sum(c) == target]


def count_combinations_with_sum(lst: List[float], target: float) -> int:
    """Conta combinações cuja soma é igual ao valor alvo."""
    return len(combinations_with_sum(lst, target))


# ============================================================
# Produto cartesiano
# ============================================================

def product_sum(lst1: List[float], lst2: List[float]) -> List[float]:
    """Soma dos pares do produto cartesiano de duas listas."""
    return [sum(p) for p in product(lst1, lst2)]


def product_prod(lst1: List[float], lst2: List[float]) -> List[float]:
    """Produto dos pares do produto cartesiano de duas listas."""
    return [np.prod(p) for p in product(lst1, lst2)]


def product_sum_square(lst1: List[float], lst2: List[float]) -> List[float]:
    """Quadrado da soma de cada par do produto cartesiano."""
    return [sum(p)**2 for p in product(lst1, lst2)]


def product_prod_square(lst1: List[float], lst2: List[float]) -> List[float]:
    """Quadrado do produto de cada par do produto cartesiano."""
    return [np.prod(p)**2 for p in product(lst1, lst2)]


# ============================================================
# Contagem de combinações e permutações exatas
# ============================================================

def combination_count(n: int, k: int) -> int:
    """Número exato de combinações."""
    return int(comb(n, k, exact=True))


def permutation_count(n: int, k: int) -> int:
    """Número exato de permutações."""
    return int(perm(n, k, exact=True))


def factorial_list(lst: List[int]) -> List[int]:
    """Fatorial de cada elemento de uma lista."""
    return [int(factorial(x)) for x in lst]
