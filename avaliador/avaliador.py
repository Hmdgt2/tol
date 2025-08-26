import os
import json
from collections import defaultdict, deque

HISTORICO_PATH = "decisor/historico_performance.json"
PESOS_PATH = "decisor/pesos_atuais.json"
N_MOVEL = 5  # Número de sorteios considerados na média móvel

def carregar_resultados(caminho_resultados):
    with open(caminho_resultados, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_previsoes(caminho_previsoes):
    with open(caminho_previsoes, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_historico(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def guardar_historico(historico, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def pontuar_heuristicas(resultado_real, detalhes):
    pontuacoes = defaultdict(float)
    for item in detalhes:
        heuristica = item["heuristica"]
        numeros = item["numeros"]
        score = 0
        num_acertos = 0
        num_aproximacoes = 0
        for n in numeros:
            if n in resultado_real:
                score += 2  # Acerto direto mais valioso
                num_acertos += 1
            elif any(abs(n - r) == 1 for r in resultado_real):
                score += 1  # Aproximação ±1
                num_aproximacoes += 1
        # Bónus por acertos múltiplos
        if num_acertos > 1:
            score += (num_acertos - 1) * 0.5
        pontuacoes[heuristica] = score
    return pontuacoes

def atualizar_historico(historico, pontuacoes):
    for heuristica, score in pontuacoes.items():
        arr = historico.get(heuristica, [])
        arr.append(score)
        if len(arr) > N_MOVEL:
            arr = arr[-N_MOVEL:]
        historico[heuristica] = arr
    return historico

def calcular_pesos(historico, peso_base=1.0):
    # Média móvel dos últimos N_MOVEL sorteios
    medias = {}
    for heuristica, scores in historico.items():
        if scores:
            medias[heuristica] = sum(scores) / len(scores)
        else:
            medias[heuristica] = 0.0
    max_score = max(medias.values()) if medias else 1.0
    if max_score == 0:
        max_score = 1.0
    pesos = {
        h: round((s / max_score) * peso_base + 0.5, 2)
        for h, s in medias.items()
    }
    return pesos

def avaliar(caminho_resultado_real, caminho_previsoes, caminho_historico, caminho_saida_pesos):
    dados_reais = carregar_resultados(caminho_resultado_real)
    dados_prev = carregar_previsoes(caminho_previsoes)

    resultado_real = dados_reais.get("numeros", [])
    detalhes = dados_prev.get("detalhes", [])

    pontuacoes = pontuar_heuristicas(resultado_real, detalhes)
    historico = carregar_historico(caminho_historico)
    historico = atualizar_historico(historico, pontuacoes)
    guardar_historico(historico, caminho_historico)
    pesos_calculados = calcular_pesos(historico)

    with open(caminho_saida_pesos, 'w', encoding='utf-8') as f:
        json.dump(pesos_calculados, f, indent=2, ensure_ascii=False)

    print("Pesos atualizados (média móvel dos últimos {} sorteios):".format(N_MOVEL))
    for heuristica, peso in pesos_calculados.items():
        print(f"→ {heuristica}: {peso} (histórico: {historico.get(heuristica, [])})")

if __name__ == "__main__":
    avaliar(
        caminho_resultado_real="dados/sorteio_atual.json",
        caminho_previsoes="previsoes/previsao_atual.json",
        caminho_historico=HISTORICO_PATH,
        caminho_saida_pesos=PESOS_PATH
    )
