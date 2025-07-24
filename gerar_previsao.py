# gerar_previsao.py
import importlib
import os
import json
from lib.dados import carregar_sorteios

HEURISTICAS_DIR = os.path.join(os.path.dirname(__file__), 'heuristicas')
PASTA_PREVISOES = os.path.join(os.path.dirname(__file__), 'previsoes')
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')


def carregar_heuristicas():
    heuristicas = []
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
            if hasattr(modulo, 'prever'):
                heuristicas.append((nome_modulo, modulo.prever))
    return heuristicas


def combinar_resultados(sugestoes):
    from collections import Counter
    contador = Counter()
    for dupla in sugestoes:
        contador.update(dupla)
    mais_comuns = [num for num, _ in contador.most_common(2)]
    return sorted(mais_comuns)


def guardar_previsao_json(combinados, detalhes):
    os.makedirs(PASTA_PREVISOES, exist_ok=True)
    dados = {
        "previsao": combinados,
        "detalhes": detalhes
    }
    with open(FICHEIRO_PREVISAO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def gerar_previsao():
    sorteios = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    print("\nPrevisão com base em heurísticas:\n")
    sugestoes = []
    detalhes = []

    for nome, funcao in heuristicas:
        try:
            resultado = funcao(sorteios)
            numeros = resultado if isinstance(resultado, list) else resultado.get("numeros", [])
            print(f"{nome:<25}: {numeros}")
            sugestoes.append(numeros)
            detalhes.append({"heuristica": nome, "numeros": numeros})
        except Exception as e:
            print(f"Erro na heurística {nome}: {e}")

    combinados = combinar_resultados(sugestoes)
    print("\nSugestão final (combinada):", combinados)

    guardar_previsao_json(combinados, detalhes)


if __name__ == '__main__':
    gerar_previsao()
