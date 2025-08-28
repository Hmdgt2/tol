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
        # Não carregar os pesos na inicialização, pois o script de previsão
        # fará isso antes de chamar o 'predict'.

    def load_pesos(self):
        """
        Carrega os pesos e as heurísticas ordenadas do ficheiro.
        Retorna True se o carregamento for bem-sucedido, False caso contrário.
        """
        if os.path.exists(self.caminho_pesos) and os.path.getsize(self.caminho_pesos) > 0:
            try:
                with open(self.caminho_pesos, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.pesos = np.array(dados['pesos'])
                    self.heuristicas_ordenadas = dados['heuristicas']
                    
                    # Atribuir os pesos ao modelo de ML
                    self.modelo_ml.coef_ = np.array([self.pesos])
                    # É boa prática também inicializar o intercept, que é o viés do modelo
                    # O valor aqui não é crítico, desde que o modelo seja treinado depois.
                    self.modelo_ml.intercept_ = np.array([0.0])
                    
                    return True
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Aviso: Erro ao carregar o ficheiro de pesos: {e}. O modelo será treinado do zero se necessário.")
                self.pesos = None
                self.heuristicas_ordenadas = []
                return False
        else:
            print("Aviso: Ficheiro de pesos não encontrado. O modelo será treinado do zero se necessário.")
            self.pesos = None
            self.heuristicas_ordenadas = []
            return False

    def save_pesos(self):
        """Guarda os pesos do modelo no ficheiro."""
        if self.pesos is not None and len(self.heuristicas_ordenadas) > 0:
            os.makedirs(os.path.dirname(self.caminho_pesos), exist_ok=True)
            with open(self.caminho_pesos, 'w', encoding='utf-8') as f:
                json.dump({
                    'heuristicas': self.heuristicas_ordenadas,
                    'pesos': self.pesos.tolist()
                }, f, indent=2, ensure_ascii=False)
        else:
            print("Aviso: Não há pesos para guardar.")

    def fit(self, X_treino, y_treino, heuristicas_ordenadas):
        """Treina o modelo de ML com dados históricos e guarda os pesos."""
        if not X_treino or not y_treino:
            print("Nenhum dado de treino fornecido.")
            return

        print("A treinar o modelo de Regressão Logística...")
        self.modelo_ml.fit(X_treino, y_treino)
        self.pesos = self.modelo_ml.coef_[0]
        self.heuristicas_ordenadas = heuristicas_ordenadas
        self.save_pesos()
        print("Treino concluído. Pesos guardados em:", self.caminho_pesos)

    def predict(self, previsoes_detalhes):
        """
        Gera a previsão final combinando as previsões das heurísticas.
        Carrega os pesos se ainda não tiverem sido carregados.
        """
        # Tentar carregar os pesos, se ainda não estiverem na memória
        if self.pesos is None:
            if not self.load_pesos():
                print("Modelo não treinado ou pesos não carregados. Não é possível gerar uma previsão.")
                return []
        
        previsoes_mapeadas = {d['nome']: d['numeros'] for d in previsoes_detalhes}
        
        X_novo = []
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_mapeadas.get(nome, []) else 0 for nome in self.heuristicas_ordenadas]
            X_novo.append(feature_vector)
        
        if not X_novo:
            return []

        # Certificar que o modelo foi treinado ou carregado corretamente
        if not hasattr(self.modelo_ml, 'coef_'):
            print("O modelo de ML não foi treinado ou inicializado corretamente. Não é possível prever.")
            return []
            
        probabilidades = self.modelo_ml.predict_proba(X_novo)[:, 1]

        numeros_com_prob = sorted(zip(range(1, 50), probabilidades), key=lambda x: x[1], reverse=True)
        
        previsao_final = [num for num, prob in numeros_com_prob[:6]]
        
        return previsao_final
