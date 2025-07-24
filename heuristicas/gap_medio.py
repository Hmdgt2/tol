# heuristicas/gap_medio.py

import json
from collections import defaultdict
from lib.dados import carregar_sorteios

def calcular_gap_medio(n=2):
    """
    Calcula o gap médio (diferença média entre concursos em que um número aparece).
    Retorna os n números com menor gap (mais "constantes").
    """
    sorteios = carregar_sorteios()

    # Atribuir um número de concurso artificial (posição)
    for idx, concurso in enumerate(sorteios):
        concurso['numero_concurso'] = idx

    posicoes = defaultdict(list)

    for concurso in sorteios:
        numero_concurso = concurso['numero_concurso']
        for numero in concurso['numeros']:
            posicoes[numero].append(numero_concurso)

    gaps = {}
    for numero in range(1, 50):
        concursos = posicoes.get(numero, [])
        if len(concursos) < 2:
            gaps[numero] = float('inf')  # Penalizar os que têm poucos dados
        else:
            diferencas = [j - i for i, j in zip(concursos[:-1], concursos[1:])]
            gaps[numero] = sum(diferencas) / len(diferencas)

    # Ordenar por menor gap (mais frequente)
    melhores = sorted(gaps.items(), key=lambda x: x[1])[:n]
    sugeridos = [item[0] for item in melhores]

    return {
        "nome": "gap_medio",
        "sugeridos": sugeridos,
        "detalhes": gaps
    }


if __name__ == "__main__":
    resultado = calcular_gap_medio()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
