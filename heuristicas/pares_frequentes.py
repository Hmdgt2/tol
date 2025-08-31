# heuristicas/pares_frequentes.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "pares_frequentes"
DESCRICAO = "Sugere números presentes nos pares mais frequentes."
# Esta heurística precisa da estatística de frequência de pares.
DEPENDENCIAS = ["pares_frequentes"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na frequência de pares de números.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    pares_frequentes = estatisticas.get('pares_frequentes', {})
    
    if not pares_frequentes:
        return []
    
    # Encontra os 10 pares mais frequentes.
    pares_mais_frequentes = Counter(pares_frequentes).most_common(10)
    
    # Conta a frequência individual dos números nesses pares.
    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
        
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return sorted(sugeridos)
