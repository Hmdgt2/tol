# heuristicas/distribuicao_uniforme_faixas.py
from collections import Counter

DESCRICAO = "Sugere números distribuídos de forma equilibrada entre as faixas do jogo, evitando concentrações."

def prever(estatisticas, n=5):
    """
    Prevê números garantindo distribuição uniforme entre as faixas do jogo.
    """
    frequencia_total = estatisticas.get('frequencia_total', {})

    if not frequencia_total:
        return {"nome": "distribuicao_uniforme_faixas", "numeros": []}

    # Definindo faixas
    faixas = [(1,10), (11,20), (21,30), (31,40), (41,49)]
    numeros_sugeridos = []

    for inicio, fim in faixas:
        candidatos = [num for num in range(inicio, fim+1) if num in frequencia_total]
        if candidatos:
            # Escolhe o número mais frequente na faixa
            mais_frequente = max(candidatos, key=lambda x: frequencia_total[x])
            numeros_sugeridos.append(mais_frequente)
        if len(numeros_sugeridos) >= n:
            break

    # Se ainda faltar completar n números, adiciona os mais frequentes gerais
    if len(numeros_sugeridos) < n:
        restantes = [num for num, _ in Counter(frequencia_total).most_common(n)]
        for num in restantes:
            if num not in numeros_sugeridos and len(numeros_sugeridos) < n:
                numeros_sugeridos.append(num)

    return {
        "nome": "distribuicao_uniforme_faixas",
        "numeros": sorted(numeros_sugeridos)
    }
