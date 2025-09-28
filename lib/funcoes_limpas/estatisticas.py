
from typing import List

def unique_count(lst: List[int]) -> int:
    'Conta o número de elementos únicos em uma lista.'
    return len(set(lst))

def intersection(lst1: List[int], lst2: List[int]) -> List[int]:
    'Retorna os elementos em comum entre duas listas.'
    return list((set(lst1) & set(lst2)))

def union(lst1: List[int], lst2: List[int]) -> List[int]:
    'Retorna a união de elementos de duas listas.'
    return list((set(lst1) | set(lst2)))

def difference(lst1: List[int], lst2: List[int]) -> List[int]:
    'Retorna os elementos de lst1 que não estão em lst2.'
    return list((set(lst1) - set(lst2)))

def symmetric_difference(lst1: List[int], lst2: List[int]) -> List[int]:
    'Retorna os elementos que estão em lst1 ou lst2, mas não em ambos.'
    return list((set(lst1) ^ set(lst2)))

def mirror_count(lst: List[int], total: int=50) -> int:
    "Conta os números que têm um 'espelho' na lista (e.g., total - x)."
    return sum((1 for x in lst if ((total - x) in lst)))

def pair_sum_count(lst: List[int], target: int) -> int:
    'Conta os pares de números que somam um valor alvo.'
    return sum((1 for i in range(len(lst)) for j in range((i + 1), len(lst)) if ((lst[i] + lst[j]) == target)))

def pair_product_count(lst: List[int], target: int) -> int:
    'Conta os pares de números que multiplicados dão um valor alvo.'
    return sum((1 for i in range(len(lst)) for j in range((i + 1), len(lst)) if ((lst[i] * lst[j]) == target)))

def count_even(lst: List[int]) -> int:
    'Conta números pares na lista.'
    return sum((1 for x in lst if ((x % 2) == 0)))

def count_odd(lst: List[int]) -> int:
    'Conta números ímpares na lista.'
    return sum((1 for x in lst if ((x % 2) == 1)))

def iqr_outliers(lst: List[float]) -> List[float]:
    '\n    Detecta outliers usando o método do Intervalo Interquartil (IQR).\n    \n    Args:\n        lst (List[float]): Lista de valores.\n    \n    Returns:\n        List[float]: Lista de valores considerados outliers.\n    '
    (q1, q3) = np.percentile(lst, [25, 75])
    iqr = (q3 - q1)
    return [x for x in lst if ((x < (q1 - (1.5 * iqr))) or (x > (q3 + (1.5 * iqr))))]
