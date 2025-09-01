# gerar_previsao.py

import os
import sys
import json
import datetime
from typing import Dict, Any, List

# Adiciona o diretório raiz ao caminho do sistema para resolver caminhos relativos
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante
from lib.dados import _carregar_sorteios, obter_estatisticas
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
        
        # 2. Carregar as heurísticas e calcular as estatísticas necessárias
        despachante = Despachante()
        todas_dependencias = despachante.get_todas_dependencias()
        sorteios_historico = _carregar_sorteios()
        estatisticas_completas = obter_estatisticas(todas_dependencias, sorteios_historico)

        # 3. Obter as previsões de cada heurística para o sorteio mais recente
        previsoes_heuristicas = despachante.get_previsoes(estatisticas_completas)
        
        # Formata as previsões para a entrada do decisor
        detalhes_previsoes = [
            {'nome': nome, 'numeros': numeros_previstos}
            for nome, numeros_previstos in previsoes_heuristicas.items()
        ]

        # 4. Instanciar o decisor de ML e obter a previsão final
        decisor_ml = HeuristicDecisor(caminho_base_decisor=CAMINHO_BASE_DECISOR)
        previsao_final_numeros = decisor_ml.predict(detalhes_previsoes)
        
        # 5. Organizar os resultados para salvar em um ficheiro
        resultado_completo = {
            "data_geracao": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "baseado_em_sorteio": sorteio_mais_recente.get("concurso"),
            "previsao_modelo_ml": previsao_final_numeros,
            "previsoes_heuristicas": detalhes_previsoes
        }
        
        # 6. Salvar os resultados em um ficheiro JSON
        nome_ficheiro = f"previsao_{sorteio_mais_recente.get('concurso').replace('/', '-')}.json"
        caminho_ficheiro = os.path.join(PASTA_PREVISOES, nome_ficheiro)
        
        with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
            json.dump(resultado_completo, f, indent=2, ensure_ascii=False)
            
        print("\n--- Previsão Gerada ---")
        print(f"Baseada nos dados até ao sorteio: {sorteio_mais_recente.get('concurso')}")
        print("-" * 35)
        print("Números Sugeridos pelo Modelo de ML:", previsao_final_numeros)
        print("-" * 35)
        print(f"✅ Previsão completa salva em: {caminho_ficheiro}")

    except Exception as e:
        print(f"\n❌ ERRO: Ocorreu um erro ao gerar a previsão.")
        print(f"Detalhes: {e}")
        sys.exit(1)

if __name__ == "__main__":
    gerar_previsao()
