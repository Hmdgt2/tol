# lib/funcoes_analiticas/processos_estocasticos_avancados.py
import numpy as np
from typing import List, Dict, Tuple
import math

# ============================================================
# Cálculo de Malliavin e Martingales
# ============================================================

def malliavin_calculus_derivative(process: List[float], time_points: List[float] = None) -> Dict:
    """Calcula derivada no sentido de Malliavin para processo estocástico."""
    if len(process) < 3:
        return {"error": "Processo muito curto para análise Malliavin"}
    
    if time_points is None:
        time_points = list(range(len(process)))
    
    # Calcula variações (simulação da derivada estocástica)
    variations = []
    for i in range(1, len(process)):
        dt = time_points[i] - time_points[i-1] if i < len(time_points) else 1.0
        if dt > 0:
            variation = (process[i] - process[i-1]) / math.sqrt(dt)
            variations.append(variation)
    
    # Análise de sensibilidade Malliavin
    sensitivity = np.std(variations) if variations else 0
    smoothness = 1.0 / (1.0 + sensitivity)  # Medida de suavidade
    
    return {
        "process_length": len(process),
        "malliavin_sensitivity": sensitivity,
        "smoothness_measure": smoothness,
        "variation_statistics": {
            "mean": np.mean(variations) if variations else 0,
            "std": np.std(variations) if variations else 0,
            "skewness": float(np.cov(variations, variations[1:] + [0])[0,1]) if len(variations) > 1 else 0
        },
        "differentiability": "malliavin_differentiable" if smoothness > 0.5 else "not_differentiable",
        "integration_by_parts_applicable": smoothness > 0.3
    }

def local_time_calculation(brownian_motion: List[float], level: float = 0.0) -> Dict:
    """Calcula tempo local do movimento browniano."""
    if len(brownian_motion) < 10:
        return {"error": "Trajetória browniana muito curta"}
    
    # Aproximação do tempo local
    epsilon = 0.1 * np.std(brownian_motion)
    local_time = 0
    
    crossings = []
    for i in range(1, len(brownian_motion)):
        # Verifica cruzamento do nível
        if (brownian_motion[i-1] - level) * (brownian_motion[i] - level) <= 0:
            crossings.append(i)
        
        # Aproximação da densidade do tempo local
        if abs(brownian_motion[i] - level) < epsilon:
            local_time += 1
    
    normalized_local_time = local_time / len(brownian_motion)
    
    return {
        "level": level,
        "local_time_estimate": normalized_local_time,
        "crossing_count": len(crossings),
        "crossing_times": crossings[:10],  # Primeiros 10 cruzamentos
        "occupation_measure": normalized_local_time,
        "tanaka_formula_applicable": len(crossings) > 0,
        "brownian_scaling_violation": check_scaling_violation(brownian_motion, crossings)
    }

def levy_process_characteristics(triplet: Tuple[float, float, float]) -> Dict:
    """Analisa características de processo de Lévy dado o tripleto."""
    drift, diffusion, jump_measure = triplet
    
    # Classificação do processo
    if jump_measure == 0:
        process_type = "brownian_motion_with_drift"
    elif diffusion == 0 and jump_measure > 0:
        process_type = "pure_jump_process"
    else:
        process_type = "jump_diffusion"
    
    # Expoente característico
    def characteristic_exponent(u):
        return -1j * drift * u - 0.5 * diffusion * u**2 + jump_measure * (np.exp(1j*u) - 1)
    
    # Medidas de atividade
    total_variation = diffusion + abs(drift) + jump_measure
    jump_activity = jump_measure / total_variation if total_variation > 0 else 0
    
    return {
        "levy_triplet": {
            "drift": drift,
            "diffusion": diffusion,
            "jump_measure": jump_measure
        },
        "process_type": process_type,
        "characteristic_exponent_samples": [
            float(characteristic_exponent(0.1).real),
            float(characteristic_exponent(1.0).real),
            float(characteristic_exponent(10.0).real)
        ],
        "activity_measures": {
            "total_variation": total_variation,
            "jump_activity": jump_activity,
            "gaussian_component_strength": diffusion / total_variation if total_variation > 0 else 0
        },
        "path_properties": {
            "finite_variation": jump_measure < 1.0,
            "has_jumps": jump_measure > 0,
            "martingale": drift == 0
        }
    }

def check_scaling_violation(brownian_motion: List[float], crossings: List[int]) -> float:
    """Verifica violação de escalonamento browniano."""
    if len(crossings) < 2:
        return 0.0
    
    # Para browniano puro, número de cruzamentos escala com sqrt(t)
    expected_crossings = math.sqrt(len(brownian_motion))
    actual_crossings = len(crossings)
    
    violation = abs(actual_crossings - expected_crossings) / expected_crossings
    return min(1.0, violation)
