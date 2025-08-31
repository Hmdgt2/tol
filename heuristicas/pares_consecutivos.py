# heuristicas/pares_consecutivos.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "pares_consecutivos"
DESCRICAO = "Sugere números que formam pares consecutivos frequentes."
# Esta heurística precisa de uma estatística que conte apenas os pares consecutivos.
DEPENDENCIAS = ["frequencia_pares_consecutivos"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na frequência de pares de números consecutivos.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'frequencia_pares_consecutivos' pré-calculada.
    pares_consecutivos = estatisticas.get('frequencia_pares_consecutivos', {})
    
    if not pares_consecutivos:
        return []

    # Encontra os números mais frequentes dentro dos pares consecutivos mais comuns.
    contador_numeros = Counter()
    pares_mais_frequentes = pares_consecutivos.most_common(5)

    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
    
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return sorted(sugeridos)
