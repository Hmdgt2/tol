# heuristicas/frequencia_total.py
from lib.dados import contar_ocorrencias

def prever(sorteios, n=2):
    contador = contar_ocorrencias(sorteios)
    sugeridos = [num for num, _ in contador.most_common(n)]
    return {
        "nome": "frequencia_total",
        "numeros": sugeridos
    }
