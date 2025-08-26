from collections import Counter
from itertools import combinations

def prever(sorteios, n=2):
    contador_consecutivos = Counter()
    for concurso in sorteios:
        numeros = sorted(concurso.get('numeros', []))
        # Identifica pares de números consecutivos
        pares = []
        for i in range(len(numeros) - 1):
            if numeros[i+1] - numeros[i] == 1:
                pares.append((numeros[i], numeros[i+1]))
        contador_consecutivos.update(pares)

    pares_mais_frequentes = contador_consecutivos.most_common(5) # Top 5 pares

    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
    
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]

    return {
        "nome": "pares_consecutivos",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
