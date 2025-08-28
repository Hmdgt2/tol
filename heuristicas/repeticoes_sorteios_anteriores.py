# heuristicas/repeticoes_sorteios_anteriores.py
from collections import Counter

def prever(estatisticas, sorteios_historico, n=2, num_sorteios_anteriores=5):
    """
    Prevê números com base na probabilidade de repetição de números de sorteios anteriores.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise.
        n (int): O número de sugestões a retornar.
        num_sorteios_anteriores (int): O número de sorteios anteriores a analisar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    probabilidades_repeticoes = estatisticas.get('repeticoes_ultimos_sorteios', {})
    frequencia_geral = estatisticas.get('frequencia_total', {})
    
    if not probabilidades_repeticoes or not frequencia_geral or len(sorteios_historico) < num_sorteios_anteriores:
        return {
            "nome": "repeticoes_sorteios_anteriores",
            "numeros": []
        }
    
    # Identifica o número de repetições mais provável
    num_repeticoes_mais_provavel = max(probabilidades_repeticoes, key=probabilidades_repeticoes.get, default=0)
    
    # Obtém os números dos últimos sorteios
    numeros_recentes = Counter()
    for i in range(1, num_sorteios_anteriores + 1):
        numeros_recentes.update(sorteios_historico[len(sorteios_historico) - i].get('numeros', []))

    sugeridos = []
    
    if num_repeticoes_mais_provavel > 0:
        # Se é provável que haja repetições, sugere os números mais frequentes dos sorteios recentes
        sugeridos.extend([num for num, _ in numeros_recentes.most_common(n)])
    else:
        # Se é provável que NÃO haja repetições
        todos_numeros = set(range(1, 50))
        numeros_recentes_set = set(numeros_recentes.keys())
        numeros_nao_recentes = list(todos_numeros - numeros_recentes_set)
        
        # Ordena os não recentes pela frequência geral
        numeros_nao_recentes.sort(key=lambda x: frequencia_geral.get(x, 0), reverse=True)
        sugeridos.extend(numeros_nao_recentes[:n])
    
    # Fallback para garantir que sempre retorna n números
    if len(sugeridos) < n:
        todos_frequentes_geral = [num for num, _ in Counter(frequencia_geral).most_common()]
        for num in todos_frequentes_geral:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "nome": "repeticoes_sorteios_anteriores",
        "numeros": sorted(list(set(sugeridos)))
    }
