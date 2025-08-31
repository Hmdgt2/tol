# heuristicas/trios_frequentes.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "trios_frequentes"
DESCRICAO = "Sugere números que aparecem juntos em trios frequentes nos sorteios passados."
# Esta heurística precisa da estatística de frequência de trios.
DEPENDENCIAS = ["trios_frequentes"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na frequência de trios de números.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    trios_frequentes = estatisticas.get('trios_frequentes', {})
    
    if not trios_frequentes:
        return []
    
    # Encontra os 10 trios mais frequentes.
    trios_mais_frequentes = Counter(trios_frequentes).most_common(10)
    
    # Conta a frequência individual dos números nesses trios.
    contador_numeros = Counter()
    for trio, _ in trios_mais_frequentes:
        contador_numeros.update(trio)
        
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return sorted(sugeridos)
