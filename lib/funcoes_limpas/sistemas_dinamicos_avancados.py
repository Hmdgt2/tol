
'# Computacao Cientifica'
import numpy as np
pass
'# Outros'
from typing import List, Tuple
from scipy import signal
pass


def phase_space_reconstruction(seq: List[float], embedding_dim: int=3, tau: int=1) -> np.ndarray:
    'Reconstrução do espaço de fase usando método de delays.'
    n = len(seq)
    if (n < (embedding_dim * tau)):
        return np.array([])
    embedded = np.zeros(((n - ((embedding_dim - 1) * tau)), embedding_dim))
    for i in range(embedding_dim):
        embedded[(:, i)] = seq[(i * tau):(((i * tau) + n) - ((embedding_dim - 1) * tau))]
    return embedded


def recurrence_quantification_analysis(seq: List[float], threshold: float=0.1) -> Dict:
    'Análise de quantificação de recorrência para sistemas dinâmicos.'
    embedded = phase_space_reconstruction(seq)
    if (len(embedded) == 0):
        return {}
    n = len(embedded)
    recurrence_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance = np.linalg.norm((embedded[i] - embedded[j]))
            recurrence_matrix[(i, j)] = (1 if (distance <= threshold) else 0)
    recurrence_rate = np.mean(recurrence_matrix)
    diagonal_lines = []
    for i in range(n):
        for j in range((i + 1), n):
            if (recurrence_matrix[(i, j)] == 1):
                line_length = 1
                k = 1
                while (((i + k) < n) and ((j + k) < n) and (recurrence_matrix[((i + k), (j + k))] == 1)):
                    line_length += 1
                    k += 1
                if (line_length > 1):
                    diagonal_lines.append(line_length)
    determinism = ((sum(diagonal_lines) / np.sum(recurrence_matrix)) if (np.sum(recurrence_matrix) > 0) else 0)
    return {'recurrence_rate': recurrence_rate, 'determinism': determinism, 'average_diagonal_length': (np.mean(diagonal_lines) if diagonal_lines else 0), 'max_diagonal_length': (max(diagonal_lines) if diagonal_lines else 0)}


def lyapunov_exponent(seq: List[float]) -> float:
    'Expoente de Lyapunov para sequências.\n\n\n🔬 **Categoria**: Sistemas Dinâmicos\n🎯 **Aplicação**: Análise de sistemas não-lineares\n📈 **Método**: Baseado em teoria do caos\n\n🌪️ **Sistema**: Não-linear/Dinâmico\n'
    if (len(seq) < 2):
        return 0.0
    differences = [abs((seq[(i + 1)] - seq[i])) for i in range((len(seq) - 1))]
    return np.mean(np.log((np.array(differences) + 1e-10)))

