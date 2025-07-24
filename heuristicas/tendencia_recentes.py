# heuristicas/tendencia_recentes.py
from lib.dados import contar_ocorrencias

def prever(sorteios, n=2, janela=10):
    if len(sorteios) < janela:
        janela = len(sorteios)
    ultimos = sorteios[-janela:]
    contador = contar_ocorrencias(ultimos)
    sugeridos = [num for num, _ in contador.most_common(n)]
    return {
        "nome": "tendencia_recentes",
        "numeros": sugeridos
    }
