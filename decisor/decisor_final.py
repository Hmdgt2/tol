# decisor_final.py
import os
import json
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
import numpy as np

class HeuristicDecisor:
    def __init__(self, caminho_pesos=None):
        self.caminho_pesos = caminho_pesos
        self.pesos = self.carregar_pesos()
        # Inicializa o modelo de regressão logística que aprenderá os pesos
        self.modelo_ml = None

    def carregar_pesos(self):
        """Carrega os pesos de um arquivo JSON se ele existir."""
        if self.caminho_pesos and os.path.exists(self.caminho_pesos):
            with open(self.caminho_pesos, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def guardar_pesos(self):
        """Guarda os pesos do modelo em um arquivo JSON."""
        if self.caminho_pesos:
            with open(self.caminho_pesos, 'w', encoding='utf-8') as f:
                json.dump(self.pesos, f, indent=4)

    def fit(self, historico_resultados, previsoes_heuristica):
        """
        Treina o modelo de ML para aprender os pesos ideais.
        
        Args:
            historico_resultados (list): Lista de sorteios reais.
            previsoes_heuristica (list): Lista de listas de previsões de cada heurística.
        """
        X = [] # As features (entradas)
        y = [] # Os rótulos (saídas, 1 se o número foi sorteado, 0 caso contrário)
        
        todas_as_heuristicas = list(previsoes_heuristica[0].keys())
        
        # Converte os dados em um formato que o modelo de ML entenda
        for i, sorteio_real in enumerate(historico_resultados):
            numeros_sorteados = set(sorteio_real.get('numeros', []))
            
            # Pega as previsões para este sorteio
            previsoes_atuais = previsoes_heuristica[i]
            
            for num in range(1, 50): # Para cada número possível
                row = []
                for heuristica in todas_as_heuristicas:
                    previsoes_num = previsoes_atuais.get(heuristica, {}).get('numeros', [])
                    # A feature é 1 se a heurística sugeriu o número, 0 caso contrário
                    row.append(1 if num in previsoes_num else 0)
                
                X.append(row)
                y.append(1 if num in numeros_sorteados else 0)
        
        self.modelo_ml = LogisticRegression()
        self.modelo_ml.fit(X, y)
        
        # Guarda os pesos aprendidos pelo modelo
        self.pesos = {
            heuristica: peso for heuristica, peso in zip(todas_as_heuristicas, self.modelo_ml.coef_[0])
        }
        self.guardar_pesos()
        
    def predict(self, previsoes_heuristica):
        """
        Faz a previsão final usando os pesos aprendidos.
        
        Args:
            previsoes_heuristica (list): Lista de previsões de cada heurística para um sorteio.
        """
        pontuacoes = defaultdict(float)
        
        for item in previsoes_heuristica:
            nome = item["nome"]
            numeros = item["numeros"]
            peso = self.pesos.get(nome, 1.0)
            for num in numeros:
                pontuacoes[num] += peso
        
        escolhidos = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in escolhidos[:2]]

def decidir_final(detalhes, caminho_pesos=None):
    """
    Função de conveniência para usar o modelo sem a necessidade de instanciar a classe.
    Mantém a compatibilidade com o código antigo.
    """
    decisor = HeuristicDecisor(caminho_pesos)
    return decisor.predict(detalhes)
