# heuristicas/padrao_finais.py
from collections import Counter

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base na frequência das terminações que coincidiram
    com o último sorteio.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise
                                  do padrão.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    frequencia_total = estatisticas.get('frequencia_total', {})

    if len(sorteios_historico) < 2 or not frequencia_total:
        return {
            "nome": "padrao_finais",
            "numeros": []
        }

    ultimos_numeros = sorteios_historico[-1].get('numeros', [])
    ultimas_terminacoes = {num % 10 for num in ultimos_numeros}
    
    contador_finais = Counter()
    
    # Este loop ainda é necessário, pois a lógica depende de um sorteio para o outro
    for s in sorteios_historico[:-1]:
        terminacoes_atuais = {num % 10 for num in s.get('numeros', [])}
        for term in ultimas_terminacoes:
            if term in terminacoes_atuais:
                contador_finais[term] += 1
    
    terminacoes_comuns = [t for t, _ in contador_finais.most_common(2)]
    
    candidatos = []
    # Usar a frequência total pré-calculada para a ordem de preferência
    frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
    
    for num, _ in frequencia_ordenada:
        if (num % 10) in terminacoes_comuns:
            candidatos.append(num)
            if len(candidatos) >= n:
                break
    
    if len(candidatos) < n: # Fallback se não houver candidatos suficientes
        sugeridos = [num for num, _ in frequencia_ordenada[:n]]
    else:
        sugeridos = candidatos
    
    return {
        "nome": "padrao_finais",
        "numeros": sorted(list(set(sugeridos)))
    }
