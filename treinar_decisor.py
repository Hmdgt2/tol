# treinar_decisor.py
import os
import sys
import importlib
from collections import defaultdict

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
    """
    Carrega dados históricos, simula as previsões das heurísticas para cada sorteio
    e treina o decisor final.
    """
    sorteios_historico = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios_historico or not heuristicas:
        print("Dados ou heurísticas insuficientes para treinar o decisor.")
        return

    todas_as_previsoes = []
    
    # Gera as previsões das heurísticas para CADA sorteio histórico
    print("Simulando previsões de heurísticas para dados históricos...")
    for sorteio in sorteios_historico:
        stats = get_all_stats(sorteios_historico[:sorteios_historico.index(sorteio)])
        previsoes_sorteio_atual = {}
        for nome, funcao in heuristicas:
            # Assumindo que as heurísticas podem aceitar stats e histórico
            if nome in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes']:
                previsao = funcao(stats, sorteios_historico[:sorteios_historico.index(sorteio)], n=5)
            else:
                previsao = funcao(stats, n=5)
            previsoes_sorteio_atual[nome] = previsao
        todas_as_previsoes.append(previsoes_sorteio_atual)

    decisor = HeuristicDecisor(caminho_pesos=PESOS_PATH)
    print("A treinar o modelo de decisão...")
    decisor.fit(sorteios_historico, todas_as_previsoes)
    print("Treino concluído. Pesos guardados em:", PESOS_PATH)

if __name__ == '__main__':
    treinar_decisor()
