# decisor/decisor_final.py
import json
import os
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import joblib

class HeuristicDecisor:
    def __init__(self, caminho_pesos='decisor/pesos_atuais.joblib'):
        self.caminho_pesos = caminho_pesos
        # Altere o modelo para GradientBoostingClassifier
        self.modelo_ml = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
        self.heuristicas_ordenadas = []

    def load_pesos(self):
        """
        Carrega o modelo treinado e as heurísticas ordenadas do ficheiro.
        """
        if os.path.exists(self.caminho_pesos):
            try:
                # Carregar o modelo completo usando joblib
                self.modelo_ml = joblib.load(self.caminho_pesos)
                # Carregar as heurísticas ordenadas de um ficheiro de texto ou JSON
                # Para simplificar, vamos assumir que elas estão no mesmo diretório
                heuristicas_path = os.path.join(os.path.dirname(self.caminho_pesos), "heuristicas.json")
                if os.path.exists(heuristicas_path):
                    with open(heuristicas_path, 'r', encoding='utf-8') as f:
                        self.heuristicas_ordenadas = json.load(f)
                else:
                    self.heuristicas_ordenadas = []
                return True
            except Exception as e:
                print(f"Aviso: Erro ao carregar o modelo do ficheiro: {e}. O modelo será treinado do zero se necessário.")
                return False
        else:
            print("Aviso: Ficheiro de pesos não encontrado. O modelo será treinado do zero se necessário.")
            return False

    def save_pesos(self):
        """Guarda o modelo treinado e as heurísticas ordenadas no ficheiro."""
        os.makedirs(os.path.dirname(self.caminho_pesos), exist_ok=True)
        # Guardar o modelo completo usando joblib
        joblib.dump(self.modelo_ml, self.caminho_pesos)
        # Guardar as heurísticas ordenadas para serem carregadas com o modelo
        heuristicas_path = os.path.join(os.path.dirname(self.caminho_pesos), "heuristicas.json")
        with open(heuristicas_path, 'w', encoding='utf-8') as f:
            json.dump(self.heuristicas_ordenadas, f, indent=2, ensure_ascii=False)
        
        print("Modelo e heurísticas guardados com sucesso.")

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        """Treina o modelo de ML com dados históricos e guarda o modelo."""
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return

        print("A treinar o modelo de Gradient Boosting...")
        self.modelo_ml.fit(X_treino, y_treino)
        self.heuristicas_ordenadas = heuristicas_ordenadas
        self.save_pesos()
        print("Treino concluído. Modelo guardado em:", self.caminho_pesos)

    def predict(self, previsoes_detalhes):
        """
        Gera a previsão final combinando as previsões das heurísticas.
        Carrega o modelo se ainda não tiver sido carregado.
        """
        # Tentar carregar o modelo, se ainda não estiver na memória
        if not hasattr(self.modelo_ml, 'n_estimators') or not self.heuristicas_ordenadas:
            if not self.load_pesos():
                print("Modelo não treinado ou carregado. Não é possível gerar uma previsão.")
                return []
        
        previsoes_mapeadas = {d['nome']: d['numeros'] for d in previsoes_detalhes}
        
        X_novo = []
        for num in range(1, 50):
            # Assegura que todas as heurísticas são incluídas na mesma ordem
            feature_vector = [1 if num in previsoes_mapeadas.get(nome, []) else 0 for nome in self.heuristicas_ordenadas]
            X_novo.append(feature_vector)
        
        if not X_novo:
            return []

        probabilidades = self.modelo_ml.predict_proba(X_novo)[:, 1]

        numeros_com_prob = sorted(zip(range(1, 50), probabilidades), key=lambda x: x[1], reverse=True)
        
        previsao_final = [num for num, prob in numeros_com_prob[:6]]
        
        return previsao_final
