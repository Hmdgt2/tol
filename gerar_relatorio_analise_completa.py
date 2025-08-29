import os
import json
import importlib
from collections import defaultdict
import sys
import inspect

# Adiciona o diretório raiz ao caminho do sistema para importar as heurísticas e os dados
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats

# Caminhos de ficheiro
HEURISTICAS_DIR = "heuristicas"
RELATORIOS_DIR = "estatisticas"
ULTIMO_CONCURSO_PATH = os.path.join(RELATORIOS_DIR, "ultimo_concurso_analisado.json")

def carregar_heuristicas():
    """Carrega dinamicamente todas as heurísticas e suas descrições."""
    heuristicas = []
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                modulo = importlib.import_module(f"heuristicas.{nome_modulo}")
                if hasattr(modulo, 'prever'):
                    descricao = getattr(modulo, 'DESCRICAO', 'Descrição não disponível.')
                    heuristicas.append({"nome": nome_modulo, "funcao": modulo.prever, "descricao": descricao})
            except ImportError as e:
                print(f"Erro ao importar heurística {nome_modulo}: {e}")
    return heuristicas

def analisar_performance_detalhada(sorteios_historicos, previsoes_por_sorteio, descricoes_heuristicas):
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
        "melhor_previsao": {
            "concurso": None, 
            "data": None, 
            "numeros_acertados": -1, 
            "numeros_previstos_pico": [],
            "numeros_reais_pico": [],
            "indice_sorteio": -1
        },
        "desempenho_pos_pico": {
            "sorteios_apos": 0,
            "media_acertos_apos": 0.0
        }
    })

    sorteios_por_concurso = {s.get("concurso"): s.get("numeros", []) for s in sorteios_historicos if s.get("concurso")}
    
    lista_previsoes_ordenada = list(previsoes_por_sorteio.items())

    for idx_concurso, (concurso, previsao) in enumerate(lista_previsoes_ordenada):
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
                    "numeros_previstos_pico": sorted(list(numeros_previstos)),
                    "numeros_reais_pico": sorted(list(resultado_real)),
                    "indice_sorteio": idx_concurso
                }

    for nome, dados in relatorio.items():
        indice_pico = dados["melhor_previsao"]["indice_sorteio"]
        if indice_pico != -1:
            sorteios_apos = lista_previsoes_ordenada[indice_pico+1:]
            total_acertos_apos = 0
            
            for concurso_apos, previsao_apos in sorteios_apos:
                resultado_real_apos = set(sorteios_por_concurso.get(concurso_apos, []))
                previsao_heuristica_apos = previsao_apos.get(nome, [])
                num_acertos_apos = len(set(previsao_heuristica_apos).intersection(resultado_real_apos))
                total_acertos_apos += num_acertos_apos
                
            num_sorteios_apos = len(sorteios_apos)
            media_acertos = (total_acertos_apos / num_sorteios_apos) if num_sorteios_apos > 0 else 0.0
            
            dados["desempenho_pos_pico"] = {
                "sorteios_apos": num_sorteios_apos,
                "media_acertos_apos": round(media_acertos, 2)
            }
        
        for i in range(1, 6):
            metrica = dados["metricas_acerto"][f"acerto_{i}"]
            total = dados["total_previsoes"]
            taxa = (metrica["total"] / total * 100) if total > 0 else 0
            metrica["taxa_sucesso"] = f"{taxa:.2f}%"
        
        dados["descricao"] = descricoes_heuristicas.get(nome, "Descrição não disponível.")

    return dict(relatorio)

def main():
    print("A carregar sorteios para gerar relatórios de análise completos...")
    sorteios = carregar_sorteios()
    
    heuristicas_info = carregar_heuristicas()
    heuristicas = [(h['nome'], h['funcao']) for h in heuristicas_info]
    descricoes_heuristicas = {h['nome']: h['descricao'] for h in heuristicas_info}

    if not sorteios or not heuristicas:
        print("Dados ou heurísticas insuficientes para gerar relatórios.")
        return

    print("Simulando previsões de heurísticas para dados históricos...")
    previsoes_por_sorteio = defaultdict(dict)
    
    for i in range(len(sorteios) - 1):
        historico_parcial = sorteios[:i+1]
        estatisticas = get_all_stats(historico_parcial)
        
        for nome, funcao in heuristicas:
            parametros = inspect.signature(funcao).parameters
            
            if 'sorteios_historico' in parametros:
                resultado = funcao(estatisticas, n=5, sorteios_historico=historico_parcial)
            else:
                resultado = funcao(estatisticas, n=5)
            
            if resultado and 'numeros' in resultado:
                previsoes_por_sorteio[sorteios[i+1]['concurso']][nome] = resultado["numeros"]

    print("Pré-cálculo concluído. A gerar o relatório detalhado...")
    relatorio = analisar_performance_detalhada(sorteios, previsoes_por_sorteio, descricoes_heuristicas)

    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    
    # Apaga ficheiros JSON existentes na pasta de relatórios, exceto o novo de ponto de controlo
    for ficheiro in os.listdir(RELATORIOS_DIR):
        caminho_completo = os.path.join(RELATORIOS_DIR, ficheiro)
        if ficheiro.endswith('.json') and caminho_completo != ULTIMO_CONCURSO_PATH:
            os.remove(caminho_completo)
            
    # Salva o relatório para cada heurística
    for nome_heuristica, dados in relatorio.items():
        caminho_ficheiro = os.path.join(RELATORIOS_DIR, f"{nome_heuristica}.json")
        with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
            
    # Salva o número do último concurso analisado
    ultimo_concurso = sorteios[-1]['concurso']
    with open(ULTIMO_CONCURSO_PATH, 'w', encoding='utf-8') as f:
        json.dump({"ultimo_concurso_analisado": ultimo_concurso}, f, indent=2)
            
    print(f"Relatórios de análise completos gerados em: {RELATORIOS_DIR}")
    print(f"Ponto de controlo guardado: '{ULTIMO_CONCURSO_PATH}' com o concurso {ultimo_concurso}")

if __name__ == "__main__":
    main()
