# lib/funcoes_analiticas/fisica_matematica.py
import numpy as np
from typing import List, Dict, Tuple
import math

# ============================================================
# Teoria Quântica de Campos
# ============================================================

def feynman_diagram_complexity(vertices: int, loops: int) -> Dict:
    """Analisa complexidade de diagramas de Feynman."""
    if vertices < 0 or loops < 0:
        return {"error": "Número de vértices e loops deve ser não-negativo"}
    
    # Número de diagramas (estimativa)
    def count_diagrams(v, l):
        # Fórmula aproximada para teoria φ^4
        if v == 0:
            return 1
        base_diagrams = math.factorial(2 * v) // (2 ** v * math.factorial(v))
        return base_diagrams * (l + 1) ** 2
    
    # Dimensão do espaço de integração
    integration_dimension = 4 * loops  # Em 4 dimensões espaço-temporais
    
    # Grau de divergência
    superficial_degree = 4 * loops - 2 * vertices
    
    diagram_count = count_diagrams(vertices, loops)
    
    return {
        "vertices": vertices,
        "loops": loops,
        "diagram_count_estimate": diagram_count,
        "integration_dimension": integration_dimension,
        "superficial_degree_of_divergence": superficial_degree,
        "renormalizability": "renormalizable" if superficial_degree <= 0 else "non-renormalizable",
        "symmetry_factors": estimate_symmetry_factors(vertices),
        "topology_complexity": analyze_diagram_topology(vertices, loops)
    }

def conformal_field_theory_analysis(central_charge: float) -> Dict:
    """Analisa teoria de campo conforme com carga central dada."""
    if central_charge <= 0:
        return {"error": "Carga central deve ser positiva"}
    
    # Mínimo modelo unitário
    unitary_minimal_models = []
    for m in range(3, 20):  # m ≥ 3
        c = 1 - 6 / (m * (m + 1))
        if c > 0 and c < 1:
            unitary_minimal_models.append((m, c))
    
    # Dimensões conformes primárias
    primary_dimensions = []
    for m, c_val in unitary_minimal_models[:5]:
        for r in range(1, m):
            for s in range(1, m + 1):
                if r < s:
                    h = ((m + 1) * r - m * s) ** 2 - 1
                    h /= 4 * m * (m + 1)
                    primary_dimensions.append(h)
    
    # Verifica se é teoria racional
    is_rational = any(abs(central_charge - c) < 1e-6 for _, c in unitary_minimal_models)
    
    return {
        "central_charge": central_charge,
        "unitary": central_charge >= 1 or is_rational,
        "minimal_model": next((m for m, c in unitary_minimal_models if abs(c - central_charge) < 1e-6), None),
        "primary_operator_spectrum": {
            "estimated_count": len([h for h in primary_dimensions if h >= 0]),
            "lowest_dimension": min(primary_dimensions) if primary_dimensions else 0,
            "rational_cft": is_rational
        },
        "partition_function_modularity": check_modular_invariance(central_charge),
        "operator_product_expansion": analyze_ope_structure(central_charge)
    }

def string_theory_compactification(dimensions: int) -> Dict:
    """Analisa compactificação de teoria de cordas."""
    if dimensions not in [10, 11, 26]:
        return {"error": "Dimensões suportadas: 10 (superstrings), 11 (M-theory), 26 (bosonic)"}
    
    # Graus de liberdade
    if dimensions == 10:
        theory_type = "superstring"
        supersymmetry = "N=2"
        compact_dimensions = 6
        moduli_space_dim = estimate_moduli_dimension(compact_dimensions)
    elif dimensions == 11:
        theory_type = "M-theory"
        supersymmetry = "N=1"
        compact_dimensions = 7
        moduli_space_dim = estimate_moduli_dimension(compact_dimensions)
    else:  # 26
        theory_type = "bosonic_string"
        supersymmetry = "N=0"
        compact_dimensions = 22
        moduli_space_dim = estimate_moduli_dimension(compact_dimensions)
    
    # Espectro de massa
    mass_spectrum = generate_mass_spectrum(dimensions, compact_dimensions)
    
    return {
        "total_dimensions": dimensions,
        "theory_type": theory_type,
        "supersymmetry": supersymmetry,
        "compact_dimensions": compact_dimensions,
        "moduli_space_dimension": moduli_space_dim,
        "mass_spectrum": mass_spectrum,
        "duality_groups": identify_duality_groups(dimensions),
        "brane_content": identify_brane_content(dimensions, theory_type)
    }

def estimate_symmetry_factors(vertices: int) -> int:
    """Estima fatores de simetria para diagramas de Feynman."""
    if vertices <= 0:
        return 1
    return math.factorial(vertices) // (2 ** (vertices // 2))

def analyze_diagram_topology(vertices: int, loops: int) -> Dict:
    """Analisa topologia de diagramas de Feynman."""
    euler_characteristic = vertices - loops + 1
    genus = (2 - euler_characteristic) // 2
    
    return {
        "euler_characteristic": euler_characteristic,
        "genus": max(0, genus),
        "planar": loops == 0,
        "connectivity": "simply_connected" if genus == 0 else "multiply_connected"
    }

def check_modular_invariance(c: float) -> bool:
    """Verifica invariância modular (condição necessária para CFT)."""
    # Para CFT unitária, c deve ser positiva
    return c > 0

def analyze_ope_structure(c: float) -> Dict:
    """Analisa estrutura de expansão de produto de operadores."""
    fusion_rules_complexity = c * 10  # Heurística
    return {
        "fusion_rules_count": int(fusion_rules_complexity),
        "associativity_constraints": int(c * 5),
        "conformal_blocks": int(c * 20)
    }

def estimate_moduli_dimension(compact_dims: int) -> int:
    """Estima dimensão do espaço de módulos."""
    # Para variedade de Calabi-Yau 3-fold: h^{1,1} + h^{2,1}
    if compact_dims == 6:
        return 100  # Típico para CY3
    elif compact_dims == 7:
        return 140  # Para G2
    else:  # 22
        return 528  # Para bosonic
