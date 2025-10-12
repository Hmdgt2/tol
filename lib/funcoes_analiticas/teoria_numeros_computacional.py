# lib/funcoes_analiticas/teoria_numeros_computacional.py
import numpy as np
from typing import List
from sympy import factorint, isprime, primerange
import math

def pollard_rho_factorization(n: int, max_iter: int = 1000) -> int:
    """Algoritmo ρ de Pollard para fatoração."""
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    
    def f(x):
        return (x * x + 1) % n
    
    x, y, d = 2, 2, 1
    for _ in range(max_iter):
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), n)
        if d != 1 and d != n:
            return d
        if d == n:
            break
    
    return n  # Não encontrou fator

def baby_step_giant_step(a: int, b: int, p: int) -> int:
    """Algoritmo baby-step giant-step para logaritmo discreto."""
    m = int(math.isqrt(p)) + 1
    
    # Baby steps
    baby_steps = {}
    current = 1
    for j in range(m):
        baby_steps[current] = j
        current = (current * a) % p
    
    # Giant steps
    giant_step = pow(a, -m, p)
    current = b
    for i in range(m):
        if current in baby_steps:
            return i * m + baby_steps[current]
        current = (current * giant_step) % p
    
    return -1  # Não encontrado

def chinese_remainder_theorem(residues: List[int], moduli: List[int]) -> int:
    """Teorema Chinês do Resto."""
    if len(residues) != len(moduli):
        raise ValueError("Resíduos e módulos devem ter o mesmo tamanho")
    
    total_mod = 1
    for m in moduli:
        total_mod *= m
    
    result = 0
    for i, (a_i, m_i) in enumerate(zip(residues, moduli)):
        M_i = total_mod // m_i
        try:
            inv = pow(M_i, -1, m_i)
        except:
            inv = 1
        result = (result + a_i * M_i * inv) % total_mod
    
    return result

def miller_rabin_primality(n: int, k: int = 5) -> bool:
    """Teste de primalidade Miller-Rabin."""
    if n < 2:
        return False
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False
    
    # Escrever n-1 como d*2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    for _ in range(k):
        a = np.random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True
