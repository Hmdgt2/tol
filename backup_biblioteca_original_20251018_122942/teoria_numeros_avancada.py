# lib/funcoes_analiticas/teoria_numeros_avancada.py
import numpy as np
from typing import List
from sympy import factorint, isprime, primerange
import math

# ============================================================
# Funções Aritméticas Avançadas
# ============================================================

def divisor_sigma(n: int, k: int = 1) -> int:
    """Função sigma σ_k(n) - soma das k-ésimas potências dos divisores."""
    factors = factorint(n)
    total = 1
    for p, exp in factors.items():
        total *= (p**(k*(exp+1)) - 1) // (p**k - 1) if k != 0 else (exp + 1)
    return total

def euler_phi(n: int) -> int:
    """Função totiente de Euler φ(n)."""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def mobius_function(n: int) -> int:
    """Função Möbius μ(n)."""
    if n == 1:
        return 1
    factors = factorint(n)
    if any(exp > 1 for exp in factors.values()):
        return 0
    return -1 if len(factors) % 2 == 1 else 1

def liouville_function(n: int) -> int:
    """Função de Liouville λ(n)."""
    factors = factorint(n)
    total_exp = sum(factors.values())
    return 1 if total_exp % 2 == 0 else -1

# ============================================================
# Sequências Especiais
# ============================================================

def perfect_numbers_up_to(limit: int) -> List[int]:
    """Números perfeitos até o limite."""
    return [n for n in range(2, limit+1) if divisor_sigma(n) - n == n]

def amicable_numbers_up_to(limit: int) -> List[tuple]:
    """Pares de números amigáveis."""
    result = []
    for a in range(2, limit+1):
        b = divisor_sigma(a) - a
        if a < b <= limit and divisor_sigma(b) - b == a:
            result.append((a, b))
    return result

def abundant_numbers(lst: List[int]) -> List[int]:
    """Números abundantes na lista."""
    return [n for n in lst if divisor_sigma(n) - n > n]

def deficient_numbers(lst: List[int]) -> List[int]:
    """Números deficientes na lista."""
    return [n for n in lst if divisor_sigma(n) - n < n]

# ============================================================
# Partições e Combinações
# ============================================================

def partition_function(n: int) -> int:
    """Função de partição p(n)."""
    if n == 0:
        return 1
    partitions = [0] * (n + 1)
    partitions[0] = 1
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            partitions[j] += partitions[j - i]
    return partitions[n]

def compositions_count(n: int, k: int) -> int:
    """Número de composições de n em k partes."""
    return math.comb(n - 1, k - 1) if 1 <= k <= n else 0

# ============================================================
# Congruências e Resíduos
# ============================================================

def quadratic_residues(p: int) -> List[int]:
    """Resíduos quadráticos módulo p (primo)."""
    return list({(x * x) % p for x in range(1, p)})

def legendre_symbol(a: int, p: int) -> int:
    """Símbolo de Legendre (a/p)."""
    if a % p == 0:
        return 0
    result = pow(a, (p - 1) // 2, p)
    return 1 if result == 1 else -1

def jacobi_symbol(a: int, n: int) -> int:
    """Símbolo de Jacobi (a/n)."""
    if n % 2 == 0 or n <= 0:
        raise ValueError("n deve ser ímpar e positivo")
    
    result = 1
    a = a % n
    
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    
    return result if n == 1 else 0
