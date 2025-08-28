# heuristicas/meta_avaliacao.py
import importlib
import os
import sys
from collections import defaultdict, Counter

# Adiciona o diretório raiz para importar outras bibliotecas
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import get_all_stats, get_repeticoes_ultimos_sorteios

def carregar_outras_heuristicas():
    """Carrega dinamicamente todas as funções 'prever' de outras heurísticas."""
    heuristicas = []
    # Itera sobre os ficheiros na mesma pasta, excluindo este próprio ficheiro
    for ficheiro in os.listdir(PROJECT_ROOT):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__') and ficheiro != 'meta_avaliacao.py':
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    heuristicas.append((nome_modulo, modulo.prever))
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
            except Exception as e:
                print(f"Erro inesperado ao carregar heurística {nome_modulo}: {e}")
    return heuristicas

def prever(estatisticas, sorteios_historico, n=6, periodo_analise=50):
    """
    Prevê números com base no desempenho histórico das outras heurísticas.

    Args:
        estatisticas (dict): Dicionário com todas as estatísticas pré-calculadas.
        sorteios_historico (list): Lista dos sorteios históricos para análise.
        n (int): O número de sugestões a retornar (normalmente 6).
        periodo_analise (int): Número de sorteios anteriores a considerar.

    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    outras_heuristicas = carregar_outras_heuristicas()

    if len(sorteios_historico) < periodo_analise + 1 or not outras_heuristicas:
        return {
            "nome": "meta_avaliacao",
            "numeros": []
        }

    pontuacoes_heuristica = defaultdict(int)

    # Iterar sobre um período de sorteios passados
    for i in range(len(sorteios_historico) - periodo_analise - 1, len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        sorteio_alvo = sorteios_historico[i+1]
        
        # Recalcular as estatísticas para o histórico parcial
        estatisticas_parcial = get_all_stats(historico_parcial)
        estatisticas_parcial['repeticoes_ultimos_sorteios'] = get_repeticoes_ultimos_sorteios(historico_parcial, num_sorteios=100)

        # Simular e avaliar as previsões de cada heurística
        for nome, funcao in outras_heuristicas:
            try:
                # Adaptação para heurísticas que precisam do histórico completo
                if nome in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes', 'soma_numeros']:
                    previsao = funcao(estatisticas_parcial, historico_parcial, n=n)
                else:
                    previsao = funcao(estatisticas_parcial, n=n)

                acertos = set(previsao.get('numeros', [])).intersection(set(sorteio_alvo.get('numeros', [])))
                pontuacoes_heuristica[nome] += len(acertos)
            except Exception as e:
                # Ignorar heurísticas que falham na simulação
                pass
    
    if not pontuacoes_heuristica:
        return {
            "nome": "meta_avaliacao",
            "numeros": []
        }

    # Encontrar a heurística com a melhor pontuação
    heuristica_vencedora = max(pontuacoes_heuristica, key=pontuacoes_heuristica.get)
    print(f"A heurística mais precisa nos últimos {periodo_analise} sorteios é: {heuristica_vencedora}")
    
    # Gerar a previsão final usando a heurística vencedora e os dados mais recentes
    funcao_vencedora = next(funcao for nome, funcao in outras_heuristicas if nome == heuristica_vencedora)

    # Certifica-se de que a função vencedora recebe os argumentos corretos
    if heuristica_vencedora in ['padrao_finais', 'quentes_frios', 'repeticoes_sorteios_anteriores', 'tendencia_recentes', 'soma_numeros']:
        previsao_final = funcao_vencedora(estatisticas, sorteios_historico, n=n)
    else:
        previsao_final = funcao_vencedora(estatisticas, n=n)

    return {
        "nome": "meta_avaliacao",
        "numeros": sorted(list(set(previsao_final.get('numeros', []))))
    }
