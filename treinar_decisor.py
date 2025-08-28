import os
import sys
import importlib
from collections import defaultdict, Counter
from itertools import combinations
import json
import inspect

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa as funções de dados e o decisor
from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios
from decisor.decisor_final import HeuristicDecisor

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
PESOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'pesos_atuais.joblib')

def carregar_heuristicas():
    """
    Carrega dinamicamente todas as heurísticas do diretório 'heuristicas'.
    """
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
    """
    Treina o modelo decisor usando dados históricos.
    Otimizado para evitar recálculos excessivos.
    """
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    # --- ETAPA 1: PRÉ-CÁLCULO DAS PREVISÕES ---
    # Esta parte do código é a mais lenta, mas é executada apenas uma vez.
    print("Simulando previsões de heurísticas para dados históricos...")
    
    previsoes_por_sorteio = defaultdict(dict)
    
    # Loop para simular cada sorteio no histórico e gerar as previsões das heurísticas
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        
        # Calcula todas as estatísticas para o histórico parcial
        estatisticas = get_all_stats(historico_parcial)
        estatisticas['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(historico_parcial, num_sorteios=100)

        for nome, funcao in heuristicas:
            try:
                # Usa inspect para verificar a assinatura da função 'prever'
                parametros = inspect.signature(funcao).parameters
                
                # Chamada condicional para passar os argumentos corretos
                if 'sorteios_historico' in parametros:
                    resultado = funcao(estatisticas, historico_parcial, n=5)
                else:
                    resultado = funcao(estatisticas, n=5)
                
                # Armazena o resultado da previsão
                previsoes_por_sorteio[i][nome] = resultado.get("numeros", [])
            except Exception as e:
                # Se uma heurística falhar, o treino não é interrompido
                print(f"Erro inesperado na heurística {nome}: {e}")
                previsoes_por_sorteio[i][nome] = []

    print("Pré-cálculo concluído. A criar os dados de treino para o modelo de ML...")
    
    # --- ETAPA 2: CRIAÇÃO DOS DADOS DE TREINO E TREINO DO MODELO ---
    # Esta parte é extremamente rápida porque usa os dados pré-calculados.
    X_treino = []
    y_treino = []
    heuristicas_ordenadas = [nome for nome, _ in heuristicas]

    # Loop para gerar os vetores de treino a partir dos dados pré-calculados
    for i in range(len(sorteios_historico) - 1):
        sorteio_alvo = sorteios_historico[i+1]
        previsoes_sorteio_atual = previsoes_por_sorteio[i]
        
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_sorteio_atual.get(nome, []) else 0 for nome in heuristicas_ordenadas]
            X_treino.append(feature_vector)
            
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    if not X_treino:
        print("Nenhum dado de treino gerado.")
        return

    decisor = HeuristicDecisor(caminho_pesos=PESOS_PATH)
    print("A treinar o modelo de decisão...")
    decisor.fit(X_treino, y_treino, heuristicas_ordenadas)
    print("Treino concluído. Pesos guardados em:", PESOS_PATH)

if __name__ == '__main__':
    treinar_decisor()
