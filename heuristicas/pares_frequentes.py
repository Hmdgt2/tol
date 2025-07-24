# heuristicas/pares_frequentes.py

import os
import json
from collections import Counter
from itertools import combinations

PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados_treino'))

def ler_todos_os_concursos():
    concursos = []
    for ficheiro in sorted(os.listdir(PASTA_DADOS)):
        if ficheiro.endswith('.json'):
            with open(os.path.join(PASTA_DADOS, ficheiro), 'r', encoding='utf-8') as f:
                concursos_ano = json.load(f)
                concursos.extend(concursos_ano)
    return concursos

def pares_frequentes(top_n=10):
    concursos = ler_todos_os_concursos()
    contador_pares = Counter()

    for concurso in concursos:
        numeros = concurso['numeros']
        pares = combinations(sorted(numeros), 2)
        contador_pares.update(pares)

    # Obter os N pares mais frequentes
    pares_mais_frequentes = contador_pares.most_common(top_n)

    # Contar a frequência individual dos números nesses pares
    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)

    # Selecionar os 2 números mais frequentes entre esses pares
    mais_frequentes = [num for num, _ in contador_numeros.most_common(2)]
    return mais_frequentes

if __name__ == '__main__':
    sugestao = pares_frequentes()
    print(f"Sugestão (pares mais frequentes): {sugestao}")
