# heuristicas/pares_distantes.py
from collections import Counter

DESCRICAO = "Prioriza números que raramente saem juntos, aumentando a diversidade do jogo."

def prever(estatisticas, n=5):
    """
    Prevê números com base em pares de números que raramente saíram juntos,
    buscando maximizar a cobertura de combinações incomuns.
    """
    pares_frequentes = estatisticas.get('pares_frequentes', {})

    if not pares_frequentes:
        return {"nome": "pares_distantes", "numeros": []}

    # Identifica os pares menos frequentes
    pares_menos_frequentes = sorted(pares_frequentes.items(), key=lambda x: x[1])[:20]

    contador_numeros = Counter()
    for par, _ in pares_menos_frequentes:
        contador_numeros.update(par)

    sugeridos = [num for num, _ in contador_numeros.most_common(n)]

    return {
        "nome": "pares_distantes",
        "numeros": sorted(list(set(sugeridos)))
    }
