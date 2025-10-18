# lib/funcoes_analiticas/teoria_representacao.py
import numpy as np
from typing import List, Callable

def character_orthogonality(chars1: List[complex], chars2: List[complex]) -> float:
    """Produto interno de caracteres (ortogonalidade)."""
    if len(chars1) != len(chars2):
        return 0.0
    
    product = sum(c1 * np.conj(c2) for c1, c2 in zip(chars1, chars2))
    return abs(product) / len(chars1)

def representation_dimension(rep_matrices: List[List[List[complex]]]) -> int:
    """Dimensão de uma representação."""
    if not rep_matrices:
        return 0
    return len(rep_matrices[0])

def irreducible_components_count(character: List[complex], irreps: List[List[complex]]) -> int:
    """Número de componentes irredutíveis em uma representação."""
    if not character or not irreps:
        return 0
    
    components = 0
    for irrep in irreps:
        if len(character) == len(irrep):
            # Coeficiente na decomposição
            coeff = character_orthogonality(character, irrep)
            if coeff > 0.5:  # Threshold
                components += int(round(coeff))
    
    return components

def schur_lemma_test(rep1: List[List[List[complex]]], rep2: List[List[List[complex]]]) -> bool:
    """Teste simplificado do Lema de Schur."""
    if not rep1 or not rep2:
        return False
    
    # Verificar se há homomorfismo não trivial entre representações
    try:
        # Simplificação: verificar se matrizes comutam
        for m1 in rep1:
            for m2 in rep2:
                m1_arr = np.array(m1)
                m2_arr = np.array(m2)
                if m1_arr.shape == m2_arr.shape:
                    comm = m1_arr @ m2_arr - m2_arr @ m1_arr
                    if np.linalg.norm(comm) < 1e-6:
                        return True
    except:
        pass
    
    return False
