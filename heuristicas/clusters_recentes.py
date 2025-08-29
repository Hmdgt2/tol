# heuristicas/clusters_recentes.py
from collections import Counter

DESCRICAO = "Prioriza grupos de números que saíram juntos recentemente, capturando pequenos clusters ou padrões."

def prever(estatisticas, sorteios_historico, n=5, janela=10):
    """
    Prevê números com base em clusters recentes — números que apareceram juntos nos últimos sorteios.
    """
    if not sorteios_historico:
        return {"nome": "clusters_recentes", "numeros": []}

    # Ajusta a janela de análise se necessário
    if len(sorteios_historico) < janela:
        janela = len(sorteios_historico)

    ultimos_sorteios = sorteios_historico[-janela:]

    contador_clusters = Counter()
    for s in ultimos_sorteios:
        numeros = s.get('numeros', [])
        # Conta todos os pares dentro do sorteio (combinações de 2)
        for i in range(len(numeros)):
            for j in range(i + 1, len(numeros)):
                par = tuple(sorted((numeros[i], numeros[j])))
                contador_clusters[par] += 1

    # Seleciona os pares mais frequentes
    pares_mais_frequentes = [par for par, _ in contador_clusters.most_common(10)]

    contador_numeros = Counter()
    for par in pares_mais_frequentes:
        contador_numeros.update(par)

    sugeridos = [num for num, _ in contador_numeros.most_common(n)]

    return {
        "nome": "clusters_recentes",
        "numeros": sorted(list(set(sugeridos)))
    }
