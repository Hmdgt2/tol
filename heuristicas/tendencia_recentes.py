# heuristicas/tendencia_recentes.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "tendencia_recentes"
DESCRICAO = "Sugere os números mais frequentes nos últimos sorteios."
# Esta heurística precisa da estatística de frequência recente.
DEPENDENCIAS = ["frequencia_recente"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na sua frequência nos sorteios mais recentes.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'frequencia_recente' pré-calculada.
    frequencia_recente = estatisticas.get('frequencia_recente', {})
    
    if not frequencia_recente:
        return []

    # Retorna os n números mais frequentes da estatística recente
    sugeridos = [num for num, _ in Counter(frequencia_recente).most_common(n)]
    
    return sorted(sugeridos)
