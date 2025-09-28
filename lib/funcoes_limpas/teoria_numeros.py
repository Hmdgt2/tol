
from sympy.ntheory import factorint, isprime, primerange, nextprime, prevprime, totient, mobius
import sympy as sp
from typing import List, Dict

def euler_totient(n: int) -> int:
    'Calcula a função totiente de Euler.'
    return totient(n)

def factor_integer(n: int) -> Dict[(int, int)]:
    'Fatora um número em seus fatores primos.'
    return factorint(n)

def prime_factors(n: int) -> List[int]:
    'Retorna os fatores primos únicos de um número.'
    return list(factorint(n).keys())

def prime_factor_count(n: int) -> int:
    'Retorna o número de fatores primos únicos de um número.'
    return len(factorint(n))

def largest_prime_factor(n: int) -> int:
    'Retorna o maior fator primo de um número.'
    return max(factorint(n).keys())

def smallest_prime_factor(n: int) -> int:
    'Retorna o menor fator primo de um número.'
    return min(factorint(n).keys())

def gcd_list(lst: List[int]) -> int:
    'Calcula o Máximo Divisor Comum (MDC) de uma lista de números.'
    return sp.gcd(*lst)

def lcm_list(lst: List[int]) -> int:
    'Calcula o Mínimo Múltiplo Comum (MMC) de uma lista de números.'
    return sp.lcm(*lst)

def check_prime(n: int) -> bool:
    'Verifica se um número é primo.'
    return isprime(n)

def count_primes_upto(n: int) -> int:
    'Conta o número de primos até n.'
    return len(list(primerange(1, (n + 1))))

def next_prime_num(n: int) -> int:
    'Encontra o próximo número primo após n.'
    return int(nextprime(n))

def prev_prime_num(n: int) -> int:
    'Encontra o número primo anterior a n.'
    return int(prevprime(n))

def generate_primes(n: int) -> List[int]:
    'Gera uma lista de primos até n.'
    return list(primerange(1, n))

def fibonacci_num(n: int) -> int:
    'Retorna o n-ésimo número de Fibonacci.'
    return sp.fibonacci(n)

def lucas_num(n: int) -> int:
    'Retorna o n-ésimo número de Lucas.'
    return sp.lucas(n)

def catalan_num(n: int) -> int:
    'Retorna o n-ésimo número de Catalan.'
    return sp.catalan(n)
