# treinar_decisor.py
import os
import sys
import importlib
from collections import defaultdict, Counter
import json
import inspect
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import joblib

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa a biblioteca de tipagem para resolver o erro
from typing import Dict, Any, List

from lib.dados import obter_estatisticas, _carregar_sorteios
# Vamos usar o mapeamento de estatísticas diretamente para o treino incremental
from lib.dados import MAP_ESTATISTICAS

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')

# Caminhos para os ficheiros
PESOS_JSON_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')
MODELO_GB_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_gradient_boosting.joblib')
MODELO_RF_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_random_forest.joblib')

def carregar_heuristicas_com_dependencias():
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

def treinar_decisor():
    """
    Treina os modelos decisores usando dados históricos de forma otimizada.
    """
    sorteios_historico = _carregar_sorteios()
    heuristicas = carregar_heuristicas_com_dependencias()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    print("Coletando dependências das heurísticas...")
    todas_dependencias = set()
    for h in heuristicas.values():
        todas_dependencias.update(h["dependencias"])

    print("Simulando previsões de heurísticas para dados históricos...")
    
    previsoes_por_sorteio = defaultdict(dict)
    
    # 1. Pré-calcula as estatísticas de forma incremental para cada sorteio
    estatisticas_incrementais = defaultdict(dict)
    
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        
        # Calcula apenas as estatísticas necessárias para este passo
        for dep in todas_dependencias:
            if dep in MAP_ESTATISTICAS:
                try:
                    # Chame a função de cálculo correspondente
                    estatisticas_incrementais[i][dep] = MAP_ESTATISTICAS[dep](historico_parcial)
                except Exception as e:
                    print(f"Erro ao calcular a estatística '{dep}' no passo {i}: {e}")
                    estatisticas_incrementais[i][dep] = {}

        # 2. Executa as heurísticas com as estatísticas do momento
        for nome, dados_heuristica in heuristicas.items():
            try:
                funcao = dados_heuristica["funcao"]
                # Passa apenas as estatísticas necessárias para a heurística
                numeros = funcao(estatisticas_incrementais[i], n=5)
                previsoes_por_sorteio[i][nome] = numeros
            except Exception as e:
                print(f"Erro inesperado na heurística {nome} no passo {i}: {e}")
                previsoes_por_sorteio[i][nome] = []
    
    print("Pré-cálculo concluído. A criar os dados de treino para os modelos de ML...")
    
    X_treino = []
    y_treino = []
    heuristicas_ordenadas = sorted(list(heuristicas.keys()))

    for i in range(len(sorteios_historico) - 1):
        sorteio_alvo = sorteios_historico[i+1]
        previsoes_sorteio_atual = previsoes_por_sorteio[i]
        
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_sorteio_atual.get(nome, []) else 0 for nome in heuristicas_ordenadas]
            X_treino.append(feature_vector)
            
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    if not X_treino:
        print("Nenhum dado de treino gerado.")
        return

    # --- NOVO: TREINA E SALVA OS DOIS MODELOS ---
    os.makedirs(os.path.dirname(MODELO_GB_PATH), exist_ok=True)
    
    print("A treinar o modelo de Gradient Boosting...")
    modelo_gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
    modelo_gb.fit(X_treino, y_treino)
    joblib.dump(modelo_gb, MODELO_GB_PATH)

    print("A treinar o modelo de Random Forest...")
    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_treino, y_treino)
    joblib.dump(modelo_rf, MODELO_RF_PATH)
    
    # --- SALVA OS METADADOS DOS DOIS MODELOS ---
    os.makedirs(os.path.dirname(PESOS_JSON_PATH), exist_ok=True)

    json_data = {
        'modelos': {
            'gradient_boosting': os.path.relpath(MODELO_GB_PATH, PROJECT_ROOT),
            'random_forest': os.path.relpath(MODELO_RF_PATH, PROJECT_ROOT)
        },
        'heuristicas_ordenadas': heuristicas_ordenadas
    }
    
    with open(PESOS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print("Treino concluído. Modelos Joblib guardados.")
    print("Metadados JSON atualizados em:", PESOS_JSON_PATH)

if __name__ == '__main__':
    treinar_decisor()
