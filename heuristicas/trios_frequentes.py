from collections import Counter
from lib.dados import carregar_todos_sorteios

def calcular_trios_frequentes(sorteios):
    trios_count = Counter()
    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        for i in range(len(numeros)):
            for j in range(i + 1, len(numeros)):
                for k in range(j + 1, len(numeros)):
                    trio = tuple(sorted([numeros[i], numeros[j], numeros[k]]))
                    trios_count[trio] += 1
    return trios_count

def trios_mais_frequentes(top_n=10):
    sorteios = carregar_todos_sorteios()
    trios_freq = calcular_trios_frequentes(sorteios)
    return trios_freq.most_common(top_n)

if __name__ == '__main__':
    top_trios = trios_mais_frequentes()
    print("Top trios mais frequentes:")
    for trio, freq in top_trios:
        print(f"{trio}: {freq} vezes")
