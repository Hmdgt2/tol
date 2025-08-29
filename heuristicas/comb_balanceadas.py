# heuristicas/comb_balanceadas.py
from collections import Counter

DESCRICAO = "Sugere combinações que equilibram números pares e ímpares, altos e baixos, com base em padrões históricos."

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base em combinações balanceadas de paridade e posição.
    """
    if not sorteios_historico:
        return {"nome": "comb_balanceadas", "numeros": []}

    frequencia_total = estatisticas.get('frequencia_total', {})
    if not frequencia_total:
        return {"nome": "comb_balanceadas", "numeros": []}

    # Divide números em pares/ímpares
    pares = [num for num in frequencia_total if num % 2 == 0]
    impares = [num for num in frequencia_total if num % 2 != 0]

    # Divide números em altos/baixos (1-24 baixos, 25-49 altos)
    baixos = [num for num in frequencia_total if num <= 24]
    altos = [num for num in frequencia_total if num >= 25]

    # Seleciona os mais frequentes de cada categoria
    freq_ordenada = sorted(frequencia_total.items(), key=lambda x: x[1], reverse=True)
    
    sugeridos = []
    for grupo in [pares, impares, baixos, altos]:
        for num, _ in freq_ordenada:
            if num in grupo and num not in sugeridos:
                sugeridos.append(num)
                if len(sugeridos) >= n:
                    break
        if len(sugeridos) >= n:
            break

    # Se faltar algum número, completa com os mais frequentes restantes
    if len(sugeridos) < n:
        for num, _ in freq_ordenada:
            if num not in sugeridos:
                sugeridos.append(num)
                if len(sugeridos) == n:
                    break

    return {
        "nome": "comb_balanceadas",
        "numeros": sorted(sugeridos)
    }
