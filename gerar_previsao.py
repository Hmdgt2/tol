import importlib
import os
import json
import sys
import inspect
from collections import defaultdict, Counter
from itertools import combinations
from decisor.decisor_final import HeuristicDecisor
from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios

# Define o caminho para a pasta de heurísticas e previsões
# Adicione esta linha para garantir que o caminho base está correto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')

# Corrija esta linha para usar o PROJECT_ROOT
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

    estatisticas = get_all_stats(sorteios_historico)
    estatisticas['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(sorteios_historico, num_sorteios=100)
    
    print("\n--- Previsões das Heurísticas ---\n")
    detalhes_previsoes = []

    for nome, funcao in heuristicas:
        try:
            parametros = inspect.signature(funcao).parameters
            if 'sorteios_historico' in parametros:
                resultado_heuristica = funcao(estatisticas, sorteios_historico, n=5)
            else:
                resultado_heuristica = funcao(estatisticas, n=5)
            
            numeros = resultado_heuristica.get("numeros", [])
            print(f"{nome:<35}: {numeros}")
            detalhes_previsoes.append({"nome": nome, "numeros": numeros})
        except Exception as e:
            print(f"Erro na heurística {nome:<35}: {e}")

    print("\n--- Sugestão Final ---")
    
    try:
        # Tenta carregar o ficheiro de pesos
        with open(PESOS_PATH, 'r', encoding='utf-8') as f:
            pesos_json = json.load(f)
        
        caminho_modelo_gb = pesos_json['modelos'].get('gradient_boosting')
        caminho_modelo_rf = pesos_json['modelos'].get('random_forest')
        
        if not caminho_modelo_gb or not caminho_modelo_rf:
            print("Erro: Caminhos dos modelos não encontrados no ficheiro de pesos. A sair.")
            return

        # Corrija aqui também para usar PROJECT_ROOT
        caminho_completo_gb = os.path.join(PROJECT_ROOT, caminho_modelo_gb)
        caminho_completo_rf = os.path.join(PROJECT_ROOT, caminho_modelo_rf)
        
        decisor = HeuristicDecisor(
            caminho_pesos_json=PESOS_PATH, 
            caminho_modelo_joblib_gb=caminho_completo_gb,
            caminho_modelo_joblib_rf=caminho_completo_rf
        )
        previsao_final = decisor.predict(detalhes_previsoes)
        
        print("Previsão Final (combinada):", sorted(previsao_final))
        print("---")
        
        guardar_previsao_json(sorted(previsao_final), detalhes_previsoes)

    except FileNotFoundError:
        print(f"Erro: O ficheiro de pesos '{PESOS_PATH}' não foi encontrado. Por favor, treine o decisor primeiro.")
        
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
