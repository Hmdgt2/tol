# heuristicas/soma_provavel.py
from collections import Counter
from itertools import combinations

DESCRICAO = "Sugere números cuja soma tende à soma mais frequente nos sorteios."

def prever(estatisticas, n=5):
    """
    Prevê números com base na soma mais provável dos sorteios.

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
            "nome": "soma_provavel",
            "numeros": []
        }

    # A sua lógica de combinations é ótima para prever 5, mas é lenta para 2.
    # Para n=2, vamos usar uma abordagem simplificada, mas que mantém a essência.
    # Vamos pegar nos números mais frequentes e verificar se a sua soma
    # está perto da soma mais comum, ajustada para 2 números.

    # Proporção da soma mais comum para 2 números (5 números na loteria)
    soma_ajustada = soma_mais_comum / 5 * 2
    
    # Define um pequeno intervalo em torno da soma ajustada
    intervalo_inferior = soma_ajustada * 0.9
    intervalo_superior = soma_ajustada * 1.1

    candidatos = [num for num, _ in Counter(frequencia).most_common(20)]
    melhores_combinacoes_de_2 = []
    
    # Gera combinações de 2 números e verifica se a soma está no intervalo
    for comb in combinations(candidatos, 2):
        if intervalo_inferior <= sum(comb) <= intervalo_superior:
            melhores_combinacoes_de_2.append(comb)
            if len(melhores_combinacoes_de_2) > 100: # Limita para performance
                break

    if melhores_combinacoes_de_2:
        contador_numeros = Counter()
        for comb in melhores_combinacoes_de_2:
            contador_numeros.update(comb)
        
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return {
            "nome": "soma_provavel",
            "numeros": sorted(sugeridos)
        }
    
    # Se não houver combinações, volta aos números mais frequentes
    return {
        "nome": "soma_provavel",
        "numeros": sorted([num for num, _ in Counter(frequencia).most_common(n)])
    }
