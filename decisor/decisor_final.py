# decisor/decisor_final.py
import json
import os
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import joblib

class HeuristicDecisor:
    def __init__(self, caminho_pesos_json, caminho_modelo_joblib):
        self.caminho_pesos_json = caminho_pesos_json
        self.caminho_modelo_joblib = caminho_modelo_joblib
        self.modelo_ml = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
        self.heuristicas_ordenadas = []

    def load_model(self):
        """
        Carrega o modelo treinado e as heurísticas dos ficheiros.
        """
        try:
            # 1. Carregar os metadados do JSON
            with open(self.caminho_pesos_json, 'r', encoding='utf-8') as f:
                dados_metadados = json.load(f)
            
            self.heuristicas_ordenadas = dados_metadados.get('heuristicas_ordenadas', [])

            # 2. Carregar o modelo do ficheiro .joblib
            self.modelo_ml = joblib.load(self.caminho_modelo_joblib)
            
            return True

        except (json.JSONDecodeError, FileNotFoundError, joblib.externals.loky.backend.exceptions.PicklingError) as e:
            print(f"Aviso: Erro ao carregar os ficheiros do modelo: {e}. O modelo será treinado do zero se necessário.")
            return False

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        """Treina o modelo e guarda os dois ficheiros."""
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return
        
        print("A treinar o modelo de Gradient Boosting...")
        self.modelo_ml.fit(X_treino, y_treino)
        self.heuristicas_ordenadas = heuristicas_ordenadas

        # Garante que os diretórios existem
        os.makedirs(os.path.dirname(self.caminho_pesos_json), exist_ok=True)
        os.makedirs(os.path.dirname(self.caminho_modelo_joblib), exist_ok=True)

        # 1. Salva o modelo de ML como um ficheiro .joblib
        joblib.dump(self.modelo_ml, self.caminho_modelo_joblib)

        # 2. Salva os metadados no JSON
        json_data = {
            'caminho_modelo_joblib': os.path.relpath(self.caminho_modelo_joblib, os.path.dirname(self.caminho_pesos_json)),
            'heuristicas_ordenadas': self.heuristicas_ordenadas
        }
        
        with open(self.caminho_pesos_json, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print("Treino concluído. Modelo Joblib guardado em:", self.caminho_modelo_joblib)
        print("Metadados JSON guardados em:", self.caminho_pesos_json)

    def predict(self, previsoes_detalhes):
        """
        Gera a previsão final combinando as previsões das heurísticas.
        """
        if not self.heuristicas_ordenadas or not hasattr(self.modelo_ml, 'n_estimators'):
            if not self.load_model():
                print("Modelo não treinado ou carregado. Não é possível gerar uma previsão.")
                return []
        
        previsoes_mapeadas = {d['nome']: d['numeros'] for d in previsoes_detalhes}
        
        X_novo = []
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_mapeadas.get(nome, []) else 0 for nome in self.heuristicas_ordenadas]
            X_novo.append(feature_vector)
        
        if not X_novo:
            return []

        probabilidades = self.modelo_ml.predict_proba(X_novo)[:, 1]

        numeros_com_prob = sorted(zip(range(1, 50), probabilidades), key=lambda x: x[1], reverse=True)
        
        previsao_final = [num for num, prob in numeros_com_prob[:6]]
        
        return previsao_final
