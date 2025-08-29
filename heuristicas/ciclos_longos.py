# heuristicas/ciclos_longos.py
from collections import defaultdict

DESCRICAO = "Sugere números que estão atrasados em relação ao seu ciclo histórico, com base no intervalo médio entre aparições."

def prever(estatisticas, sorteios_historico, n=5):
    """
    Prevê números com base nos ciclos longos.
    """
    if not sorteios_historico:
        return {"nome": "ciclos_longos", "numeros": []}

    ultimos_indices = defaultdict(list)
    for idx, s in enumerate(sorteios_historico):
        for num in s.get('numeros', []):
            ultimos_indices[num].append(idx)
    
    gaps_medios = {}
    for num, indices in ultimos_indices.items():
        if len(indices) < 2:
            continue
        gaps = [j - i for i, j in zip(indices[:-1], indices[1:])]
        gaps_medios[num] = sum(gaps) / len(gaps)
    
    sorteio_atual = len(sorteios_historico)
    atraso = {num: sorteio_atual - indices[-1] for num, indices in ultimos_indices.items()}

    score = {num: atraso[num] / gaps_medios.get(num, 1) for num in atraso}

    sugeridos = sorted(score, key=score.get, reverse=True)[:n]

    return {
        "nome": "ciclos_longos",
        "numeros": sorted(sugeridos)
    }
