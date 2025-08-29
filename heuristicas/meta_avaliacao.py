# heuristicas/meta_avaliacao.py
import os
import sys
import importlib

DESCRICAO = "Escolhe a heurística mais precisa dos últimos sorteios."

# Adiciona o diretório raiz para importações
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, '..', 'heuristicas')

def carregar_heuristicas_internas():
    """Carrega dinamicamente todas as heurísticas exceto a meta_avaliacao."""
    heuristicas = {}
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__') and ficheiro != 'meta_avaliacao.py':
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    heuristicas[nome_modulo] = modulo.prever
            except ImportError as e:
                pass  # Ignora heurísticas com erros para não interromper a meta
    return heuristicas

# Cache para armazenar os resultados de precisão e evitar recálculos
precisao_cache = {}

def prever(estatisticas, sorteios_historico, n=5, periodo_analise=50, **kwargs):
    """
    Prevê números com base na heurística mais precisa nos últimos sorteios.
    Otimizado para não recalcular a precisão a cada chamada.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas do histórico.
        sorteios_historico (list): Lista dos sorteios para análise.
        n (int): O número de sugestões a retornar.
        periodo_analise (int): O número de sorteios recentes para avaliar a precisão.

    Returns:
        dict: Um dicionário com o nome da heurística e os números sugeridos.
    """
    global precisao_cache
    
    # Se a heurística não for chamada com um histórico completo, não pode avaliar
    if len(sorteios_historico) < periodo_analise + 1:
        return {
            "nome": "meta_avaliacao",
            "numeros": []
        }

    # Verifica se o resultado já está no cache para evitar recálculo
    hist_key = len(sorteios_historico)
    if hist_key in precisao_cache:
        return precisao_cache[hist_key]

    heuristicas_internas = carregar_heuristicas_internas()
    precisoes = {}

    # Avalia a precisão de cada heurística nos últimos sorteios
    for nome, funcao in heuristicas_internas.items():
        acertos_totais = 0
        sorteios_avaliados = sorteios_historico[-periodo_analise:]
        
        for i in range(len(sorteios_avaliados) - 1):
            hist_parcial = sorteios_avaliados[:i+1]
            sorteio_alvo = sorteios_avaliados[i+1]
            
            # Garante que as heurísticas recebam os argumentos corretos
            try:
                if 'sorteios_historico' in funcao.__code__.co_varnames:
                    previsao = funcao(estatisticas, hist_parcial, n=6)
                else:
                    previsao = funcao(estatisticas, n=6)
            except:
                previsao = {"numeros": []}
                
            acertos = set(previsao.get("numeros", [])).intersection(set(sorteio_alvo.get("numeros", [])))
            acertos_totais += len(acertos)
        
        precisoes[nome] = acertos_totais / (periodo_analise * 6) if periodo_analise > 0 else 0

    if not precisoes or max(precisoes.values()) == 0:
        return {
            "nome": "meta_avaliacao",
            "numeros": []
        }

    heuristica_vencedora = max(precisoes, key=precisoes.get)
    funcao_vencedora = heuristicas_internas[heuristica_vencedora]

    # Previsão final com a heurística vencedora
    try:
        if 'sorteios_historico' in funcao_vencedora.__code__.co_varnames:
            resultado_final = funcao_vencedora(estatisticas, sorteios_historico, n=n)
        else:
            resultado_final = funcao_vencedora(estatisticas, n=n)
    except:
        resultado_final = {"numeros": []}

    # Armazena e retorna a previsão
    previsao_final = {
        "nome": "meta_avaliacao",
        "numeros": sorted(list(set(resultado_final.get("numeros", []))))
    }
    
    precisao_cache[hist_key] = previsao_final
    return previsao_final
