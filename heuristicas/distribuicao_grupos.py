# heuristicas/distribuicao_grupos.py
from collections import Counter

def prever(estatisticas, n=5):
    """
    Prevê números com base na distribuição mais frequente por grupos (dezenas).

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    # Acessa diretamente as estatísticas de distribuição de dezenas e frequência total
    padrao_ideal = estatisticas.get('distribuicao_dezenas', (0, 0, 0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return {
            "nome": "distribuicao_grupos",
            "numeros": []
        }

    # Ordena os grupos pela contagem ideal
    grupos_ordenados = sorted(
        enumerate(padrao_ideal),
        key=lambda item: item[1],
        reverse=True
    )

    sugeridos = []
    faixas = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 49)]

    # Itera sobre os grupos mais frequentes
    for idx_grupo, _ in grupos_ordenados:
        limite_inferior, limite_superior = faixas[idx_grupo]

        # Encontra os números mais frequentes nessa faixa
        candidatos_na_faixa = sorted(
            [num for num, _ in frequencia.items() if limite_inferior <= num <= limite_superior],
            key=lambda num: frequencia[num],
            reverse=True
        )
        
        # Adiciona o número mais frequente dessa faixa, se ele não estiver já na lista
        if candidatos_na_faixa and candidatos_na_faixa[0] not in sugeridos:
            sugeridos.append(candidatos_na_faixa[0])
            if len(sugeridos) >= n:
                break

    # Se a lista ainda não tiver n números, preenche com os mais frequentes
    if len(sugeridos) < n:
        todos_mais_frequentes = [num for num, _ in Counter(frequencia).most_common(len(frequencia))]
        for num in todos_mais_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)
    
    return {
        "nome": "distribuicao_grupos",
        "numeros": sorted(list(set(sugeridos)))
    }
