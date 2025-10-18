# lib/funcoes_analiticas/analise_quantica.py
import numpy as np
from typing import List, Dict
from scipy import linalg

def quantum_wavefunction_analysis(seq: List[float]) -> Dict:
    """Análise inspirada em funções de onda quântica."""
    if len(seq) < 10:
        return {}
    
    # Normaliza a sequência como uma função de onda
    psi = np.array(seq)
    psi = psi / (np.linalg.norm(psi) + 1e-10)  # Normalização
    
    # Calcula "observáveis quânticos"
    position_expectation = np.sum(np.arange(len(psi)) * psi**2)
    momentum_psi = np.fft.fft(psi)
    momentum_expectation = np.sum(np.arange(len(momentum_psi)) * np.abs(momentum_psi)**2)
    
    # Matriz densidade reduzida (para sistemas compostos)
    if len(psi) >= 4:
        # Divide o sistema em duas partes
        split_point = len(psi) // 2
        psi_matrix = np.outer(psi[:split_point], psi[split_point:])
        density_matrix = np.conj(psi_matrix.T) @ psi_matrix
        
        # Entropia de von Neumann
        eigenvalues = np.linalg.eigvalsh(density_matrix)
        eigenvalues = eigenvalues[eigenvalues > 1e-10]  # Remove zeros numéricos
        von_neumann_entropy = -np.sum(eigenvalues * np.log(eigenvalues))
    else:
        von_neumann_entropy = 0
    
    return {
        'position_expectation': position_expectation,
        'momentum_expectation': momentum_expectation,
        'uncertainty_principle': position_expectation * momentum_expectation,
        'von_neumann_entropy': von_neumann_entropy,
        'quantum_coherence': np.max(np.abs(np.fft.fft(psi))) / len(psi)
    }

def stochastic_process_classification(seq: List[float]) -> Dict:
    """Classifica o processo estocástico subjacente."""
    if len(seq) < 30:
        return {'classification': 'insufficient_data'}
    
    # Testa diferentes hipóteses de processos estocásticos
    tests = {}
    
    # 1. Teste para passeio aleatório
    differences = np.diff(seq)
    adf_statistic = np.corrcoef(differences[:-1], differences[1:])[0,1] if len(differences) > 1 else 0
    tests['random_walk'] = abs(adf_statistic) < 0.1
    
    # 2. Teste para processo de mean-reversion
    from_mean_deviation = np.mean([abs(seq[i] - np.mean(seq[:i])) for i in range(1, len(seq))])
    tests['mean_reverting'] = from_mean_deviation < np.std(seq) * 0.5
    
    # 3. Teste para tendência determinística
    x = np.arange(len(seq))
    linear_fit = np.polyfit(x, seq, 1)
    residuals = seq - (linear_fit[0] * x + linear_fit[1])
    tests['deterministic_trend'] = np.var(residuals) < np.var(seq) * 0.3
    
    # 4. Teste para sazonalidade
    if len(seq) > 50:
        # Verifica padrões periódicos
        spectrum = np.abs(np.fft.fft(seq))**2
        dominant_freq = np.argmax(spectrum[1:len(spectrum)//2]) + 1
        tests['seasonal'] = spectrum[dominant_freq] > np.mean(spectrum) * 3
    
    # Classificação final
    classification = "complex_composite"
    if tests.get('random_walk', False):
        classification = "random_walk"
    elif tests.get('mean_reverting', False):
        classification = "mean_reverting"
    elif tests.get('deterministic_trend', False):
        classification = "deterministic_trend"
    elif tests.get('seasonal', False):
        classification = "seasonal"
    
    return {
        'process_classification': classification,
        'hypothesis_tests': tests,
        'complexity_score': len([t for t in tests.values() if t]) / len(tests)
    }
