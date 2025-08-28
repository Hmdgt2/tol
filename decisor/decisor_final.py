# decisor/decisor_final.py
import os
import json
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
import numpy as np

class HeuristicDecisor:
    def __init__(self, caminho_pesos=None):
        self.caminho_pesos = caminho_pesos
        self.pesos = self.carregar_pesos()
        self.modelo_ml = LogisticRegression()

    def carregar_pesos(self):
        """Carrega os pesos do arquivo JSON se ele existir."""
        if self.caminho_pesos and os.path.exists(self.caminho_pesos):
            with open(self.caminho_pesos, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def guardar_pesos(self):
        """Guarda os pesos do modelo em um arquivo JSON."""
        if self.caminho_pesos and self.pesos:
            with open(self.caminho_pesos, 'w', encoding='utf-8') as f:
                json.dump(self.pesos, f, indent=4)

    def fit(self, historico_resultados, previsoes_heuristica):
        """
        Treina o modelo de ML para aprender os pesos ideais.
        """
        X = []  # As features (entradas)
        y = []  # Os rótulos (saídas, 1 se o número foi sorteado, 0 caso contrário)
        
        # Obter a lista de todas as heurísticas presentes nos dados
        todas_as_heuristicas = []
        if previsoes_heuristica:
            todas_as_heuristicas = list(previsoes_heuristica[0].keys())

        # Converte os dados em um formato que o modelo de ML entenda
        for i, sorteio_real in enumerate(historico_resultados):
            numeros_sorteados = set(sorteio_real.get('numeros', []))
            
            # Pega as previsões para este sorteio
            previsoes_atuais = previsoes_heuristica[i]
            
            for num in range(1, 50):  # Para cada número possível
                row = []
                for heuristica_nome in todas_as_heuristicas:
                    previsoes_num = previsoes_atuais.get(heuristica_nome, {}).get('numeros', [])
                    # A feature é 1 se a heurística sugeriu o número, 0 caso contrário
                    row.append(1 if num in previsoes_num else 0)
                
                X.append(row)
                y.append(1 if num in numeros_sorteados else 0)
        
        # Se houver dados, treina o modelo
        if X and y:
            self.modelo_ml.fit(X, y)
            
            # Guarda os pesos aprendidos pelo modelo
            self.pesos = {
                heuristica: peso for heuristica, peso in zip(todas_as_heuristicas, self.modelo_ml.coef_[0])
            }
            self.guardar_pesos()
            print("Modelo de decisor treinado com sucesso.")
        else:
            print("Dados insuficientes para treinar o modelo de decisor.")

    def predict(self, previsoes_heuristica_atual):
        """
        Faz a previsão final usando o modelo treinado.
        
        Args:
            previsoes_heuristica_atual (list): Lista de previsões de cada heurística para o próximo sorteio.
        """
        todas_as_heuristicas = list(self.pesos.keys())
        X_novo = []
        
        # Converte as previsões atuais para o formato de features
        for num in range(1, 50):
            row = []
            for heuristica_nome in todas_as_heuristicas:
                # Encontra a lista de números para a heurística atual
                numeros_previstos = []
                for item in previsoes_heuristica_atual:
                    if item['nome'] == heuristica_nome:
                        numeros_previstos = item.get('numeros', [])
                        break
                row.append(1 if num in numeros_previstos else 0)
            X_novo.append(row)

        if not hasattr(self.modelo_ml, 'predict_proba'):
            print("Erro: O modelo de ML não foi treinado. Usando pontuação baseada em pesos.")
            # Fallback para a lógica de pontuação simples se o modelo não foi treinado
            pontuacoes = defaultdict(float)
            for item in previsoes_heuristica_atual:
                nome = item["nome"]
                numeros = item["numeros"]
                peso = self.pesos.get(nome, 1.0)
                for num in numeros:
                    pontuacoes[num] += peso
            escolhidos = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
            return [num for num, _ in escolhidos[:5]]

        # Usa o modelo treinado para prever as probabilidades
        probabilidades = self.modelo_ml.predict_proba(X_novo)[:, 1]
        
        # Associa cada número à sua probabilidade
        pontuacoes = {i + 1: prob for i, prob in enumerate(probabilidades)}
        
        # Seleciona os 5 números com maior probabilidade
        escolhidos = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in escolhidos[:5]]

# Esta função de conveniência não é mais necessária com a nova lógica do 'gerar_previsao.py'
# Mas pode mantê-la se precisar dela para compatibilidade com outros scripts.
def decidir_final(detalhes, caminho_pesos=None):
    decisor = HeuristicDecisor(caminho_pesos)
    return decisor.predict(detalhes)
