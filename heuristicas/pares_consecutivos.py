from collections import Counter

def prever(sorteios, n=2):
    contador_consecutivos = Counter()
    for concurso in sorteios:
        numeros = sorted(concurso.get('numeros', []))
        # Identifica pares de números consecutivos
        for i in range(len(numeros) - 1):
            if numeros[i+1] - numeros[i] == 1:
                contador_consecutivos.update([(numeros[i], numeros[i+1])])

    pares_mais_frequentes = contador_consecutivos.most_common(5) # Top 5 pares

    contador_numeros = Counter()
    for par, _ in pares_mais_frequentes:
        contador_numeros.update(par)
    
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]

    return {
        "heuristica": "pares_consecutivos",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
