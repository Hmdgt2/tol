# decisor_final.py
import os
import json
from collections import defaultdict

def decidir_final(detalhes, caminho_pesos=None):
    pesos = {}
    if caminho_pesos and os.path.exists(caminho_pesos):
        with open(caminho_pesos, 'r', encoding='utf-8') as f:
            pesos = json.load(f)

    pontuacoes = defaultdict(float)
    for item in detalhes:
        nome = item["heuristica"]
        numeros = item["numeros"]
        peso = pesos.get(nome, 1.0)
        for num in numeros:
            pontuacoes[num] += peso

    escolhidos = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    return [num for num, _ in escolhidos[:2]]
