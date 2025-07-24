# heuristicas/frequencia_total.py

from collections import Counter
from lib.dados import carregar_todos_sorteios

def frequencia_total(n=2):
    """
    Retorna os n números mais frequentes ao longo de todos os sorteios.
    """
    sorteios = carregar_todos_sorteios()
    contador = Counter()

    for concurso in sorteios:
        numeros = concurso["numeros"]
        contador.update(numeros)

    mais_frequentes = [num for num, _ in contador.most_common(n)]
    return mais_frequentes

# Exemplo de teste direto
if __name__ == "__main__":
    print("Números mais frequentes:", frequencia_total(2))
