from typing import List, Set
from lib.funcoes_analiticas.estatisticas import count_even, count_odd, count_prime

# ============================================================
# Operações com conjuntos
# ============================================================

def unique_count(lst: List[int]) -> int:
    """Conta o número de elementos únicos em uma lista."""
    return len(set(lst))

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
