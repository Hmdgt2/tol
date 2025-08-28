# heuristicas/pares_frequentes.py
from collections import Counter

def prever(estatisticas, n=5):
    """
    Prevê números com base na frequência de pares de números.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    pares_frequentes = estatisticas.get('pares_frequentes', {})
    
    if not pares_frequentes:
        return {
            "nome": "pares_frequentes",
            "numeros": []
        }
        
    pares_mais_frequentes = Counter(pares_frequentes).most_common(10)
    
    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
        
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return {
        "nome": "pares_frequentes",
        "numeros": sorted(list(set(sugeridos)))
    }
