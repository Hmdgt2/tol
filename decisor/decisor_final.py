# decisor_final.py

import joblib
import json
import os
import sys
import numpy as np
from typing import Dict, Any, List

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class HeuristicDecisor:
    def __init__(self, caminho_pipeline: str, caminho_metadados: str):
        """
        Inicializa o decisor carregando o pipeline de ML e os metadados.
        
        Args:
            caminho_pipeline (str): O caminho para o ficheiro Joblib do pipeline completo.
            caminho_metadados (str): O caminho para o ficheiro JSON com metadados do modelo.
        """
        try:
            # Carregamos o pipeline completo, que inclui o scaler e o modelo
            self.pipeline = joblib.load(caminho_pipeline)
        except FileNotFoundError:
            raise FileNotFoundError(f"Pipeline de ML não encontrado em: {caminho_pipeline}. Por favor, treine o modelo primeiro.")
        
        try:
            with open(caminho_metadados, 'r', encoding='utf-8') as f:
                self.metadados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Ficheiro de metadados não encontrado em: {caminho_metadados}.")

        self.heuristicas_ordenadas = self.metadados.get('heuristicas_ordenadas', [])
        
    def _get_feature_vector(self, previsoes_atuais: List[Dict[str, Any]]) -> np.ndarray:
        """
        Cria um array NumPy de características (features) para um único sorteio.
        """
        previsoes_dict = {p.get('nome'): set(p.get('numeros', [])) for p in previsoes_atuais}
        
        feature_vectors = []
        for num in range(1, 50):
            # Vetor binário que indica se cada heurística sugeriu o número
            vector = [1 if num in previsoes_dict.get(nome, set()) else 0 for nome in self.heuristicas_ordenadas]
            feature_vectors.append(vector)
            
        return np.array(feature_vectors)

    def predict(self, detalhes_previsoes: List[Dict[str, Any]], n_resultados: int = 5) -> List[int]:
        """
        Faz a previsão usando o pipeline de ML e retorna os 5 números mais prováveis.
        
        Args:
            detalhes_previsoes (list): Lista de dicionários com as previsões de cada heurística.
            n_resultados (int): O número de resultados a retornar.
            
        Returns:
            list: Uma lista dos números previstos.
        """
        feature_vectors = self._get_feature_vector(detalhes_previsoes)
        
        if feature_vectors.size == 0:
            return []
            
        # O pipeline irá automaticamente normalizar os dados e fazer a previsão
        probabilidades = self.pipeline.predict_proba(feature_vectors)[:, 1]
        
        # Criar uma lista de tuplas (probabilidade, numero)
        probabilidades_por_numero = list(zip(probabilidades, range(1, 50)))
        
        # Ordenar e selecionar os números com maior probabilidade
        probabilidades_por_numero.sort(key=lambda x: x[0], reverse=True)
        
        previsao_final = [numero for prob, numero in probabilidades_por_numero[:n_resultados]]
        
        return previsao_final
