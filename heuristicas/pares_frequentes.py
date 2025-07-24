# heuristicas/pares_frequentes.py
from collections import Counter
from itertools import combinations
from lib.dados import carregar_sorteios

def prever(sorteios, n=2):
    contador_pares = Counter()
    for concurso in sorteios:
        numeros = concurso.get('numeros', [])
        pares = combinations(sorted(numeros), 2)
        contador_pares.update(pares)
    pares_mais_frequentes = contador_pares.most_common(10)
    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    return {
        "nome": "pares_frequentes",
        "numeros": sugeridos
    }
