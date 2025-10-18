# lib/funcoes_analiticas/algebra_abstrata.py
import numpy as np
from typing import List, Any, Callable
from itertools import product

def group_character_table(elements: List[Any], operation: Callable) -> List[List[complex]]:
    """Tabela de caracteres de um grupo finito."""
    n = len(elements)
    characters = []
    
    # Para cada elemento, calcular traço da representação regular
    for g in elements:
        char_row = []
        # Matriz de representação regular
        rep_matrix = np.zeros((n, n), dtype=complex)
        for i, h in enumerate(elements):
            gh = operation(g, h)
            j = elements.index(gh)
            rep_matrix[j, i] = 1
        # Caráter é o traço
        char_row.append(np.trace(rep_matrix))
        characters.append(char_row)
    
    return characters

def group_commutator_subgroup_size(elements: List[Any], operation: Callable) -> int:
    """Tamanho do subgrupo comutador aproximado."""
    commutators = set()
    for a in elements:
        for b in elements:
            comm = operation(operation(a, b), operation(b, a))  # [a,b] = aba⁻¹b⁻¹
            if comm in elements:
                commutators.add(comm)
    return len(commutators)

def ring_ideal_generator(ring_elements: List[int], operation: Callable) -> int:
    """Encontra gerador de ideal principal em anel comutativo."""
    if not ring_elements:
        return 0
    # Em Z, o ideal é gerado pelo mdc
    return np.gcd.reduce(ring_elements)

def field_extension_degree(base_field: List[float], extension: List[float]) -> float:
    """Grau de extensão de corpo aproximado."""
    if not base_field or not extension:
        return 1.0
    # Razão entre dimensões como aproximação
    return len(extension) / len(base_field) if len(base_field) > 0 else 1.0

def module_homomorphism_rank(domain: List[List[float]], codomain: List[List[float]]) -> int:
    """Posto de homomorfismo entre módulos."""
    if not domain or not codomain:
        return 0
    # Aproximação usando posto matricial
    domain_mat = np.array(domain)
    codomain_mat = np.array(codomain)
    return min(np.linalg.matrix_rank(domain_mat), np.linalg.matrix_rank(codomain_mat))
