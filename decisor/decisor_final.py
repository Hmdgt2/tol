# decisor/decisor_final.py
import json
import os
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import joblib

class HeuristicDecisor:
    def __init__(self, caminho_pesos='decisor/pesos_atuais.joblib'):
        self.caminho_pesos = caminho_pesos
        self.modelo_ml = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
        self.heuristicas_ordenadas = []

    def load_pesos(self):
        """
        Carrega o modelo e as heurísticas do ficheiro .joblib.
        """
        if os.path.exists(self.caminho_pesos):
            try:
                # Carrega o dicionário que contém o modelo e a lista de heurísticas
                dados_carregados = joblib.load(self.caminho_pesos)
                self.modelo_ml = dados_carregados['modelo']
                self.heuristicas_ordenadas = dados_carregados['heuristica_nomes']
                return True
            except Exception as e:
                print(f"Aviso: Erro ao carregar o modelo do ficheiro: {e}.")
                return False
        else:
            print("Aviso: Ficheiro de pesos não encontrado. O modelo será treinado do zero se necessário.")
            return False

    def save_pesos(self, heuristicas_ordenadas):
        """Guarda o modelo e as heurísticas ordenadas no ficheiro .joblib."""
        os.makedirs(os.path.dirname(self.caminho_pesos), exist_ok=True)
        
        # Cria um dicionário para guardar tudo
        dados_a_guardar = {
            'modelo': self.modelo_ml,
            'heuristica_nomes': heuristicas_ordenadas
        }
        
        # Guarda o dicionário no ficheiro .joblib
        joblib.dump(dados_a_guardar, self.caminho_pesos)
        print("Modelo e heurísticas guardados com sucesso.")

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        """Treina o modelo de ML com dados históricos e guarda o modelo."""
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return

        print("A treinar o modelo de Gradient Boosting...")
        self.modelo_ml.fit(X_treino, y_treino)
        self.heuristicas_ordenadas = heuristicas_ordenadas
        self.save_pesos(heuristicas_ordenadas) # Passa a lista de heurísticas para o método de salvamento
        print("Treino concluído. Modelo guardado em:", self.caminho_pesos)

    def predict(self, previsoes_detalhes):
        """
        Gera a previsão final combinando as previsões das heurísticas.
        Carrega o modelo se ainda não tiver sido carregado.
        """
        if not self.heuristicas_ordenadas or not hasattr(self.modelo_ml, 'n_estimators'):
            if not self.load_pesos():
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
