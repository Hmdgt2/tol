# heuristicas/trios_frequentes.py
from lib.dados import calcular_trios_frequentes
from collections import Counter

def prever(sorteios, n=2):
    trios = calcular_trios_frequentes(sorteios)
    contador = Counter()
    for trio, _ in trios.most_common(10):
        contador.update(trio)
    sugeridos = [num for num, _ in contador.most_common(n)]
    return {
        "nome": "trios_frequentes",
        "numeros": sugeridos
    }

