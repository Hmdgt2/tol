import importlib
import os
import json
import sys
from collections import defaultdict, Counter
from itertools import combinations

# Adicione a nova função aqui para que possa ser usada
from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios
from decisor.decisor_final import HeuristicDecisor

# Define o caminho para a pasta de heurísticas e previsões
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')
PESOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')

def carregar_heuristicas():
    """Carrega dinamicamente todas as funções 'prever' do diretório de heurísticas."""
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
            except Exception as e:
                print(f"Erro inesperado ao carregar heurística {nome_modulo}: {e}")
    return heuristicas

def gerar_previsao():
    """
    Gera uma previsão de números com base em múltiplas heurísticas
    e um decisor ponderado.
    """
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico:
        print("Erro: Nenhum sorteio histórico encontrado. Não é possível gerar uma previsão.")
        return

    # Calcula todas as estatísticas uma única vez
    estatisticas = get_all_stats(sorteios_historico)
    # Adição da chamada para a nova função de estatísticas de repetição
    estatisticas['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(sorteios_historico, num_sorteios=100)
    
    print("\n--- Previsões das Heurísticas ---\n")
    detalhes_previsoes = []

    # Executa todas as heurísticas e armazena os resultados
    for nome, funcao in heuristicas:
        try:
            # Algumas heurísticas precisam do histórico completo
            if nome in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes']:
                resultado_heuristica = funcao(estatisticas, sorteios_historico, n=5)
            else:
                resultado_heuristica = funcao(estatisticas, n=5)
            
            numeros = resultado_heuristica.get("numeros", [])
            print(f"{nome:<35}: {numeros}")
            detalhes_previsoes.append({"nome": nome, "numeros": numeros})
        except Exception as e:
            print(f"Erro na heurística {nome:<35}: {e}")

    # Usa o decisor final para combinar os resultados
    print("\n--- Sugestão Final ---")
    decisor = HeuristicDecisor(caminho_pesos=PESOS_PATH)
    previsao_final = decisor.predict(detalhes_previsoes)
    
    print("Previsão Final (combinada):", sorted(previsao_final))
    print("---")

    # Guardar a previsão e os detalhes
    guardar_previsao_json(sorted(previsao_final), detalhes_previsoes)

def guardar_previsao_json(combinados, detalhes):
    """Guarda a previsão final e os detalhes das heurísticas em um arquivo JSON."""
    os.makedirs(PASTA_PREVISOES, exist_ok=True)
    dados = {
        "previsao": combinados,
        "detalhes": detalhes
    }
    with open(FICHEIRO_PREVISAO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    gerar_previsao()
