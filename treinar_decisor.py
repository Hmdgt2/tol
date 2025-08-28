import os
import sys
import importlib
from collections import defaultdict, Counter
from itertools import combinations
import json
import inspect
from sklearn.ensemble import GradientBoostingClassifier
import joblib

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa as funções de dados
from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios
# A classe HeuristicDecisor será ajustada para carregar este novo formato posteriormente
from decisor.decisor_final import HeuristicDecisor 

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')

# Caminho para o ficheiro JSON de pesos (agora conterá metadados e o caminho para o modelo .joblib)
PESOS_JSON_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')
# Caminho para o ficheiro Joblib que armazenará o modelo de ML real
MODELO_JOBLIB_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_ml.joblib')


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
    Treina o modelo decisor usando dados históricos.
    Otimizado para evitar recálculos excessivos.
    """
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    # --- ETAPA 1: PRÉ-CÁLCULO DAS PREVISÕES ---
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

    print("Pré-cálculo concluído. A criar os dados de treino para o modelo de ML...")
    
    # --- ETAPA 2: CRIAÇÃO DOS DADOS DE TREINO E TREINO DO MODELO ---
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

    print("A treinar o modelo de Gradient Boosting...")
    modelo_ml = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
    modelo_ml.fit(X_treino, y_treino)

    # --- NOVO: SALVA O MODELO EM .JOBLIB E METADADOS EM .JSON ---
    # Garante que os diretórios existem
    os.makedirs(os.path.dirname(MODELO_JOBLIB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(PESOS_JSON_PATH), exist_ok=True)

    # 1. Salva o modelo de ML como um ficheiro .joblib
    joblib.dump(modelo_ml, MODELO_JOBLIB_PATH)

    # 2. Salva os metadados (como a lista de heurísticas e o caminho para o modelo .joblib) no JSON
    json_data = {
        # Usamos o caminho relativo para melhor portabilidade entre ambientes
        'caminho_modelo_joblib': os.path.relpath(MODELO_JOBLIB_PATH, PROJECT_ROOT), 
        'heuristicas_ordenadas': heuristicas_ordenadas
    }
    
    with open(PESOS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print("Treino concluído. Modelo Joblib guardado em:", MODELO_JOBLIB_PATH)
    print("Metadados JSON guardados em:", PESOS_JSON_PATH)

if __name__ == '__main__':
    treinar_decisor()
