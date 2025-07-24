# heuristicas/ausencia_superior_media.py
from lib.dados import calcular_ausencia_atual

def prever(sorteios, n=2):
    ausencia = calcular_ausencia_atual(sorteios)
    media = sum(ausencia.values()) / len(ausencia)
    candidatos = [num for num, dias in ausencia.items() if dias > media]
    sugeridos = sorted(candidatos, key=lambda x: ausencia[x], reverse=True)[:n]
    return {
        "nome": "ausencia_superior_media",
        "numeros": sugeridos
    }
