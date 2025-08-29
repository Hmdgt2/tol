import joblib
import json
import os
import sys
from collections import defaultdict, Counter

# Adiciona o diretório raiz ao caminho do sistema para resolver caminhos relativos
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class HeuristicDecisor:
    def __init__(self, caminho_pesos_json, caminho_modelo_joblib_gb, caminho_modelo_joblib_rf):
        """
        Inicializa o decisor carregando o ficheiro de metadados e os modelos de ML.
        
        Args:
            caminho_pesos_json (str): O caminho para o ficheiro JSON com a ordem das heurísticas.
            caminho_modelo_joblib_gb (str): O caminho para o modelo Gradient Boosting.
            caminho_modelo_joblib_rf (str): O caminho para o modelo Random Forest.
        """
        self.caminho_pesos_json = caminho_pesos_json
        
        try:
            with open(caminho_pesos_json, 'r', encoding='utf-8') as f:
                self.metadados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Ficheiro de pesos não encontrado em: {caminho_pesos_json}. Por favor, treine o modelo primeiro.")

        self.heuristicas_ordenadas = self.metadados.get('heuristicas_ordenadas', [])
        
        try:
            self.modelo_gb = joblib.load(caminho_modelo_joblib_gb)
            self.modelo_rf = joblib.load(caminho_modelo_joblib_rf)
        except FileNotFoundError:
            raise FileNotFoundError("Um dos modelos Joblib não foi encontrado. Por favor, treine o modelo novamente.")
        
        self.pesos_manuais = self.metadados.get('pesos_manuais', {})

    def _get_feature_vector(self, previsoes_atuais):
        """
        Cria um vetor de características (features) para um único sorteio.
        """
        previsoes_dict = {p['nome']: set(p['numeros']) for p in previsoes_atuais}
        
        feature_vectors = []
        for num in range(1, 50):
            vector = [1 if num in previsoes_dict.get(nome, set()) else 0 for nome in self.heuristicas_ordenadas]
            feature_vectors.append(vector)
            
        return feature_vectors

    def predict(self, detalhes_previsoes):
        """
        Combina as previsões das heurísticas usando os modelos de ML.
        
        Args:
            detalhes_previsoes (list): Lista de dicionários com as previsões de cada heurística.
            
        Returns:
            list: Uma lista de 5 números previstos.
        """
        feature_vectors = self._get_feature_vector(detalhes_previsoes)
        
        # Obter as probabilidades de acerto de cada modelo
        probabilidades_gb = self.modelo_gb.predict_proba(feature_vectors)[:, 1]
        probabilidades_rf = self.modelo_rf.predict_proba(feature_vectors)[:, 1]
        
        # Combinar as probabilidades (neste caso, uma simples média)
        probabilidades_combinadas = (probabilidades_gb + probabilidades_rf) / 2
        
        # Criar uma lista de tuplas (probabilidade, numero)
        probabilidades_por_numero = []
        for i, prob in enumerate(probabilidades_combinadas):
            probabilidades_por_numero.append((prob, i + 1))
            
        # Ordenar e selecionar os 5 números com maior probabilidade
        probabilidades_por_numero.sort(key=lambda x: x[0], reverse=True)
        
        previsao_final = [numero for prob, numero in probabilidades_por_numero[:5]]
        
        return previsao_final
