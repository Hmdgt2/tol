# heuristicas/ausencia_superior_media.py

from collections import defaultdict
from lib.dados import carregar_todos_sorteios

def ausencia_superior_media(n=2):
    """
    Retorna os n números com ausência superior à média de ausência geral.
    """
    sorteios = carregar_todos_sorteios()
    ultima_ocorrencia = defaultdict(lambda: -1)
    total_concursos = len(sorteios)

    # Regista o último concurso em que cada número apareceu
    for idx, concurso in enumerate(sorteios):
        for numero in concurso["numeros"]:
            ultima_ocorrencia[numero] = idx

    # Calcula a ausência de cada número
    ausencia = {num: total_concursos - idx - 1 for num, idx in ultima_ocorrencia.items()}

    # Calcula a média de ausência
    media_ausencia = sum(ausencia.values()) / len(ausencia)

    # Seleciona os que estão acima da média
    candidatos = [num for num, dias in ausencia.items() if dias > media_ausencia]

    # Ordena por maior ausência e devolve os top n
    candidatos_ordenados = sorted(candidatos, key=lambda x: ausencia[x], reverse=True)
    return candidatos_ordenados[:n]

# Exemplo de teste direto
if __name__ == "__main__":
    print("Ausentes acima da média:", ausencia_superior_media(2))
