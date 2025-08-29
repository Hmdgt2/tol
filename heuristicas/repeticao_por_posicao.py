# heuristicas/repeticao_por_posicao.py
from collections import Counter

DESCRICAO = "Sugere números com base na frequência em cada posição do sorteio, aproveitando padrões posicionais."

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base na repetição de números em posições específicas do sorteio.
    """
    if not sorteios_historico:
        return {"nome": "repeticao_por_posicao", "numeros": []}

    posicoes = len(sorteios_historico[0].get('numeros', []))
    contador_posicoes = [Counter() for _ in range(posicoes)]

    for s in sorteios_historico:
        numeros = s.get('numeros', [])
        for i, num in enumerate(numeros):
            contador_posicoes[i][num] += 1

    sugeridos = []
    for contador in contador_posicoes:
        if contador:
            num_mais_frequente = contador.most_common(1)[0][0]
            if num_mais_frequente not in sugeridos:
                sugeridos.append(num_mais_frequente)
        if len(sugeridos) >= n:
            break

    # Se não houver números suficientes, completa com os mais frequentes no geral
    if len(sugeridos) < n:
        frequencia_total = estatisticas.get('frequencia_total', {})
        para_completar = [num for num, _ in Counter(frequencia_total).most_common(n)]
        for num in para_completar:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "nome": "repeticao_por_posicao",
        "numeros": sorted(sugeridos)
    }
