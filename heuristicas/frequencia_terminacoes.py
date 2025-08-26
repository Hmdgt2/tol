from collections import Counter

def prever(sorteios, n=2):
    contador_terminacoes = Counter()
    contador_numeros = Counter()
    
    for s in sorteios:
        for num in s.get('numeros', []):
            terminacao = num % 10
            contador_terminacoes[terminacao] += 1
            contador_numeros[num] += 1

    terminacoes_mais_frequentes = [t for t, _ in contador_terminacoes.most_common(3)]
    
    candidatos = []
    for num, _ in contador_numeros.most_common(len(contador_numeros)):
        if (num % 10) in terminacoes_mais_frequentes:
            candidatos.append(num)

    sugeridos = candidatos[:n]

    return {
        "heuristica": "frequencia_terminacoes",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
