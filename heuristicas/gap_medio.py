# heuristicas/gap_medio.py
from lib.dados import calcular_gaps_por_numero

def prever(sorteios, n=2):
    gaps = calcular_gaps_por_numero(sorteios)
    melhores = sorted(gaps.items(), key=lambda x: x[1])[:n]
    sugeridos = [item[0] for item in melhores]
    return {
        "nome": "gap_medio",
        "numeros": sugeridos
    }
