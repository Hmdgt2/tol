import os
import json
from collections import defaultdict, Counter

# Caminhos de ficheiro
RELATORIOS_DIR = "estatisticas"
RELATORIO_COMBINACOES_PATH = "estatisticas/relatorio_combinacoes.json"

def carregar_relatorios_de_heuristica():
    """Carrega todos os relatórios de heurísticas da pasta de relatórios."""
    relatorios = {}
    if not os.path.exists(RELATORIOS_DIR):
        print(f"A pasta de relatórios '{RELATORIOS_DIR}' não foi encontrada.")
        return relatorios

    for ficheiro in os.listdir(RELATORIOS_DIR):
        if ficheiro.endswith('.json') and ficheiro != os.path.basename(RELATORIO_COMBINACOES_PATH):
            caminho_ficheiro = os.path.join(RELATORIOS_DIR, ficheiro)
            with open(caminho_ficheiro, 'r', encoding='utf-8') as f:
                nome_heuristica = os.path.splitext(ficheiro)[0]
                relatorios[nome_heuristica] = json.load(f)
    return relatorios

def analisar_relatorios(relatorios):
    """Analisa todos os relatórios e gera um resumo combinado."""
    resumo_geral = {
        "resumo_acertos": {
            "acerto_1": {"total": 0, "media": 0.0},
            "acerto_2": {"total": 0, "media": 0.0},
            "acerto_3": {"total": 0, "media": 0.0},
            "acerto_4": {"total": 0, "media": 0.0},
            "acerto_5": {"total": 0, "media": 0.0}
        },
        "melhores_previsoes_por_acertos": {
            "acerto_5": [],
            "acerto_4": [],
            "acerto_3": []
        }
    }
    
    total_heurísticas = len(relatorios)
    if total_heurísticas == 0:
        return resumo_geral

    # Acumular totais e encontrar as melhores previsões
    for nome, dados in relatorios.items():
        for i in range(1, 6):
            total_acertos = dados["metricas_acerto"][f"acerto_{i}"]["total"]
            resumo_geral["resumo_acertos"][f"acerto_{i}"]["total"] += total_acertos
        
        num_acertos = dados["melhor_previsao"]["numeros_acertados"]
        if num_acertos in [3, 4, 5]:
            acertos_str = f"acerto_{num_acertos}"
            resumo_geral["melhores_previsoes_por_acertos"][acertos_str].append({
                "heuristica": nome,
                "concurso": dados["melhor_previsao"]["concurso"],
                "data": dados["melhor_previsao"]["data"],
                "numeros_acertados": num_acertos,
                "numeros_previstos": dados["melhor_previsao"].get("numeros_previstos_pico", [])
            })

    # Calcular médias
    total_previsoes_geral = sum(dados["total_previsoes"] for dados in relatorios.values())
    if total_previsoes_geral > 0:
        for i in range(1, 6):
            total_acertos = resumo_geral["resumo_acertos"][f"acerto_{i}"]["total"]
            media = (total_acertos / total_previsoes_geral * 100)
            resumo_geral["resumo_acertos"][f"acerto_{i}"]["media"] = f"{media:.2f}%"

    return resumo_geral

def main():
    print("Iniciando a análise combinada dos relatórios...")
    relatorios_carregados = carregar_relatorios_de_heuristica()
    
    if not relatorios_carregados:
        print("Nenhum relatório de heurística encontrado para analisar.")
        return

    relatorio_combinacoes = analisar_relatorios(relatorios_carregados)
    
    salvar_relatorio_json(relatorio_combinacoes, RELATORIO_COMBINACOES_PATH)
    print(f"Análise combinada concluída. Relatório guardado em: {RELATORIO_COMBINACOES_PATH}")

if __name__ == "__main__":
    main()
