import os
import sys
import importlib
from collections import defaultdict, Counter
from itertools import combinations
import json
import inspect
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
import joblib

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios
from decisor.decisor_final import HeuristicDecisor

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')

# Caminho para o ficheiro JSON de pesos (agora conterá metadados e os caminhos para os modelos)
PESOS_JSON_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')
# Caminho para o ficheiro Joblib que armazenará o modelo Gradient Boosting
MODELO_GB_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_gradient_boosting.joblib')
# Caminho para o ficheiro Joblib que armazenará o modelo Random Forest
MODELO_RF_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_random_forest.joblib')
# Caminho para o ficheiro de pesos das heurísticas
PESOS_HEURISTICAS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_heuristicas.json')


def carregar_heuristicas():
    """
    Carrega dinamicamente todas as heurísticas do diretório 'heuristicas'.
    """
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

def treinar_decisor():
    """
    Treina os modelos decisores usando dados históricos.
    """
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    print("Simulando previsões de heurísticas para dados históricos...")
    
    previsoes_por_sorteio = defaultdict(dict)
    
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        
        estatisticas = get_all_stats(historico_parcial)
        estatisticas['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(historico_parcial, num_sorteios=100)

        for nome, funcao in heuristicas:
            try:
                parametros = inspect.signature(funcao).parameters
                
                if 'sorteios_historico' in parametros:
                    resultado = funcao(estatisticas, historico_parcial, n=5)
                else:
                    resultado = funcao(estatisticas, n=5)
                
                previsoes_por_sorteio[i][nome] = resultado.get("numeros", [])
            except Exception as e:
                print(f"Erro inesperado na heurística {nome}: {e}")
                previsoes_por_sorteio[i][nome] = []

    print("Pré-cálculo concluído. A criar os dados de treino para os modelos de ML...")
    
    X_treino = []
    y_treino = []
    heuristicas_ordenadas = [nome for nome, _ in heuristicas]

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

    # Adicione estas linhas para verificar a criação dos ficheiros
    print("\n--- Verificação de Ficheiros ---")
    if os.path.exists(MODELO_GB_PATH):
        print(f"✅ Ficheiro de modelo Gradient Boosting encontrado em: {MODELO_GB_PATH}")
    else:
        print(f"❌ Erro: Ficheiro de modelo Gradient Boosting não encontrado em: {MODELO_GB_PATH}")
    
    if os.path.exists(MODELO_RF_PATH):
        print(f"✅ Ficheiro de modelo Random Forest encontrado em: {MODELO_RF_PATH}")
    else:
        print(f"❌ Erro: Ficheiro de modelo Random Forest não encontrado em: {MODELO_RF_PATH}")
        
    if os.path.exists(PESOS_JSON_PATH):
        print(f"✅ Ficheiro de pesos JSON encontrado em: {PESOS_JSON_PATH}")
    else:
        print(f"❌ Erro: Ficheiro de pesos JSON não encontrado em: {PESOS_JSON_PATH}")
    print("--- Fim da Verificação ---")


    if os.path.exists(PESOS_HEURISTICAS_PATH):
        os.remove(PESOS_HEURISTICAS_PATH)
        print("Ficheiro de pesos das heurísticas reiniciado.")

if __name__ == '__main__':
    treinar_decisor()
