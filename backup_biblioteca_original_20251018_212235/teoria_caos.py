# lib/funcoes_analiticas/teoria_caos.py
import numpy as np
from typing import List, Dict
from scipy.integrate import odeint

def chaotic_system_identification(seq: List[float]) -> Dict:
    """Identifica características de sistemas caóticos na sequência."""
    if len(seq) < 100:
        return {}
    
    # Calcula expoentes de Lyapunov locais
    lyapunov_exponents = []
    for i in range(len(seq) - 10):
        window = seq[i:i+10]
        if len(window) > 5 and np.std(window) > 0:
            # Aproximação simples do expoente de Lyapunov
            differences = np.diff(np.log(np.abs(np.diff(window)) + 1e-10))
            lyap = np.mean(differences) if len(differences) > 0 else 0
            lyapunov_exponents.append(lyap)
    
    # Teste de caoticidade
    positive_lyap_ratio = len([x for x in lyapunov_exponents if x > 0]) / len(lyapunov_exponents)
    
    # Dimensão de correlação (aproximada)
    def correlation_dimension_estimate(data, max_embedding=5):
        if len(data) < 50:
            return 0
        
        dimensions = []
        for m in range(2, min(max_embedding + 1, len(data)//10)):
            # Embedding simples
            embedded = np.array([data[i:i+m] for i in range(len(data) - m)])
            
            # Calcula distâncias
            if len(embedded) > 1:
                from scipy.spatial.distance import pdist
                distances = pdist(embedded)
                
                # Conta pares dentro de raio r
                r = np.std(data) * 0.1
                close_pairs = np.sum(distances < r)
                total_pairs = len(distances)
                
                if total_pairs > 0 and close_pairs > 0:
                    C_r = close_pairs / total_pairs
                    dimensions.append(np.log(C_r) / np.log(r) if C_r > 0 and r > 0 else 0)
        
        return np.mean(dimensions) if dimensions else 0
    
    corr_dim = correlation_dimension_estimate(seq)
    
    return {
        'is_chaotic': positive_lyap_ratio > 0.1,
        'lyapunov_spectrum': {
            'mean': np.mean(lyapunov_exponents),
            'std': np.std(lyapunov_exponents),
            'positive_ratio': positive_lyap_ratio
        },
        'correlation_dimension': corr_dim,
        'chaos_confidence': min(1.0, positive_lyap_ratio * corr_dim * 10),
        'predictability_horizon': 1.0 / (np.mean([x for x in lyapunov_exponents if x > 0]) + 1e-10) if any(x > 0 for x in lyapunov_exponents) else float('inf')
    }
