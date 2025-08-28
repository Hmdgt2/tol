# heuristicas/quentes_frios.py
from collections import Counter

def prever(estatisticas, sorteios_historico, n=2, janela_quentes=15):
    """
    Prevê números com base nos números "quentes" (mais frequentes recentemente)
    e "frios" (mais ausentes).

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise
                                  de números "quentes".
        n (int): O número de sugestões a retornar.
        janela_quentes (int): O número de sorteios recentes para considerar.
    
    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    if len(sorteios_historico) < janela_quentes:
        janela_quentes = len(sorteios_historico)

    sorteios_recentes = sorteios_historico[-janela_quentes:]
    
    # Recalcula a frequência para a janela "quente"
    contador_quentes = Counter()
    for s in sorteios_recentes:
        contador_quentes.update(s.get('numeros', []))

    numeros_quentes = [num for num, _ in contador_quentes.most_common(n)]
    
    # Usa a ausência pré-calculada
    ausencia = estatisticas.get('ausencia_atual', {})
    numeros_frios = sorted(ausencia, key=ausencia.get, reverse=True)[:n]

    # Combina os dois, garantindo que não haja duplicados
    sugeridos = list(set(numeros_quentes + numeros_frios))
    
    # Garante que a lista tenha pelo menos n números, se possível
    if len(sugeridos) < n:
        frequencia_geral = estatisticas.get('frequencia_total', {})
        todos_frequentes = [num for num, _ in Counter(frequencia_geral).most_common()]
        for num in todos_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return {
        "nome": "quentes_frios",
        "numeros": sorted(list(set(sugeridos)))
    }
