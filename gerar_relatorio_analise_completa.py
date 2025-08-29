# gerar_relatorio_analise_completa.py

import os
import json
import importlib
from collections import defaultdict, Counter
from itertools import combinations
import re
import sys

# Adiciona o diretório raiz ao caminho do sistema para importar as heurísticas e os dados
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats

# Caminhos de ficheiro
HEURISTICAS_DIR = "heuristicas"
RELATORIOS_DIR = "analise_heuristicas"

def carregar_heuristicas():
    """Carrega dinamicamente todas as heurísticas."""
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

def analisar_performance_detalhada(sorteios_historicos, previsoes_por_sorteio):
    """Gera um relatório detalhado de desempenho das heurísticas."""
    relatorio = defaultdict(lambda: {
        "nome_heuristica": "",
        "descricao": "",
        "total_previsoes": 0,
        "metricas_acerto": {
            "acerto_1": {"total": 0, "taxa_sucesso": 0.0},
            "acerto_2": {"total": 0, "taxa_sucesso": 0.0},
            "acerto_3": {"total": 0, "taxa_sucesso": 0.0},
            "acerto_4": {"total": 0, "taxa_sucesso": 0.0},
            "acerto_5": {"total": 0, "taxa_sucesso": 0.0}
        },
        "melhor_previsao": {"concurso": None, "data": None, "numeros_acertados": -1, "numeros_previstos": []}
    })

    sorteios_por_concurso = {s.get("concurso"): s.get("numeros", []) for s in sorteios_historicos if s.get("concurso")}
    
    for concurso, previsao in previsoes_por_sorteio.items():
        resultado_real = set(sorteios_por_concurso.get(concurso, []))
        
        for nome_heuristica, numeros_previstos in previsao.items():
            relatorio[nome_heuristica]["total_previsoes"] += 1
            num_acertos = len(set(numeros_previstos).intersection(resultado_real))
            
            for i in range(1, 6):
                if num_acertos >= i:
                    relatorio[nome_heuristica]["metricas_acerto"][f"acerto_{i}"]["total"] += 1

            if num_acertos > relatorio[nome_heuristica]["melhor_previsao"]["numeros_acertados"]:
                relatorio[nome_heuristica]["melhor_previsao"] = {
                    "concurso": concurso,
                    "data": next((s['data'] for s in sorteios_historicos if s.get('concurso') == concurso), None),
                    "numeros_acertados": num_acertos,
                    "numeros_previstos": numeros_previstos
                }

    for nome, dados in relatorio.items():
        dados["nome_heuristica"] = nome
        for i in range(1, 6):
            metrica = dados["metricas_acerto"][f"acerto_{i}"]
            total = dados["total_previsoes"]
            taxa = (metrica["total"] / total * 100) if total > 0 else 0
            metrica["taxa_sucesso"] = f"{taxa:.2f}%"

    return dict(relatorio)

def main():
    print("A carregar sorteios para gerar relatórios de análise completos...")
    sorteios = carregar_sorteios()
    heuristicas = carregar_heuristicas()

    if not sorteios or not heuristicas:
        print("Dados ou heurísticas insuficientes para gerar relatórios.")
        return

    print("Simulando previsões de heurísticas para dados históricos...")
    previsoes_por_sorteio = defaultdict(dict)
    
    # Iterate over all draws except the last one, to simulate the historical data
    for i in range(len(sorteios) - 1):
        # Grab the partial history up to the previous draw
        historico_parcial = sorteios[:i+1]
        
        # Recalculate stats based on the partial history
        estatisticas = get_all_stats(historico_parcial)
        
        # For each heuristic, use the "prever" function to generate a prediction
        for nome, funcao in heuristicas:
            # Pass the partial list of historical draws to the prever function
            try:
                # Try calling the prever function with the new argument
                resultado = funcao(estatisticas, n=5, sorteios_historico=historico_parcial)
                
                if resultado and 'numeros' in resultado:
                    previsoes_por_sorteio[sorteios[i+1]['concurso']][nome] = resultado["numeros"]
            except TypeError as e:
                # If the heuristic doesn't accept the new argument, try the original call
                if "missing 1 required positional argument: 'sorteios_historico'" in str(e):
                    print(f"Aviso: Heurística '{nome}' não aceita 'sorteios_historico'. A tentar chamada original.")
                    resultado = funcao(estatisticas, n=5)
                    if resultado and 'numeros' in resultado:
                        previsoes_por_sorteio[sorteios[i+1]['concurso']][nome] = resultado["numeros"]
                else:
                    raise e

    print("Pré-cálculo concluído. A gerar o relatório detalhado...")
    relatorio = analisar_performance_detalhada(sorteios, previsoes_por_sorteio)

    # ... (code to save the report) ...
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    for ficheiro in os.listdir(RELATORIOS_DIR):
        if ficheiro.endswith('.json'):
            os.remove(os.path.join(RELATORIOS_DIR, ficheiro))
            
    for nome_heuristica, dados in relatorio.items():
        caminho_ficheiro = os.path.join(RELATORIOS_DIR, f"{nome_heuristica}.json")
        with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
            
    print(f"Relatórios de análise completos gerados em: {RELATORIOS_DIR}")

if __name__ == "__main__":
    main()
