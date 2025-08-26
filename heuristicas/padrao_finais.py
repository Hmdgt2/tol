from collections import Counter
from lib.dados import contar_ocorrencias

def prever(sorteios, n=2):
    if len(sorteios) < 2:
        return {"nome": "padrao_finais", "numeros": []}

    ultimos_numeros = sorteios[-1].get('numeros', [])
    ultimas_terminacoes = [num % 10 for num in ultimos_numeros]
    
    contador_finais = Counter()
    for s in sorteios[:-1]:
        terminacoes_atuais = {num % 10 for num in s.get('numeros', [])}
        for term in ultimas_terminacoes:
            if term in terminacoes_atuais:
                contador_finais[term] += 1
    
    terminacoes_comuns = [t for t, _ in contador_finais.most_common(2)]
    
    frequencia_geral = contar_ocorrencias(sorteios)
    
    candidatos = []
    for num, _ in frequencia_geral.most_common(len(frequencia_geral)):
        if (num % 10) in terminacoes_comuns:
            candidatos.append(num)
            if len(candidatos) >= n:
                break
    
    if len(candidatos) < n: # Fallback se não houver candidatos suficientes
        sugeridos = [num for num, _ in frequencia_geral.most_common(n)]
    else:
        sugeridos = candidatos
        
    return {
        "heuristicas": "padrao_finais",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
