# heuristicas/frequencia_soma.py
from collections import Counter
from itertools import combinations

DESCRICAO = "Sugere números que ajudam a formar a soma mais frequente dos sorteios."

# Nota: analisa a soma total dos números sorteados e escolhe os que mais contribuem
# para a soma considerada mais comum ao longo do histórico.


def prever(estatisticas, n=5):
    """
    Prevê números com base na soma mais frequente dos sorteios.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    soma_mais_comum = estatisticas.get('soma_mais_comum', 0)
    frequencia = estatisticas.get('frequencia_total', {})

    if not frequencia or soma_mais_comum == 0:
        return {
            "nome": "frequencia_soma",
            "numeros": []
        }

    # A lógica original com 'combinations' é muito pesada para um backtesting eficiente.
    # Vamos simplificar, priorizando números que contribuíram para a soma mais comum.
    # Abordagem:
    # 1. Encontrar os números mais frequentes.
    # 2. Selecionar aqueles que, ao serem somados, tendem a atingir a soma mais comum.
    #    Vamos focar nos números mais frequentes que são "candidatos" a essa soma.

    # Esta versão otimizada simplesmente retorna os números mais frequentes que estão
    # dentro de uma faixa de soma que tende a ser a mais comum.

    # Em vez de gerar todas as combinações, vamos pegar nos números mais frequentes
    # e verificar se eles se encaixam na soma.

    # Seleciona os números mais frequentes para o nosso conjunto de candidatos
    candidatos = [num for num, _ in Counter(frequencia).most_common(20)]
    
    melhores_combinacoes = []
    
    # Cria combinações de 2 números e verifica a soma.
    # Esta é uma otimização para a sua heurística de 'n=2'.
    for comb in combinations(candidatos, 2):
        if sum(comb) == soma_mais_comum // (49/5): # Proporção da soma
            melhores_combinacoes.append(comb)
            
    # Se encontramos combinações que se encaixam na soma, sugerimos os números mais comuns nessas combinações.
    if melhores_combinacoes:
        contador_numeros_comb = Counter()
        for comb in melhores_combinacoes:
            contador_numeros_comb.update(comb)
        
        sugeridos = [num for num, _ in contador_numeros_comb.most_common(n)]
        
        return {
            "nome": "frequencia_soma",
            "numeros": sorted(sugeridos)
        }
    
    # Se não houver combinações, recorre aos números mais frequentes
    return {
        "nome": "frequencia_soma",
        "numeros": sorted([num for num, _ in Counter(frequencia).most_common(n)])
    }
