# heuristicas/pares_frequentes.py

from collections import Counter
from itertools import combinations
from lib.dados import carregar_sorteios

def pares_frequentes(top_n=10):
    """
    Retorna os 2 números mais frequentes entre os top_n pares mais frequentes.
    """
    concursos = carregar_sorteios()
    contador_pares = Counter()

    for concurso in concursos:
        numeros = concurso.get('numeros', [])
        pares = combinations(sorted(numeros), 2)
        contador_pares.update(pares)

    # Obter os top_n pares mais frequentes
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
