# heuristicas/trios_frequentes.py
from collections import Counter

DESCRICAO = "Sugere números que aparecem juntos em trios frequentes nos sorteios passados."

def prever(estatisticas, n=5):
    """
    Prevê números com base na frequência de trios de números.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    trios_frequentes = estatisticas.get('trios_frequentes', {})
    
    if not trios_frequentes:
        return {
            "nome": "trios_frequentes",
            "numeros": []
        }
        
    trios_mais_frequentes = Counter(trios_frequentes).most_common(10)
    
    contador_numeros = Counter()
    for trio, _ in trios_mais_frequentes:
        contador_numeros.update(trio)
        
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return {
        "nome": "trios_frequentes",
        "numeros": sorted(list(set(sugeridos)))
    }
