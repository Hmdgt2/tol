# heuristicas/frequencia_total.py

from collections import Counter

def prever(estatisticas, n=5):
    """
    Prevê números com base na frequência total.
    
    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
        
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    # Acessa diretamente a estatística de frequência total
    contador = estatisticas.get('frequencia_total', {})
    
    # Se o contador estiver vazio, retorna uma lista vazia
    if not contador:
        return {
            "nome": "frequencia_total",
            "numeros": []
        }
    
    # Retorna os n números mais frequentes
    sugeridos = [num for num, _ in Counter(contador).most_common(n)]

    return {
        "nome": "frequencia_total",
        "numeros": sugeridos
    }
