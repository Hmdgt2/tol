# heuristicas/ausencia_superior_media.py

from lib.dados import carregar_sorteios, calcular_ausencia_atual

def ausencia_superior_media(n=2):
    sorteios = carregar_sorteios()
    ausencia = calcular_ausencia_atual(sorteios)

    media = sum(ausencia.values()) / len(ausencia)
    candidatos = [num for num, dias in ausencia.items() if dias > media]
    return sorted(candidatos, key=lambda x: ausencia[x], reverse=True)[:n]
