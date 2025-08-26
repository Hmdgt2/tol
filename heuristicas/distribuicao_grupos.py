from lib.dados import analisar_distribuicao_grupos
from collections import Counter
import random

def prever(sorteios, n=2):
    padrao_ideal_grupos = analisar_distribuicao_grupos(sorteios)
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))

    grupos_ordenados = sorted(
        enumerate(padrao_ideal_grupos),
        key=lambda item: item[1],
        reverse=True
    ) # (índice_grupo, contagem_ideal)

    sugeridos = []
    # Define as faixas dos grupos (ex: 1-10, 11-20, etc.)
    faixas = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 49)]

    for idx_grupo, _ in grupos_ordenados[:min(2, len(grupos_ordenados))]:
        limite_inferior, limite_superior = faixas[idx_grupo]

        candidatos_no_grupo = [
            num for num, _ in frequencia_geral.most_common(len(frequencia_geral))
            if limite_inferior <= num <= limite_superior
        ]
        
        if candidatos_no_grupo and len(sugeridos) < n:
            sugeridos.append(candidatos_no_grupo[0])

    if len(sugeridos) < n:
        todos_mais_frequentes = [num for num, _ in frequencia_geral.most_common(len(frequencia_geral))]
        for num in todos_mais_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "heuristica": "distribuicao_grupos",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
