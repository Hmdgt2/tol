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
    def __init__(self, caminho_base_decisor: str):
        """
        Inicializa o decisor, carregando todos os pipelines de ML para um ensemble.

        Args:
            caminho_base_decisor (str): O caminho para a pasta 'decisor'.
        """
        self.modelos_dir = os.path.join(caminho_base_decisor, 'modelos_salvos')
        self.performance_path = os.path.join(self.modelos_dir, 'performance_modelos.json')
        self.metadados_path = os.path.join(caminho_base_decisor, 'metadados_modelo.json')
        self.pipelines: Dict[str, Any] = {}
        self.performance_data: Dict[str, Any] = {}

        try:
            # 1. Carrega o ficheiro de performance de todos os modelos
            with open(self.performance_path, 'r', encoding='utf-8') as f:
                self.performance_data = json.load(f)

            # 2. Carrega todos os pipelines salvos e suas pontuações de desempenho
            for modelo_nome, dados in self.performance_data.items():
                pipeline_path = dados['caminho']
                if os.path.exists(pipeline_path):
                    self.pipelines[modelo_nome] = joblib.load(pipeline_path)
                    print(f"Decisor: A carregar o modelo '{modelo_nome}' (Score: {dados['score_treino']:.4f})")
                else:
                    print(f"Aviso: Pipeline não encontrado para o modelo '{modelo_nome}' em: {pipeline_path}")
            
            if not self.pipelines:
                raise RuntimeError("Nenhum pipeline de modelo de ML válido foi encontrado.")

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Erro ao carregar os modelos. Detalhes: {e}")

        try:
            with open(self.metadados_path, 'r', encoding='utf-8') as f:
                self.metadados = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Ficheiro de metadados não encontrado em: {self.metadados_path}.")

        self.heuristicas_ordenadas = self.metadados.get('heuristicas_ordenadas', [])

    def _get_feature_vector(self, previsoes_atuais: List[Dict[str, Any]]) -> np.ndarray:
        """
        Cria um array NumPy de características (features) para um único sorteio.
        (A lógica desta função permanece a mesma)
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
        Faz a previsão usando o ensemble de modelos e retorna os 5 números mais prováveis.
        """
        feature_vectors = self._get_feature_vector(detalhes_previsoes)
        
        if feature_vectors.size == 0:
            return []
            
        probabilidades_combinadas = np.zeros(49)
        total_score = sum(d['score_treino'] for d in self.performance_data.values())
        
        # 1. Obter as probabilidades de cada modelo e ponderá-las
        for nome_modelo, pipeline in self.pipelines.items():
            score = self.performance_data[nome_modelo]['score_treino']
            peso = score / total_score # Peso proporcional ao score
            
            # O pipeline irá automaticamente normalizar os dados e fazer a previsão
            probabilidades = pipeline.predict_proba(feature_vectors)[:, 1]
            probabilidades_combinadas += probabilidades * peso
        
        # 2. Criar uma lista de tuplas (probabilidade, numero)
        probabilidades_por_numero = list(zip(probabilidades_combinadas, range(1, 50)))
        
        # 3. Ordenar e selecionar os números com maior probabilidade
        probabilidades_por_numero.sort(key=lambda x: x[0], reverse=True)
        
        previsao_final = [numero for prob, numero in probabilidades_por_numero[:n_resultados]]
        
        return previsao_final
