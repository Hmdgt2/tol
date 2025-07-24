# heuristicas/repeticoes_sorteios_anteriores.py
from lib.dados import calcular_repeticoes_ultimos_sorteios
from collections import Counter
import random

def prever(sorteios, n=2, num_sorteios_anteriores=5):
    probabilidades_repeticoes = calcular_repeticoes_ultimos_sorteios(sorteios, num_sorteios_anteriores)
    
    # Identificar o número de repetições mais provável
    # Ex: se a probabilidade de 1 repetição é a maior, a heurística foca nisso.
    
    # Calcular a frequência geral para ter números "quentes"
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))

    # Obter os números dos últimos 'num_sorteios_anteriores' sorteios
    numeros_recentes = Counter()
    for i in range(1, num_sorteios_anteriores + 1):
        if len(sorteios) - i >= 0:
            numeros_recentes.update(sorteios[len(sorteios) - i].get('numeros', []))

    # Se a maior probabilidade é de ter 1 ou 2 repetições:
    # Pegar nos números mais frequentes que apareceram nos sorteios recentes.
    # Se a maior probabilidade é de 0 repetições:
    # Pegar nos números mais frequentes que *não* apareceram nos sorteios recentes (os "frios" do momento).

    # Determine o número de repetições mais provável com base nas probabilidades.
    # Ex: a chave com a maior probabilidade em probabilidades_repeticoes
    num_repeticoes_mais_provavel = 0
    if probabilidades_repeticoes:
        num_repeticoes_mais_provavel = max(probabilidades_repeticoes, key=probabilidades_repeticoes.get)

    sugeridos = []
    
    if num_repeticoes_mais_provavel > 0: # Se é provável que haja repetições
        # Sugere os números mais frequentes dos sorteios recentes
        sugeridos.extend([num for num, _ in numeros_recentes.most_common(n)])
    else: # Se é provável que NÃO haja repetições (sorteio "novo")
        # Sugere os números mais frequentes que NÃO apareceram nos sorteios recentes
        todos_numeros = set(range(1, 50))
        numeros_recentes_set = set(numeros_recentes.keys())
        numeros_nao_recentes = list(todos_numeros - numeros_recentes_set)
        
        # Ordenar os não recentes pela frequência geral
        numeros_nao_recentes.sort(key=lambda x: frequencia_geral[x], reverse=True)
        sugeridos.extend(numeros_nao_recentes[:n])

    return {
        "nome": "repeticoes_sorteios_anteriores",
        "numeros": sorted(list(set(sugeridos)))[:n] # Garante n números únicos e ordenados
    }
