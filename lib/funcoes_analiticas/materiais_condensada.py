# lib/funcoes_analiticas/materiais_condensada.py
import numpy as np
from typing import List, Dict, Tuple
import math

# ============================================================
# Materiais Topológicos e Estrutura de Bandas
# ============================================================

def topological_insulator_invariants(lattice: List[List[float]]) -> Dict:
    """Calcula invariantes topológicos para isolantes topológicos."""
    if len(lattice) < 2:
        return {"error": "Lattice muito pequeno para análise topológica"}
    
    # Matriz de hopping (simplificada)
    hopping_matrix = calculate_hopping_matrix(lattice)
    
    # Invariantes de Chern (2D)
    chern_number = calculate_chern_number(hopping_matrix)
    
    # Invariante Z₂ (para isolantes topológicos de spin)
    z2_invariant = calculate_z2_invariant(hopping_matrix)
    
    # Simetrias de proteção
    symmetries = identify_protecting_symmetries(lattice)
    
    return {
        "lattice_type": classify_lattice_type(lattice),
        "chern_number": chern_number,
        "z2_invariant": z2_invariant,
        "topological_phase": classify_topological_phase(chern_number, z2_invariant),
        "protecting_symmetries": symmetries,
        "edge_states_present": chern_number != 0 or z2_invariant != 0,
        "bulk_boundary_correspondence": verify_bulk_boundary_correspondence(chern_number),
        "robustness_to_disorder": calculate_disorder_robustness(chern_number, z2_invariant)
    }

def band_structure_calculation(crystal_data: Dict) -> Dict:
    """Calcula estrutura de bandas para cristal."""
    lattice_vectors = crystal_data.get('lattice_vectors', [])
    atomic_positions = crystal_data.get('atomic_positions', [])
    
    if not lattice_vectors or not atomic_positions:
        return {"error": "Dados de cristal incompletos"}
    
    # Zona de Brillouin
    brillouin_zone = calculate_brillouin_zone(lattice_vectors)
    
    # Pontos de alta simetria
    high_symmetry_points = identify_high_symmetry_points(brillouin_zone)
    
    # Bandas de energia (simulação)
    energy_bands = simulate_energy_bands(lattice_vectors, atomic_positions)
    
    # Gap e propriedades
    band_gap = calculate_band_gap(energy_bands)
    fermi_level = estimate_fermi_level(energy_bands)
    
    return {
        "crystal_system": classify_crystal_system(lattice_vectors),
        "brillouin_zone_volume": brillouin_zone.get('volume', 0),
        "high_symmetry_points": high_symmetry_points,
        "energy_bands": {
            "number_of_bands": len(energy_bands),
            "band_gap": band_gap,
            "gap_type": classify_gap_type(band_gap),
            "fermi_level": fermi_level,
            "effective_masses": calculate_effective_masses(energy_bands)
        },
        "electronic_properties": {
            "conductor": band_gap == 0,
            "insulator": band_gap > 1.0,  # eV
            "semiconductor": 0 < band_gap <= 1.0
        },
        "optical_properties": estimate_optical_properties(band_gap)
    }

def phase_transition_critical_exponents(observables: List[float], temperatures: List[float]) -> Dict:
    """Calcula expoentes críticos de transição de fase."""
    if len(observables) != len(temperatures) or len(observables) < 5:
        return {"error": "Dados insuficientes para análise de expoentes críticos"}
    
    # Encontra temperatura crítica
    tc_index = estimate_critical_temperature(observables, temperatures)
    critical_temperature = temperatures[tc_index] if tc_index >= 0 else temperatures[len(temperatures)//2]
    
    # Ajuste de lei de potência
    exponents = fit_critical_exponents(observables, temperatures, critical_temperature)
    
    # Universalidade
    universality_class = identify_universality_class(exponents)
    
    return {
        "critical_temperature": critical_temperature,
        "critical_exponents": exponents,
        "universality_class": universality_class,
        "scaling_laws": {
            "valid": check_scaling_laws(exponents),
            "hyperscaling": check_hyperscaling(exponents),
            "rushbrooke_inequality": check_rushbrooke_inequality(exponents)
        },
        "finite_size_effects": analyze_finite_size_effects(observables, temperatures),
        "renormalization_group_flow": analyze_rg_flow(exponents, universality_class)
    }

def calculate_hopping_matrix(lattice: List[List[float]]) -> np.ndarray:
    """Calcula matriz de hopping para lattice."""
    n_sites = len(lattice)
    matrix = np.zeros((n_sites, n_sites))
    
    for i in range(n_sites):
        for j in range(n_sites):
            if i != j:
                distance = np.linalg.norm(np.array(lattice[i]) - np.array(lattice[j]))
                matrix[i,j] = math.exp(-distance)  # Hopping decaindo exponencialmente
    
    return matrix

def calculate_chern_number(hopping_matrix: np.ndarray) -> int:
    """Calcula número de Chern (simplificado)."""
    # Para modelo simples, Chern number é relacionado ao fluxo magnético
    eigenvalues = np.linalg.eigvals(hopping_matrix)
    flux = np.angle(eigenvalues).sum() / (2 * math.pi)
    return int(round(flux))

def calculate_z2_invariant(hopping_matrix: np.ndarray) -> int:
    """Calcula invariante Z₂ (simplificado)."""
    # Para sistemas com simetria TRS, Z₂ = 0 ou 1
    time_reversal_symmetric = check_time_reversal_symmetry(hopping_matrix)
    return 1 if time_reversal_symmetric and np.linalg.det(hopping_matrix) < 0 else 0
