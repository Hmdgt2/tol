# lib/funcoes_analiticas/conjuntos.py
from sympy import isprime
from typing import List, Set


# ============================================================
# Contagem de elementos
# ============================================================

def count_even(lst: List[int]) -> int:
    """Conta os números pares em uma lista."""
    return sum(1 for x in lst if x % 2 == 0)


def count_odd(lst: List[int]) -> int:
    """Conta os números ímpares em uma lista."""
    return sum(1 for x in lst if x % 2 == 1)


def count_prime(lst: List[int]) -> int:
    """Conta os números primos em uma lista."""
    return sum(1 for x in lst if isprime(x))


def unique_count(lst: List[int]) -> int:
    """Conta o número de elementos únicos em uma lista."""
    return len(set(lst))


# ============================================================
# Operações com conjuntos
# ============================================================

def intersection(lst1: List[int], lst2: List[int]) -> List[int]:
    """Retorna os elementos em comum entre duas listas."""
    return list(set(lst1) & set(lst2))


def union(lst1: List[int], lst2: List[int]) -> List[int]:
    """Retorna a união de elementos de duas listas."""
    return list(set(lst1) | set(lst2))


# ============================================================
# Funções especiais
# ============================================================

def mirror_count(lst: List[int], total: int = 50) -> int:
    """Conta os números que têm um 'espelho' na lista (e.g., total - x)."""
    return sum(1 for x in lst if (total - x) in lst)


def pair_sum_count(lst: List[int], target: int) -> int:
    """Conta os pares de números que somam um valor alvo."""
    return sum(1 for i in range(len(lst)) for j in range(i + 1, len(lst)) if lst[i] + lst[j] == target)
