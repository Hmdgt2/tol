from collections import Counter
from itertools import combinations
from lib.dados import calcular_somas_sorteios

def prever(sorteios, n=2):
    somas_por_sorteio = [sum(s['numeros']) for s in sorteios if 'numeros' in s]
    if not somas_por_sorteio:
        return {"nome": "frequencia_soma", "numeros": []}
    
    contador_somas = Counter(somas_por_sorteio)
    soma_mais_comum = contador_somas.most_common(1)[0][0]
    
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))

    candidatos_por_freq = [num for num, _ in frequencia_geral.most_common(20)]
    
    melhores_combinacoes_de_5 = []
    
    for comb in combinations(candidatos_por_freq, 5):
        if sum(comb) == soma_mais_comum:
            melhores_combinacoes_de_5.append(comb)
            if len(melhores_combinacoes_de_5) > 500: # Limite para performance
                break

    if not melhores_combinacoes_de_5:
        return {"nome": "frequencia_soma", "numeros": []}
    
    contador_numeros = Counter()
    for comb in melhores_combinacoes_de_5:
        contador_numeros.update(comb)
    
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]

    return {
        "heuristicas": "frequencia_soma",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
