# heuristicas/pares_consecutivos.py
from collections import Counter

DESCRICAO = "Sugere números que formam pares consecutivos frequentes."

def prever(estatisticas, n=2):
    """
    Prevê números com base na frequência de pares de números consecutivos.
    
    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
        
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    pares_frequentes = estatisticas.get('pares_frequentes', {})
    
    if not pares_frequentes:
        return {
            "nome": "pares_consecutivos",
            "numeros": []
        }
        
    contador_consecutivos = Counter()
    
    # Filtra apenas os pares que são consecutivos
    for par, freq in pares_frequentes.items():
        if par[1] - par[0] == 1:
            contador_consecutivos[par] = freq
            
    pares_mais_frequentes = contador_consecutivos.most_common(5)
    
    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
        
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return {
        "nome": "pares_consecutivos",
        "numeros": sorted(list(set(sugeridos)))
    }
