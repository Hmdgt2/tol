# heuristicas/numeros_retenção_longa.py
from collections import Counter

DESCRICAO = "Prioriza números que não saem há muitos sorteios, com base no histórico de ausência (gaps longos)."

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números que estão 'atrasados', ou seja, não saem há muito tempo.
    """
    ausencia = estatisticas.get('ausencia_atual', {})
    frequencia_total = estatisticas.get('frequencia_total', {})

    if not ausencia or not frequencia_total:
        return {"nome": "numeros_retenção_longa", "numeros": []}

    # Ordena os números pela ausência (gap) mais longo
    ausentes_mais_longo = sorted(ausencia.items(), key=lambda x: x[1], reverse=True)

    sugeridos = [num for num, _ in ausentes_mais_longo[:n]]

    # Se faltar algum número, completa com os mais frequentes
    if len(sugeridos) < n:
        freq_ordenada = sorted(frequencia_total.items(), key=lambda x: x[1], reverse=True)
        for num, _ in freq_ordenada:
            if num not in sugeridos:
                sugeridos.append(num)
                if len(sugeridos) == n:
                    break

    return {
        "nome": "numeros_retenção_longa",
        "numeros": sorted(sugeridos)
    }
