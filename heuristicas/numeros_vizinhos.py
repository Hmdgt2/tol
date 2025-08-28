# heuristicas/numeros_vizinhos.py
from collections import defaultdict, Counter

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base na frequência de vizinhos sorteados em sorteios recentes.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    if not sorteios_historico or len(sorteios_historico) < 2:
        return {
            "nome": "numeros_vizinhos",
            "numeros": []
        }

    frequencia_vizinhos = Counter()
    
    # Análise dos últimos 50 sorteios
    periodo_analise = 50
    historico_recente = sorteios_historico[-periodo_analise:]

    for i in range(len(historico_recente) - 1):
        sorteio_atual = set(historico_recente[i].get('numeros', []))
        sorteio_seguinte = set(historico_recente[i+1].get('numeros', []))
        
        for num_atual in sorteio_atual:
            vizinho_esq = num_atual - 1
            vizinho_dir = num_atual + 1
            
            # Conta se o vizinho apareceu no próximo sorteio
            if vizinho_esq > 0 and vizinho_esq in sorteio_seguinte:
                frequencia_vizinhos[vizinho_esq] += 1
            if vizinho_dir < 50 and vizinho_dir in sorteio_seguinte:
                frequencia_vizinhos[vizinho_dir] += 1

    # Sugere os números vizinhos mais frequentes
    sugeridos = [num for num, _ in frequencia_vizinhos.most_common(n)]

    # Se não houver vizinhos frequentes, voltar para a heurística de números quentes
    if not sugeridos:
        numeros_quentes = estatisticas.get('numeros_quentes', [])
        sugeridos.extend(numeros_quentes[:n])

    return {
        "nome": "numeros_vizinhos",
        "numeros": sorted(list(set(sugeridos)))
    }
