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

# Adiciona a importação da nova função de estatísticas
from lib.dados import carregar_sorteios, get_all_stats, get_repeticoes_ultimos_sorteios
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
    
    # Lista de todas as heurísticas que vamos usar para criar o vetor de features
    heuristicas_ordenadas = [nome for nome, _ in heuristicas]

    # Iterar sobre cada sorteio no histórico, exceto o último, que não tem resultado para treinar
    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        sorteio_alvo = sorteios_historico[i+1]
        
        # Calcula as estatísticas e as repetições para o histórico parcial
        estatisticas = get_all_stats(historico_parcial)
        estatisticas['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(historico_parcial, num_sorteios=100)

        previsoes_sorteio_atual = {}
        
        for nome, funcao in heuristicas:
            try:
                # O CÓDIGO AQUI FOI CORRIGIDO
                # Ele agora passa sempre ambos os argumentos, `estatisticas` e `historico_parcial`,
                # e os valores padrão (`n=5`) são aplicados automaticamente.
                resultado = funcao(estatisticas, historico_parcial, n=5)
                previsoes_sorteio_atual[nome] = resultado.get("numeros", [])
            except Exception as e:
                print(f"Erro inesperado na heurística {nome}: {e}")
                previsoes_sorteio_atual[nome] = []
        
        # Cria o vetor de features (X) e o vetor de labels (y) para o treino
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_sorteio_atual.get(nome, []) else 0 for nome in heuristicas_ordenadas]
            X_treino.append(feature_vector)
            
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    if not X_treino:
        print("Nenhum dado de treino gerado.")
        return

    decisor = HeuristicDecisor(caminho_pesos=PESOS_PATH)
    print("A treinar o modelo de decisão...")
    # Passa as listas de features (X) e labels (y) diretamente para o fit
    decisor.fit(X_treino, y_treino, heuristicas_ordenadas)
    print("Treino concluído. Pesos guardados em:", PESOS_PATH)

if __name__ == '__main__':
    treinar_decisor()
