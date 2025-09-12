# lib/funcoes_analiticas/numeros_especiais.py
import sympy as sp
from typing import List

# ============================================================
# Sequências e números especiais
# ============================================================
def fibonacci(n: int) -> int:
    """Retorna o n-ésimo número de Fibonacci."""
    return int(sp.fibonacci(n))

def lucas(n: int) -> int:
    """Retorna o n-ésimo número de Lucas."""
    return int(sp.lucas(n))

def catalan_number(n: int) -> int:
    """Retorna o n-ésimo número de Catalan."""
    return int(sp.catalan(n))

def bell_number(n: int) -> int:
    """Retorna o n-ésimo número de Bell."""
    return int(sp.bell(n))

def partition_number(n: int) -> int:
    """Retorna o número de partições de n."""
    return int(sp.partition(n))

def stirling2(n: int, k: int) -> int:
    """Retorna o número de Stirling de segunda espécie S(n, k)."""
    return int(sp.stirling(n, k))

def stirling1(n: int, k: int) -> int:
    """Retorna o número de Stirling de primeira espécie s(n, k)."""
    return int(sp.stirling(n, k, kind=1))

def bernoulli_number(n: int) -> int:
    """Retorna o n-ésimo número de Bernoulli."""
    return int(sp.bernoulli(n))
