import os
import sys
import json
import numpy as np
import joblib
from collections import defaultdict
from typing import Dict, Any, List
import importlib

# Adiciona o diretório raiz para resolver importações
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# IMPORTANTE: Agora importamos a classe 'Dados' em vez das funções
from lib.dados import Dados 
from lib.despachante import Despachante

# Adicionamos os imports para os modelos e o scaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Novos caminhos para os ficheiros
MODELOS_DIR = os.path.join(PROJECT_ROOT, 'decisor', 'modelos_salvos')
PERFORMANCE_PATH = os.path.join(MODELOS_DIR, 'performance_modelos.json')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
MODELOS_ML_DIR = os.path.join(PROJECT_ROOT, 'modelos_ml')

if not os.path.exists(MODELOS_DIR):
    os.makedirs(MODELOS_DIR)

def carregar_modelos_ml():
    """
    Carrega dinamicamente os modelos de machine learning da pasta 'modelos_ml'.
    """
    modelos_disponiveis = {}
    sys.path.insert(0, MODELOS_ML_DIR)
    for filename in os.listdir(MODELOS_ML_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'get_model'):
                    modelos_disponiveis[module_name] = module.get_model()
            except ImportError as e:
                print(f"Aviso: Não foi possível importar o modelo '{module_name}'. Erro: {e}")
    sys.path.pop(0)
    return modelos_disponiveis

def treinar_decisor():
    """
    Treina múltiplos modelos e salva o melhor.
    """
    try:
        # 1. Carrega o despachante e dados
        print("Iniciando o treino. Carregando heurísticas e dados...")
        despachante = Despachante()
        todas_dependencias = despachante.obter_todas_dependencias()
        
        # IMPORTANTE: Instancia a classe Dados para carregar os sorteios
        dados_manager = Dados()
        sorteios_historico = dados_manager.sorteios

        if not todas_dependencias or not sorteios_historico or len(sorteios_historico) < 2:
            print("Dados insuficientes para treino. O processo será encerrado.")
            return

        print("Simulando previsões de heurísticas para dados históricos...")
        X_treino = []
        y_treino = []
        metadados_heuristicas = despachante.get_metadados()
        heuristicas_ordenadas = sorted(list(metadados_heuristicas.keys()))

        for i in range(len(sorteios_historico) - 1):
            # IMPORTANTE: Cria uma nova instância de Dados com um subconjunto do histórico
            # Isso simula o conhecimento do sistema em cada ponto do tempo.
            historico_parcial = sorteios_historico[:i+1]
            dados_parciais = Dados()
            dados_parciais.sorteios = historico_parcial
            
            sorteio_alvo = sorteios_historico[i+1]
            
            # Chama o método da instância para obter as estatísticas
            estatisticas_parciais, _ = dados_parciais.obter_estatisticas(todas_dependencias)
            
            previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)
            
            for num in range(1, 50):
                feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
                X_treino.append(feature_vector)
                y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

        X_treino_np = np.array(X_treino)
        y_treino_np = np.array(y_treino)

        # 2. Carrega os modelos dinamicamente
        modelos_disponiveis = carregar_modelos_ml()
        if not modelos_disponiveis:
            print("Nenhum modelo de ML encontrado na pasta 'modelos_ml'. O treino será encerrado.")
            return
            
        resultados_treino = {}

        # 3. Treina e salva cada modelo
        print("\nConjunto de treino criado. Iniciando o treino dos modelos de ML...")
        for nome_modelo, modelo in modelos_disponiveis.items():
            print(f"Treinando o modelo: {nome_modelo}...")
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('model', modelo)
            ])
            pipeline.fit(X_treino_np, y_treino_np)
            
            # Avalia o modelo
            score_treino = pipeline.score(X_treino_np, y_treino_np)
            
            # Salva o pipeline
            modelo_path = os.path.join(MODELOS_DIR, f"{nome_modelo}_pipeline.joblib")
            joblib.dump(pipeline, modelo_path)
            
            resultados_treino[nome_modelo] = {
                'caminho': modelo_path,
                'score_treino': score_treino,
                'ultima_atualizacao': "AGORA"
            }
            print(f"✅ Modelo {nome_modelo} salvo com score: {score_treino:.4f}")

        # 4. Salva o ficheiro de performance
        with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
            json.dump(resultados_treino, f, indent=2, ensure_ascii=False)
            
        # 5. Salva os metadados das heurísticas
        json_data_metadados = {'heuristicas_ordenadas': heuristicas_ordenadas}
        with open(METADADOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_data_metadados, f, indent=2, ensure_ascii=False)
            
        print("\n✅ Treino de todos os modelos concluído com sucesso.")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: Ocorreu um erro durante o treino do modelo.")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Detalhes: {e}")
        sys.exit(1)

if __name__ == '__main__':
    treinar_decisor()
