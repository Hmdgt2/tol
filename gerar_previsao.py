# gerar_previsao.py
import importlib
import os
import json
import sys
import inspect
from typing import Dict, Any, List
from collections import defaultdict, Counter
from decisor.decisor_final import HeuristicDecisor
from lib.dados import _carregar_sorteios, obter_estatisticas, salvar_estatisticas, carregar_estatisticas

# Define os caminhos
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')
PESOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')

def carregar_heuristicas() -> Dict[str, Any]:
    """
    Carrega dinamicamente todas as heurísticas e suas dependências.
    Retorna um dicionário { nome: { "funcao": funcao, "dependencias": set } }
    """
    heuristicas = {}
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever') and hasattr(modulo, 'DEPENDENCIAS'):
                    heuristicas[nome_modulo] = {
                        "funcao": modulo.prever,
                        "dependencias": set(modulo.DEPENDENCIAS)
                    }
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
            except Exception as e:
                print(f"Erro inesperado ao carregar heurística {nome_modulo}: {e}")
    return heuristicas

def gerar_previsao():
    """
    Gera uma previsão de números com base em múltiplas heurísticas
    e um decisor ponderado, utilizando a nova arquitetura modular.
    """
    sorteios_historico = _carregar_sorteios()
    if not sorteios_historico:
        print("Erro: Nenhum sorteio histórico encontrado. Não é possível gerar uma previsão.")
        return

    # 1. Carrega todas as heurísticas e coleta as suas dependências
    heuristicas = carregar_heuristicas()
    todas_dependencias = set()
    for h in heuristicas.values():
        todas_dependencias.update(h["dependencias"])
    
    # 2. Obtém as estatísticas necessárias de forma otimizada
    # Esta é a chamada crucial para o nosso novo módulo 'dados.py'
    estatisticas = obter_estatisticas(todas_dependencias, sorteios_historico)
    # Adiciona dados do último sorteio, necessário para algumas heurísticas
    estatisticas['terminacoes_sorteio_atual'] = {num % 10 for num in sorteios_historico[-1].get('numeros', [])}
    
    print("\n--- Previsões das Heurísticas ---\n")
    detalhes_previsoes = []

    # 3. Executa cada heurística com os dados necessários
    for nome, dados_heuristica in heuristicas.items():
        try:
            funcao = dados_heuristica["funcao"]
            # Todas as heurísticas agora têm a mesma interface: prever(estatisticas, n=5)
            numeros = funcao(estatisticas, n=5)
            print(f"{nome:<35}: {sorted(numeros)}")
            detalhes_previsoes.append({"nome": nome, "numeros": sorted(numeros)})
        except Exception as e:
            print(f"Erro na heurística {nome:<35}: {e}")

    print("\n--- Sugestão Final ---")
    
    # 4. Tenta carregar o decisor
    try:
        if not os.path.exists(PESOS_PATH):
            print(f"Erro: O ficheiro de pesos '{PESOS_PATH}' não foi encontrado. Por favor, treine o decisor primeiro.")
            return

        with open(PESOS_PATH, 'r', encoding='utf-8') as f:
            pesos_json = json.load(f)
            
        caminho_modelo_gb = pesos_json['modelos'].get('gradient_boosting')
        caminho_modelo_rf = pesos_json['modelos'].get('random_forest')
        
        if not caminho_modelo_gb or not caminho_modelo_rf:
            print("Erro: Caminhos dos modelos não encontrados no ficheiro de pesos. A sair.")
            return

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
    except Exception as e:
        print(f"Erro inesperado no decisor: {e}")

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
