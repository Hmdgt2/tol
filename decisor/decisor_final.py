# decisor/decisor_final.py
import json
import os
import numpy as np
from sklearn.linear_model import LogisticRegression

class HeuristicDecisor:
    def __init__(self, caminho_pesos='decisor/pesos_atuais.json'):
        self.caminho_pesos = caminho_pesos
        self.modelo_ml = LogisticRegression(solver='liblinear')
        self.pesos = None
        self.heuristicas_ordenadas = []
        self.load_pesos()

    def load_pesos(self):
        # A linha "if" deve ter 4 espaços de indentação para estar dentro da função.
        if os.path.exists(self.caminho_pesos) and os.path.getsize(self.caminho_pesos) > 0:
            try:
                with open(self.caminho_pesos, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.pesos = np.array(dados['pesos'])
                    self.heuristicas_ordenadas = dados['heuristicas']
                    self.modelo_ml.coef_ = np.array([self.pesos])
                    
                    if len(self.heuristicas_ordenadas) > 0:
                        X_dummy = np.array([[0] * len(self.heuristicas_ordenadas), [1] * len(self.heuristicas_ordenadas)])
                        y_dummy = np.array([0, 1])
                        self.modelo_ml.fit(X_dummy, y_dummy)

            except (KeyError, json.JSONDecodeError) as e:
                print(f"Aviso: Erro ao carregar o ficheiro de pesos: {e}. O modelo será treinado do zero.")
                self.pesos = None
                self.heuristicas_ordenadas = []
        else:
            print("Aviso: Ficheiro de pesos não encontrado. O modelo será treinado do zero.")
            self.pesos = None
            self.heuristicas_ordenadas = []

    def save_pesos(self):
        os.makedirs(os.path.dirname(self.caminho_pesos), exist_ok=True)
        with open(self.caminho_pesos, 'w', encoding='utf-8') as f:
            json.dump({
                'heuristicas': self.heuristicas_ordenadas,
                'pesos': self.pesos.tolist()
            }, f, indent=2, ensure_ascii=False)

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return

        self.modelo_ml.fit(X_treino, y_treino)
        self.pesos = self.modelo_ml.coef_[0]
        self.heuristicas_ordenadas = heuristicas_ordenadas
        self.save_pesos()

    def predict(self, previsoes_detalhes):
        if not self.pesos or not self.heuristicas_ordenadas:
            print("Modelo não treinado ou pesos não carregados. A usar pesos padrão.")
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
