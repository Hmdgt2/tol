# lib/funcoes_analiticas/analise_primos.py
from sympy import isprime, primerange, nextprime
import numpy as np
from typing import List

def primes_in_list(lst: list) -> list:
    """Filtra e retorna os números primos de uma lista."""
    return [x for x in lst if isprime(x)]

def count_primes(lst: list) -> int:
    """Conta a quantidade de números primos em uma lista."""
    return len(primes_in_list(lst))

def next_primes(lst: list) -> list:
    """Retorna o próximo número primo de cada elemento."""
    return [nextprime(x) for x in lst]

def prime_gaps(lst: list) -> list:
    """Calcula os gaps (diferenças) entre números primos consecutivos."""
    primes = primes_in_list(lst)
    return [primes[i + 1] - primes[i] for i in range(len(primes) - 1)]

def sum_primes(lst: list) -> float:
    """Calcula a soma dos números primos em uma lista."""
    return sum(primes_in_list(lst))

def mean_primes(lst: list) -> float:
    """Calcula a média dos números primos em uma lista."""
    primes = primes_in_list(lst)
    return np.mean(primes) if primes else 0

def median_primes(lst: list) -> float:
    """Calcula a mediana dos números primos em uma lista."""
    primes = primes_in_list(lst)
    return np.median(primes) if primes else 0

def max_prime(lst: list) -> float:
    """Retorna o maior número primo em uma lista."""
    primes = primes_in_list(lst)
    return max(primes) if primes else 0

def min_prime(lst: list) -> float:
    """Retorna o menor número primo em uma lista."""
    primes = primes_in_list(lst)
    return min(primes) if primes else 0

def odd_primes(lst: list) -> list:
    """Retorna os números primos ímpares de uma lista."""
    return [x for x in primes_in_list(lst) if x % 2 != 0]

def square_primes(lst: list) -> list:
    """Retorna o quadrado de cada número primo em uma lista."""
    return [x ** 2 for x in primes_in_list(lst)]

def prime_near_mean(lst: list) -> float:
    """Retorna o número primo mais próximo da média da lista."""
    primes = primes_in_list(lst)
    if not primes: return 0
    mean_val = np.mean(lst)
    return min(primes, key=lambda x: abs(x - mean_val))

def prime_binary(lst: list) -> list:
    """Cria uma representação binária (1=primo, 0=não primo)."""
    return [1 if isprime(x) else 0 for x in lst]

def sum_prime_gaps(lst: list) -> float:
    """Calcula a soma dos gaps entre números primos."""
    return sum(prime_gaps(lst))

def range_primes(lst: list) -> float:
    """Calcula a diferença entre o maior e o menor primo."""
    primes = primes_in_list(lst)
    return max(primes) - min(primes) if primes else 0

def count_primes_below(lst: list, limit: int) -> int:
    """Conta os primos abaixo de um limite."""
    return len([x for x in primes_in_list(lst) if x < limit])

def count_primes_above(lst: list, limit: int) -> int:
    """Conta os primos acima de um limite."""
    return len([x for x in primes_in_list(lst) if x > limit])
