# heuristicas/frequencia_total.py
from typing import Dict, Any, List
from collections import Counter

# --- Heuristic Metadata ---
# The new architecture uses a metadata pattern to define the heuristic.
NOME = "frequencia_total"
DESCRICAO = "Sugere os números mais frequentes no histórico."
# This heuristic explicitly declares its dependency.
DEPENDENCIAS = ["frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Predicts numbers based on their total historical frequency.
    
    Args:
        estatisticas (dict): Dictionary with the pre-calculated statistics the heuristic depends on.
        n (int): The number of suggestions to return.
        
    Returns:
        list: A list of suggested numbers.
    """
    # Access the pre-calculated 'frequencia_total' statistic.
    frequencia = estatisticas.get('frequencia_total', {})
    
    # If the statistic is empty, return an empty list.
    if not frequencia:
        return []

    # Return the 'n' most frequent numbers.
    # The Counter is used here to get the most common items from the dict.
    sugeridos = [num for num, _ in Counter(frequencia).most_common(n)]

    return sorted(sugeridos)
