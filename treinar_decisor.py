# treinar_decisor.py
import os
import sys
import importlib
from collections import defaultdict, Counter
from itertools import combinations
import json

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats
from decisor.decisor_final import HeuristicDecisor

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
PESOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.json')

def carregar_heuristicas():
    heuristicas = []
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    heuristicas.append((nome_modulo, modulo.prever))
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
    return heuristicas

def treinar_decisor():
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    print("Simulando previsões de heurísticas para dados históricos...")
    
    X_treino = []
    y_treino = []

    # Iterar sobre cada sorteio no histórico, exceto o último
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        sorteio_alvo = sorteios_historico[i+1]
        
        # Calcula estatísticas com base no histórico parcial
        estatisticas = get_all_stats(historico_parcial)
        previsoes_sorteio_atual = {}
        
        for nome, funcao in heuristicas:
            # Chama a função 'prever' com os argumentos corretos para cada heurística
            try:
                if nome in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes']:
                    resultado = funcao(estatisticas, historico_parcial, n=5)
                else:
                    resultado = funcao(estatisticas, n=5)
                previsoes_sorteio_atual[nome] = resultado.get("numeros", [])
            except TypeError as e:
                # Trata o caso em que 'n' é um argumento duplicado.
                # Remove o argumento nomeado 'n' e tenta novamente.
                try:
                    if nome in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes']:
                        resultado = funcao(estatisticas, historico_parcial)
                    else:
                        resultado = funcao(estatisticas)
                    previsoes_sorteio_atual[nome] = resultado.get("numeros", [])
                except Exception as inner_e:
                    print(f"Erro na heurística {nome} após tentativa de correção: {inner_e}")
            except Exception as e:
                print(f"Erro inesperado na heurística {nome}: {e}")

        # Cria o vetor de features (X) e o vetor de labels (y) para o treino
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_sorteio_atual.get(nome, []) else 0 for nome, _ in heuristicas]
            X_treino.append(feature_vector)
            
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    decisor = HeuristicDecisor(caminho_pesos=PESOS_PATH)
    print("A treinar o modelo de decisão...")
    decisor.fit(X_treino, y_treino)
    print("Treino concluído. Pesos guardados em:", PESOS_PATH)

if __name__ == '__main__':
    treinar_decisor()
