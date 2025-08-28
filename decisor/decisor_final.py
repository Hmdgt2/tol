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
        if os.path.exists(self.caminho_pesos):
            with open(self.caminho_pesos, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.pesos = np.array(dados['pesos'])
                self.heuristicas_ordenadas = dados['heuristicas']
                self.modelo_ml.coef_ = np.array([self.pesos])
                # Dummy call to make it "fitted"
                self.modelo_ml.fit([[0] * len(self.heuristicas_ordenadas)], [0])

    def save_pesos(self):
        os.makedirs(os.path.dirname(self.caminho_pesos), exist_ok=True)
        with open(self.caminho_pesos, 'w', encoding='utf-8') as f:
            json.dump({
                'heuristicas': self.heuristicas_ordenadas,
                'pesos': self.pesos.tolist()
            }, f, indent=2, ensure_ascii=False)

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        """
        Treina o modelo de regressão logística com base nas previsões históricas.
        
        :param X_treino: Matriz de features.
        :param y_treino: Vetor de labels.
        :param heuristicas_ordenadas: Lista com os nomes das heurísticas na ordem correta.
        """
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return

        self.modelo_ml.fit(X_treino, y_treino)
        self.pesos = self.modelo_ml.coef_[0]
        self.heuristicas_ordenadas = heuristicas_ordenadas
        self.save_pesos()

    def predict(self, previsoes_detalhes):
        """
        Faz uma previsão usando o modelo treinado.
        
        :param previsoes_detalhes: Lista de dicionários com as previsões das heurísticas.
        :return: Lista de 6 números mais prováveis.
        """
        if not self.pesos or not self.heuristicas_ordenadas:
            print("Modelo não treinado ou pesos não carregados. A usar pesos padrão.")
            # Retorna uma previsão padrão se o modelo não estiver pronto
            return []

        # Mapeia as previsões para a ordem correta
        previsoes_mapeadas = {d['nome']: d['numeros'] for d in previsoes_detalhes}
        
        # Cria a matriz de features para a previsão
        X_novo = []
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_mapeadas.get(nome, []) else 0 for nome in self.heuristicas_ordenadas]
            X_novo.append(feature_vector)
        
        if not X_novo:
            return []

        # Faz a previsão e obtém as probabilidades
        probabilidades = self.modelo_ml.predict_proba(X_novo)[:, 1]

        # Combina números e probabilidades e ordena por probabilidade
        numeros_com_prob = sorted(zip(range(1, 50), probabilidades), key=lambda x: x[1], reverse=True)
        
        # Seleciona os 6 números mais prováveis
        previsao_final = [num for num, prob in numeros_com_prob[:6]]
        
        return previsao_final
