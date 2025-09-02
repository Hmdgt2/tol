# gerar_previsao.py

import os
import sys
import json
import datetime
import numpy as np
from typing import Dict, Any, List

# Adiciona o diretório raiz ao caminho do sistema para resolver caminhos relativos
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante
from lib.dados import Dados
from decisor.decisor_final import HeuristicDecisor

# --- Caminhos dos Ficheiros ---
DADOS_ATUAL_PATH = os.path.join(PROJECT_ROOT, 'dados', 'sorteio_atual.json')
CAMINHO_BASE_DECISOR = os.path.join(PROJECT_ROOT, 'decisor')
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
os.makedirs(PASTA_PREVISOES, exist_ok=True)


def gerar_previsao():
    """
    Gera a previsão final para o próximo sorteio usando o melhor modelo de ML.
    Sempre recalcula a previsão para garantir consistência com os modelos mais recentes.
    """
    print("Iniciando a geração da previsão...")

    try:
        # 1. Carregar os dados mais recentes para a previsão
        if not os.path.exists(DADOS_ATUAL_PATH):
            print(f"AVISO: Ficheiro de dados mais recente não encontrado em: {DADOS_ATUAL_PATH}.")
            print("Usando os dados do histórico para a previsão...")
            sorteio_mais_recente = {"concurso": "sem_concurso_recente"}
        else:
            with open(DADOS_ATUAL_PATH, 'r', encoding='utf-8') as f:
                sorteio_mais_recente = json.load(f)

        # 2. Carregar o histórico de sorteios e o despachante
        dados_manager = Dados()
        despachante = Despachante()
        todas_dependencias = despachante.obter_todas_dependencias()
        estatisticas_atuais, _ = dados_manager.obter_estatisticas(todas_dependencias)

        # 3. Obter as previsões das heurísticas (sempre recalculado)
        previsoes_heuristicas = despachante.get_previsoes(estatisticas_atuais)

        # 4. Formatar as previsões para o decisor
        detalhes_previsoes = [
            {'nome': nome, 'numeros': numeros_previstos}
            for nome, numeros_previstos in previsoes_heuristicas.items()
        ]

        # 5. Instanciar o decisor de ML e obter a previsão final (sempre recarregado)
        decisor_ml = HeuristicDecisor(caminho_base_decisor=CAMINHO_BASE_DECISOR)
        previsao_final_numeros = decisor_ml.predict(detalhes_previsoes)

        # 6. Organizar e salvar os resultados em ficheiros
        concurso_base = sorteio_mais_recente.get("concurso", "sem_concurso_recente")
        
        resultado_completo = {
            "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "baseado_em_sorteio": concurso_base,
            "previsao_modelo_ml": previsao_final_numeros,
            "previsoes_heuristicas": detalhes_previsoes
        }

        nome_ficheiro_completo = f"previsao_{concurso_base.replace('/', '-')}.json"
        caminho_ficheiro_completo = os.path.join(PASTA_PREVISOES, nome_ficheiro_completo)

        # Sobrescrever o arquivo de histórico
        with open(caminho_ficheiro_completo, 'w', encoding='utf-8') as f:
            json.dump(resultado_completo, f, indent=2, ensure_ascii=False)

        # Sobrescrever o arquivo de previsão mais recente
        caminho_previsao_atual = os.path.join(PASTA_PREVISOES, "previsao_atual.json")
        with open(caminho_previsao_atual, 'w', encoding='utf-8') as f:
            json.dump({"previsao_modelo_ml": previsao_final_numeros}, f, indent=2, ensure_ascii=False)

        print("\n--- Previsão Gerada ---")
        print(f"Baseada nos dados até ao sorteio: {concurso_base}")
        print("-" * 35)
        print("Números Sugeridos pelo Modelo de ML:", previsao_final_numeros)
        print("-" * 35)
        print(f"✅ Previsão completa salva em: {caminho_ficheiro_completo}")
        print(f"✅ Previsão resumida salva em: {caminho_previsao_atual}")

    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro ao gerar a previsão.")
        print(f"Detalhes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    gerar_previsao()
