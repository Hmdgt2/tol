# gerar_previsao.py
import importlib
import os
import json
import sys # Importa o módulo sys

# Adiciona o diretório raiz do projeto ao sys.path
# Isso permite que as importações como 'from lib.dados import ...' funcionem corretamente
# Assumimos que 'lib' e 'heuristicas' estão no mesmo nível do 'gerar_previsao.py'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios # Esta linha agora deve funcionar

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas') # Usa PROJECT_ROOT
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')   # Usa PROJECT_ROOT
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')


def carregar_heuristicas():
    heuristicas = []
    # Cria um pacote Python temporário para importação dinâmica, se necessário
    # ou garante que o diretório 'heuristicas' é um pacote.
    # Neste cenário, a importação direta 'heuristicas.nome_modulo' funciona melhor
    # se o diretório raiz do projeto estiver no sys.path.

    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                # O importlib.import_module espera um nome de módulo completo.
                # Como adicionamos o PROJECT_ROOT ao sys.path, 'heuristicas' é agora um pacote.
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    heuristicas.append((nome_modulo, modulo.prever))
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
            except Exception as e:
                print(f"Erro inesperado ao carregar heurística {nome_modulo}: {e}")
    return heuristicas


def combinar_resultados(sugestoes):
    from collections import Counter
    contador = Counter()
    for lista_numeros in sugestoes:
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
            resultado_heuristica = funcao(sorteios, n=2)
            numeros = resultado_heuristica.get("numeros", [])
            print(f"{nome:<35}: {numeros}")
            sugestoes.append(numeros)
            detalhes.append({"heuristica": nome, "numeros": numeros})
        except Exception as e:
            print(f"Erro na heurística {nome:<35}: {e}")

    combinados = combinar_resultados(sugestoes)
    print("\n---")
    print("Sugestão final (combinada):", combinados)
    print("---")

    guardar_previsao_json(combinados, detalhes)


if __name__ == '__main__':
    gerar_previsao()
