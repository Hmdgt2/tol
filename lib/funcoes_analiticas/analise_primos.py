# lib/funcoes_analiticas/analise_primos.py

from sympy import isprime, nextprime
import numpy as np
from typing import List


# ============================================================
# Filtragem e contagem
# ============================================================

def primes_in_list(lst: List[int]) -> List[int]:
    """Filtra e retorna os números primos de uma lista."""
    return [x for x in lst if isprime(x)]


def count_primes(lst: List[int]) -> int:
    """Conta a quantidade de números primos em uma lista."""
    return len(primes_in_list(lst))


def count_primes_below(lst: List[int], limit: int) -> int:
    """Conta os primos abaixo de um limite."""
    return len([x for x in primes_in_list(lst) if x < limit])


def count_primes_above(lst: List[int], limit: int) -> int:
    """Conta os primos acima de um limite."""
    return len([x for x in primes_in_list(lst) if x > limit])


# ============================================================
# Estatísticas dos primos
# ============================================================

def sum_primes(lst: List[int]) -> float:
    """Calcula a soma dos números primos em uma lista."""
    return sum(primes_in_list(lst))


def mean_primes(lst: List[int]) -> float:
    """Calcula a média dos números primos em uma lista."""
    primes = primes_in_list(lst)
    return np.mean(primes) if primes else 0


def median_primes(lst: List[int]) -> float:
    """Calcula a mediana dos números primos em uma lista."""
    primes = primes_in_list(lst)
    return np.median(primes) if primes else 0


def max_prime(lst: List[int]) -> int:
    """Retorna o maior número primo em uma lista."""
    primes = primes_in_list(lst)
    return max(primes) if primes else 0


def min_prime(lst: List[int]) -> int:
    """Retorna o menor número primo em uma lista."""
    primes = primes_in_list(lst)
    return min(primes) if primes else 0


def range_primes(lst: List[int]) -> int:
    """Calcula a diferença entre o maior e o menor primo."""
    primes = primes_in_list(lst)
    return max(primes) - min(primes) if primes else 0


def prime_near_mean(lst: List[int]) -> int:
    """Retorna o número primo mais próximo da média da lista."""
    primes = primes_in_list(lst)
    if not primes:
        return 0
    mean_val = np.mean(lst)
    return min(primes, key=lambda x: abs(x - mean_val))


# ============================================================
# Operações com primos
# ============================================================

def next_primes(lst: List[int]) -> List[int]:
    """Retorna o próximo número primo de cada elemento."""
    return [nextprime(x) for x in lst]


def prime_gaps(lst: List[int]) -> List[int]:
    """Calcula os gaps (diferenças) entre números primos consecutivos."""
    primes = primes_in_list(lst)
    return [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]


def sum_prime_gaps(lst: List[int]) -> int:
    """Calcula a soma dos gaps entre números primos."""
    return sum(prime_gaps(lst))


def odd_primes(lst: List[int]) -> List[int]:
    """Retorna os números primos ímpares de uma lista."""
    return [x for x in primes_in_list(lst) if x % 2 != 0]


def square_primes(lst: List[int]) -> List[int]:
    """Retorna o quadrado de cada número primo em uma lista."""
    return [x ** 2 for x in primes_in_list(lst)]


# ============================================================
# Representações
# ============================================================

def prime_binary(lst: List[int]) -> List[int]:
    """Cria uma representação binária (1=primo, 0=não primo)."""
    return [1 if isprime(x) else 0 for x in lst]
