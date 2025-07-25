# avaliador.py
import os
import json
from collections import defaultdict

def carregar_resultados(caminho_resultados):
    with open(caminho_resultados, 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_previsoes(caminho_previsoes):
    with open(caminho_previsoes, 'r', encoding='utf-8') as f:
        return json.load(f)

def pontuar_heuristicas(resultado_real, detalhes):
    pontuacoes = defaultdict(list)

    for item in detalhes:
        heuristica = item["heuristica"]
        numeros = item["numeros"]
        score = 0

        for n in numeros:
            if n in resultado_real:
                score += 1  # Acerto direto
            elif any(abs(n - r) == 1 for r in resultado_real):
                score += 0.5  # Aproximação (±1)

        pontuacoes[heuristica].append(score)

    return pontuacoes

def calcular_pesos(pontuacoes, peso_base=1.0):
    media = {
        heuristica: sum(scores) / len(scores)
        for heuristica, scores in pontuacoes.items()
    }

    # Normaliza os valores entre 0.5 e 1.5
    max_score = max(media.values()) if media else 1.0
    pesos = {
        h: round((s / max_score) * peso_base + 0.5, 2)
        for h, s in media.items()
    }
    return pesos

def avaliar(caminho_resultado_real, caminho_previsoes, caminho_saida_pesos):
    dados_reais = carregar_resultados(caminho_resultado_real)
    dados_prev = carregar_previsoes(caminho_previsoes)

    resultado_real = dados_reais.get("numeros", [])
    detalhes = dados_prev.get("detalhes", [])

    pontuacoes = pontuar_heuristicas(resultado_real, detalhes)
    pesos_calculados = calcular_pesos(pontuacoes)

    with open(caminho_saida_pesos, 'w', encoding='utf-8') as f:
        json.dump(pesos_calculados, f, indent=2, ensure_ascii=False)

    print("Pesos atualizados com base na performance:")
    for heuristica, peso in pesos_calculados.items():
        print(f"→ {heuristica}: {peso}")

if __name__ == "__main__":
    avaliar(
        caminho_resultado_real="dados/sorteio_atual.json",
        caminho_previsoes="previsoes/previsao_atual.json",
        caminho_saida_pesos="decisor/pesos_atuais.json"
    )
