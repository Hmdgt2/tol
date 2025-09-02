# gerar_previsao.py

import os
import sys
import json
import datetime
import numpy as np
from typing import Dict, Any, List

# CORREÇÃO: Este script está na raiz do projeto, então apenas subimos um nível.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante
from lib.dados import Dados  # Importa a classe Dados, que é a forma correta agora
from decisor.decisor_final import HeuristicDecisor

# --- Caminhos dos Ficheiros ---
DADOS_ATUAL_PATH = os.path.join(PROJECT_ROOT, 'dados', 'sorteio_atual.json')
CAMINHO_BASE_DECISOR = os.path.join(PROJECT_ROOT, 'decisor')
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
os.makedirs(PASTA_PREVISOES, exist_ok=True)


def gerar_previsao():
    """
    Gera a previsão final para o próximo sorteio usando o melhor modelo de ML.
    """
    print("Iniciando a geração da previsão...")

    try:
        # 1. Carregar os dados mais recentes para a previsão
        if not os.path.exists(DADOS_ATUAL_PATH):
            print(f"Ficheiro de dados mais recente não encontrado em: {DADOS_ATUAL_PATH}.")
            print("Execute o script de scraping para obter os dados mais recentes.")
            return

        with open(DADOS_ATUAL_PATH, 'r', encoding='utf-8') as f:
            sorteio_mais_recente = json.load(f)

        # 2. Carregar o histórico de sorteios
        dados_manager = Dados()
        sorteios_historico = dados_manager.sorteios
        
        # 3. Carregar o despachante e dependências
        despachante = Despachante()
        todas_dependencias = despachante.obter_todas_dependencias()

        # 4. Obter as estatísticas mais recentes para a previsão
        estatisticas_atuais, _ = dados_manager.obter_estatisticas(todas_dependencias)

        # 5. Obter as previsões das heurísticas e logs de erro
        resultados_processamento = despachante.get_previsoes(estatisticas_atuais)
        
        previsoes_heuristicas = resultados_processamento['previsoes']
        logs = resultados_processamento['logs']
        
        # Opcional: imprimir logs de erro aqui para o utilizador saber o que se passa
        if logs['erros_estatisticas'] or logs['erros_heuristicas']:
            print("\n--- Avisos durante o Processamento ---")
            if logs['erros_estatisticas']:
                print("❌ Erros no Cálculo de Estatísticas:")
                for erro in logs['erros_estatisticas']:
                    print(f"  - {erro}")
            if logs['erros_heuristicas']:
                print("\n⚠️ Erros na Execução das Heurísticas:")
                for erro in logs['erros_heuristicas']:
                    print(f"  - {erro}")
        
        # 6. Formatar as previsões para a entrada do decisor
        detalhes_previsoes = [
            {'nome': nome, 'numeros': numeros_previstos}
            for nome, numeros_previstos in previsoes_heuristicas.items()
        ]

        # 7. Instanciar o decisor de ML e obter a previsão final
        decisor_ml = HeuristicDecisor(caminho_base_decisor=CAMINHO_BASE_DECISOR)
        previsao_final_numeros = decisor_ml.predict(detalhes_previsoes)
        
        # 8. Organizar e salvar os resultados em ficheiros
        resultado_completo = {
            "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "baseado_em_sorteio": sorteio_mais_recente.get("concurso"),
            "previsao_modelo_ml": previsao_final_numeros,
            "previsoes_heuristicas": detalhes_previsoes
        }
        
        nome_ficheiro_completo = f"previsao_{sorteio_mais_recente.get('concurso').replace('/', '-')}.json"
        caminho_ficheiro_completo = os.path.join(PASTA_PREVISOES, nome_ficheiro_completo)
        
        with open(caminho_ficheiro_completo, 'w', encoding='utf-8') as f:
            json.dump(resultado_completo, f, indent=2, ensure_ascii=False)

        caminho_previsao_atual = os.path.join(PASTA_PREVISOES, "previsao_atual.json")
        with open(caminho_previsao_atual, 'w', encoding='utf-8') as f:
            json.dump({"previsao_modelo_ml": previsao_final_numeros}, f, indent=2, ensure_ascii=False)
            
        print("\n--- Previsão Gerada ---")
        print(f"Baseada nos dados até ao sorteio: {sorteio_mais_recente.get('concurso')}")
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
