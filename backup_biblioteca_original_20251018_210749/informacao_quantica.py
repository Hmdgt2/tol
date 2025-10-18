# lib/funcoes_analiticas/informacao_quantica.py
import numpy as np
from typing import List
from scipy import linalg

def density_matrix_purity(rho: List[List[complex]]) -> float:
    """Pureza de uma matriz densidade: Tr(ρ²)."""
    rho_arr = np.array(rho)
    rho_squared = rho_arr @ rho_arr
    return np.real(np.trace(rho_squared))

def von_neumann_entropy(rho: List[List[complex]]) -> float:
    """Entropia de von Neumann: -Tr(ρ log ρ)."""
    rho_arr = np.array(rho)
    eigenvalues = linalg.eigvals(rho_arr)
    entropy = 0.0
    for lam in eigenvalues:
        if abs(lam) > 1e-12:
            entropy -= lam * np.log(lam + 1e-12)
    return np.real(entropy)

def quantum_fidelity(rho: List[List[complex]], 
                    sigma: List[List[complex]]) -> float:
    """Fidelidade quântica entre dois estados."""
    rho_arr, sigma_arr = np.array(rho), np.array(sigma)
    
    try:
        sqrt_rho = linalg.sqrtm(rho_arr)
        product = sqrt_rho @ sigma_arr @ sqrt_rho
        fidelity = np.real(np.trace(linalg.sqrtm(product))) ** 2
        return max(0.0, min(1.0, fidelity))
    except:
        return 0.0

def concurrence_entanglement(rho: List[List[complex]]) -> float:
    """Concorrência para medida de emaranhamento de 2 qubits."""
    if len(rho) != 4 or len(rho[0]) != 4:
        return 0.0
    
    rho_arr = np.array(rho)
    # Matriz spin-flip
    Y = np.array([[0, -1j], [1j, 0]])
    YY = np.kron(Y, Y)
    
    R = rho_arr @ YY @ rho_arr.conj() @ YY
    eigenvalues = sorted(np.real(linalg.eigvals(R)), reverse=True)
    
    if len(eigenvalues) >= 1 and eigenvalues[0] > 0:
        concurrence = max(0.0, np.sqrt(eigenvalues[0]) - 
                         sum(np.sqrt(max(0.0, e)) for e in eigenvalues[1:]))
        return concurrence
    return 0.0
