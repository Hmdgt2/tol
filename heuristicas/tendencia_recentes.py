# heuristicas/tendencia_recentes.py

from collections import Counter
from lib.dados import carregar_todos_sorteios

def tendencia_recentes(n=2, janela=10):
    """
    Retorna os n números mais frequentes nos últimos 'janela' concursos.
    """
    sorteios = carregar_todos_sorteios()

    if len(sorteios) < janela:
        janela = len(sorteios)

    ultimos = sorteios[-janela:]
    contador = Counter()

    for concurso in ultimos:
        contador.update(concurso["numeros"])

    mais_frequentes = [num for num, _ in contador.most_common(n)]
    return mais_frequentes

# Exemplo de teste direto
if __name__ == "__main__":
    print("Tendência recentes (últimos 10 concursos):", tendencia_recentes(2, 10))
