# heuristicas/distribuicao_quadrantes.py
from collections import Counter

def prever(estatisticas, n=5):
    """
    Prevê números com base na distribuição mais frequente por quadrantes.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        n (int): O número de sugestões a retornar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    # Acessa diretamente as estatísticas de distribuição de quadrantes e frequência total
    padrao_ideal_quadrantes = estatisticas.get('distribuicao_quadrantes', (0, 0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return {
            "nome": "distribuicao_quadrantes",
            "numeros": []
        }

    # Ordena os quadrantes pela contagem ideal
    quadrantes_ordenados = sorted(
        enumerate(padrao_ideal_quadrantes),
        key=lambda item: item[1],
        reverse=True
    )

    sugeridos = []
    tamanho_quadrante = 49 // 4
    
    # Itera sobre os quadrantes mais frequentes no padrão ideal
    for idx_quadrante, _ in quadrantes_ordenados:
        limite_inferior = idx_quadrante * tamanho_quadrante + 1
        limite_superior = (idx_quadrante + 1) * tamanho_quadrante
        if idx_quadrante == 3: # Último quadrante vai até 49
            limite_superior = 49

        # Encontra os números mais frequentes nessa faixa
        candidatos_no_quadrante = sorted(
            [num for num, _ in frequencia.items() if limite_inferior <= num <= limite_superior],
            key=lambda num: frequencia[num],
            reverse=True
        )
        
        # Adiciona o número mais frequente deste quadrante, se houver
        if candidatos_no_quadrante and candidatos_no_quadrante[0] not in sugeridos:
            sugeridos.append(candidatos_no_quadrante[0])
            if len(sugeridos) >= n:
                break

    # Se a lista de sugestões ainda não tiver 'n' números, preenche com os mais frequentes no geral
    while len(sugeridos) < n:
        todos_mais_frequentes = [num for num, _ in Counter(frequencia).most_common(len(frequencia))]
        for num in todos_mais_frequentes:
            if num not in sugeridos:
                sugeridos.append(num)
                if len(sugeridos) == n:
                    break
    
    return {
        "nome": "distribuicao_quadrantes",
        "numeros": sorted(sugeridos)
    }
