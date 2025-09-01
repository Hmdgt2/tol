import os
import sys
import json
import numpy as np
import joblib
from collections import defaultdict
from typing import Dict, Any, List

# Adicionamos os imports para a nova arquitetura
from lib.dados import _carregar_sorteios, obter_estatisticas
from lib.despachante import Despachante

# Adicionamos os imports para os modelos e o scaler
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Caminhos para os ficheiros
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_previsor.joblib')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
DECISOR_DIR = os.path.join(PROJECT_ROOT, 'decisor')
if not os.path.exists(DECISOR_DIR):
    os.makedirs(DECISOR_DIR)

def treinar_decisor(modelo_ml):
    """
    Treina o modelo decisor usando dados históricos.
    Args:
        modelo_ml: O modelo de Machine Learning a ser treinado (ex: LogisticRegression()).
    """
    # 1. Carrega o despachante para gerir as heurísticas
    print("Iniciando o treino. Carregando heurísticas...")
    despachante = Despachante()
    
    # 2. Obtém todas as dependências necessárias
    todas_dependencias = despachante.get_todas_dependencias()
    if not todas_dependencias:
        print("Nenhuma dependência encontrada nas heurísticas. O treino não pode continuar.")
        return
    
    # 3. Carrega o histórico de sorteios
    sorteios_historico = _carregar_sorteios()
    if not sorteios_historico or len(sorteios_historico) < 2:
        print("Histórico de sorteios insuficiente para treino.")
        return
    
    print("Simulando previsões de heurísticas para dados históricos...")
    
    X_treino = []
    y_treino = []
    
    # Usamos o despachante para obter os metadados e garantir a ordem
    metadados_heuristicas = despachante.get_metadados()
    heuristicas_ordenadas = sorted(list(metadados_heuristicas.keys()))

    # 4. Loop de simulação para construir o conjunto de treino
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        sorteio_alvo = sorteios_historico[i+1]
        
        # Obtém as estatísticas para o histórico parcial
        estatisticas_parciais = obter_estatisticas(todas_dependencias, historico_parcial)
        
        # Obtém as previsões das heurísticas para este ponto no tempo
        previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)
        
        # Cria o vetor de features (X) para cada número
        for num in range(1, 50):
            # A feature é 1 se a heurística sugeriu o número, 0 caso contrário
            feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
            X_treino.append(feature_vector)
            
            # A label é 1 se o número saiu no sorteio real, 0 caso contrário
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    # 5. Treina o modelo usando um pipeline para normalizar os dados
    print("\nConjunto de treino criado. Iniciando o treino do modelo de ML...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', modelo_ml)
    ])
    
    X_treino_np = np.array(X_treino)
    y_treino_np = np.array(y_treino)
    
    pipeline.fit(X_treino_np, y_treino_np)
    
    # 6. Salva o pipeline completo (incluindo o scaler) e os metadados
    joblib.dump(pipeline, MODELO_PATH)
    
    json_data = {
        'modelo_usado': str(modelo_ml),
        'heuristicas_ordenadas': heuristicas_ordenadas
    }
    with open(METADADOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Treino concluído. Pipeline salvo em '{MODELO_PATH}'.")
    print(f"✅ Metadados salvos em '{METADADOS_PATH}'.")

if __name__ == '__main__':
    # Exemplo de como usar com LogisticRegression
    modelo_a_treinar = LogisticRegression(solver='liblinear')
    treinar_decisor(modelo_a_treinar)

    # Pode testar outros modelos, como:
    # modelo_a_treinar = RandomForestClassifier(n_estimators=100, random_state=42)
    # treinar_decisor(modelo_a_treinar)
