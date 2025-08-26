from collections import Counter
from lib.dados import contar_ocorrencias, calcular_ausencia_atual

def prever(sorteios, n=2, janela_quentes=15):
    if len(sorteios) < 2:
        return {"nome": "quentes_frios", "numeros": []}

    sorteios_recentes = sorteios[-janela_quentes:]
    
    # Números quentes (os mais frequentes recentemente)
    contador_quentes = contar_ocorrencias(sorteios_recentes)
    numeros_quentes = [num for num, _ in contador_quentes.most_common(n)]
    
    # Números frios (os mais ausentes)
    ausencia = calcular_ausencia_atual(sorteios)
    numeros_frios = sorted(ausencia, key=ausencia.get, reverse=True)[:n]

    # Combina os dois, garantindo que não haja duplicados
    sugeridos = list(set(numeros_quentes + numeros_frios))
    
    if len(sugeridos) < n:
        # Se a combinação não gerar n números, complementa com os mais frequentes no geral
        frequencia_geral = contar_ocorrencias(sorteios)
        todos_frequentes = [num for num, _ in frequencia_geral.most_common()]
        for num in todos_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "heuristicas": "quentes_frios",
        "numeros": sorted(list(set(sugeridos)))[:n]
    }
