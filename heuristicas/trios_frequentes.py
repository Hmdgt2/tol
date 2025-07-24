from collections import Counter
from itertools import combinations
from lib.dados import carregar_sorteios

def calcular_trios_frequentes(sorteios):
    """
    Conta a frequência de cada trio de números nos sorteios.
    """
    trios_count = Counter()
    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        trios = combinations(sorted(numeros), 3)
        trios_count.update(trios)
    return trios_count

def trios_mais_frequentes(top_n=10):
    sorteios = carregar_sorteios()
    trios_freq = calcular_trios_frequentes(sorteios)
    return trios_freq.most_common(top_n)

if __name__ == '__main__':
    top_trios = trios_mais_frequentes()
    print("Top trios mais frequentes:")
    for trio, freq in top_trios:
        print(f"{trio}: {freq} vezes")
