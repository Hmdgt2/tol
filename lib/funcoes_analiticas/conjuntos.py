# lib/funcoes_analiticas/conjuntos.py
from sympy import isprime
from typing import List

def count_even(lst: list) -> int:
    """Conta os números pares em uma lista."""
    return sum(1 for x in lst if x % 2 == 0)

def count_odd(lst: list) -> int:
    """Conta os números ímpares em uma lista."""
    return sum(1 for x in lst if x % 2 == 1)

def count_prime(lst: list) -> int:
    """Conta os números primos em uma lista."""
    return sum(1 for x in lst if isprime(x))

def unique_count(lst: list) -> int:
    """Conta o número de elementos únicos em uma lista."""
    return len(set(lst))

def intersection(lst1: list, lst2: list) -> list:
    """Retorna os elementos em comum entre duas listas."""
    return list(set(lst1) & set(lst2))

def union(lst1: list, lst2: list) -> list:
    """Retorna a união de elementos de duas listas."""
    return list(set(lst1) | set(lst2))

def mirror_count(lst: list, total: int = 50) -> int:
    """Conta os números que têm um 'espelho' na lista (e.g., 50-x)."""
    return sum(1 for x in lst if (total - x) in lst)

def pair_sum_count(lst: list, target: int) -> int:
    """Conta os pares de números que somam um valor alvo."""
    return sum(1 for i in range(len(lst)) for j in range(i + 1, len(lst)) if lst[i] + lst[j] == target)
