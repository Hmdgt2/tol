# heuristicas/tendencia_recentes.py

from collections import Counter
from lib.dados import carregar_sorteios, contar_ocorrencias

def tendencia_recentes(n=2, janela=10):
    """
    Retorna os n números mais frequentes nos últimos 'janela' concursos.
    """
    sorteios = carregar_sorteios()

    if len(sorteios) < janela:
        janela = len(sorteios)

    ultimos = sorteios[-janela:]
    contador = contar_ocorrencias(ultimos)

    return [num for num, _ in contador.most_common(n)]


if __name__ == "__main__":
    print("Tendência recentes (últimos 10 concursos):", tendencia_recentes(2, 10))
