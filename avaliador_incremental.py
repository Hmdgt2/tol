import os
import json
from collections import defaultdict
import sys

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats

# Caminhos de ficheiro
ULTIMO_SORTEIO_PATH = "decisor/sorteio_processado.json"
PREVISAO_ATUAL_PATH = "previsoes/previsao_atual.json"
RELATORIOS_DIR = "estatisticas"
HISTORICO_DADOS_PATH = "dados"

def carregar_dados_json(caminho):
    """Carrega dados de um ficheiro JSON."""
    if not os.path.exists(caminho):
        return None
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_relatorio_json(dados, caminho):
    """Salva dados em um ficheiro JSON com formatação."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def main():
    print("Iniciando a avaliação incremental das heurísticas...")
    
    # 1. Carregar o último sorteio e as previsões
    ultimo_sorteio = carregar_dados_json(ULTIMO_SORTEIO_PATH)
    previsoes_atuais = carregar_dados_json(PREVISAO_ATUAL_PATH)

    if not ultimo_sorteio or not previsoes_atuais:
        print("Dados do último sorteio ou previsões não encontrados. A sair.")
        return

    concurso_atual = ultimo_sorteio.get("concurso")
    resultado_real = set(ultimo_sorteio.get("numeros", []))

    # 2. Iterar sobre as previsões e atualizar os relatórios
    for nome_heuristica, numeros_previstos in previsoes_atuais.items():
        relatorio_path = os.path.join(RELATORIOS_DIR, f"{nome_heuristica}.json")
        relatorio = carregar_dados_json(relatorio_path)

        if not relatorio:
            print(f"Relatório para a heurística '{nome_heuristica}' não encontrado. A ignorar.")
            continue

        relatorio["total_previsoes"] += 1
        num_acertos = len(set(numeros_previstos).intersection(resultado_real))
        
        # 3. Atualizar as métricas de acerto
        for i in range(1, 6):
            if num_acertos >= i:
                relatorio["metricas_acerto"][f"acerto_{i}"]["total"] += 1
        
        # 4. Verificar se é a melhor previsão
        if num_acertos > relatorio["melhor_previsao"]["numeros_acertados"]:
            relatorio["melhor_previsao"] = {
                "concurso": concurso_atual,
                "data": ultimo_sorteio.get("data"),
                "numeros_acertados": num_acertos,
                "numeros_previstos_pico": sorted(list(numeros_previstos)),
                "numeros_reais_pico": sorted(list(resultado_real))
            }
        
        # 5. Recalcular as taxas de sucesso
        for i in range(1, 6):
            metrica = relatorio["metricas_acerto"][f"acerto_{i}"]
            total = relatorio["total_previsoes"]
            taxa = (metrica["total"] / total * 100) if total > 0 else 0
            metrica["taxa_sucesso"] = f"{taxa:.2f}%"

        # 6. Salvar o relatório atualizado
        salvar_relatorio_json(relatorio, relatorio_path)
        print(f"Relatório da heurística '{nome_heuristica}' atualizado com sucesso.")

if __name__ == "__main__":
    main()
