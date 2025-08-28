# heuristicas/ausencia_superior_media.py
from collections import Counter

def prever(estatisticas, n=5):
    """
    Prevê números com base na ausência, favorecendo aqueles ausentes por mais tempo que a média.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.

    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    # Acessa diretamente a estatística de ausência atual
    ausencia = estatisticas.get('ausencia_atual', {})

    if not ausencia:
        return {
            "nome": "ausencia_superior_media",
            "numeros": []
        }

    # Calcula a média de ausência
    numeros_presentes = [d for d in ausencia.values() if d != -1 and d != float('inf')]
    if not numeros_presentes:
        media = 0
    else:
        media = sum(numeros_presentes) / len(numeros_presentes)

    # Filtra os números com ausência superior à média
    candidatos = [num for num, dias in ausencia.items() if dias > media]

    # Ordena os candidatos do maior para o menor e pega os n primeiros
    sugeridos = sorted(candidatos, key=lambda x: ausencia[x], reverse=True)[:n]

    return {
        "nome": "ausencia_superior_media",
        "numeros": sugeridos
    }
