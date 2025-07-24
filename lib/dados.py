# gerar_previsao.py
import importlib
import os
import json

HEURISTICAS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'heuristicas'))
PASTA_PREVISOES = os.path.abspath(os.path.join(os.path.dirname(__file__), 'previsoes')) # Use os.path.abspath aqui também
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')


def carregar_heuristicas():
    heuristicas = []
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    heuristicas.append((nome_modulo, modulo.prever))
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
    return heuristicas


def combinar_resultados(sugestoes):
    from collections import Counter
    contador = Counter()
    for lista_numeros in sugestoes: # Alterado de 'dupla' para 'lista_numeros' para maior clareza
        contador.update(lista_numeros)
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
            # *** MUDANÇA IMPORTANTE AQUI: Passa n=2 para as funções prever ***
            resultado_heuristica = funcao(sorteios, n=2)
            numeros = resultado_heuristica.get("numeros", [])
            # *** AJUSTE NA FORMATAÇÃO PARA MAIOR CLAREZA ***
            print(f"{nome:<35}: {numeros}")
            sugestoes.append(numeros)
            detalhes.append({"heuristica": nome, "numeros": numeros})
        except Exception as e:
            # *** AJUSTE NA FORMATAÇÃO PARA MAIOR CLAREZA NO ERRO ***
            print(f"Erro na heurística {nome:<35}: {e}")

    combinados = combinar_resultados(sugestoes)
    print("\n---") # Adicionado separador para destacar o resultado final
    print("Sugestão final (combinada):", combinados)
    print("---") # Adicionado separador

    guardar_previsao_json(combinados, detalhes)


if __name__ == '__main__':
    gerar_previsao()
