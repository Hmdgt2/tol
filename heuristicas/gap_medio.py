# heuristicas/gap_medio.py

import os
import json
from collections import defaultdict

PASTA_DADOS = os.path.join(os.path.dirname(__file__), '..', 'dados_treino')


def calcular_gap_medio():
    historico = []
    for ano in sorted(os.listdir(PASTA_DADOS)):
        if ano.endswith('.json'):
            with open(os.path.join(PASTA_DADOS, ano), 'r', encoding='utf-8') as f:
                historico += json.load(f)

    ultimo_concurso = historico[-1]['numero_concurso']

    posicoes = defaultdict(list)

    for concurso in historico:
        for numero in concurso['numeros']:  # lista de 5 números
            posicoes[numero].append(concurso['numero_concurso'])

    gaps = {}
    for numero in range(1, 50):
        concursos = posicoes.get(numero, [])
        if len(concursos) < 2:
            gaps[numero] = 100  # arbitrário, não há dados suficientes
        else:
            diferencas = [j - i for i, j in zip(concursos[:-1], concursos[1:])]
            gaps[numero] = sum(diferencas) / len(diferencas)

    # Ordenar por menor gap (mais frequente), e escolher os 2 melhores
    melhores = sorted(gaps.items(), key=lambda x: x[1])[:2]
    sugeridos = [item[0] for item in melhores]

    return {
        "nome": "gap_medio",
        "sugeridos": sugeridos,
        "detalhes": gaps
    }


if __name__ == "__main__":
    resultado = calcular_gap_medio()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
