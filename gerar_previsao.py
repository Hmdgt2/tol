import os
import sys
import json
from typing import Dict, Any, List

# Adiciona o diretório raiz para resolver importações
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importamos a nossa nova arquitetura
from lib.dados import _carregar_sorteios, obter_estatisticas
from lib.despachante import Despachante
from lib.decisor import HeuristicDecisor

# Define os caminhos dos ficheiros para a nova arquitetura
PASTA_PREVISOES = os.path.join(PROJECT_ROOT, 'previsoes')
FICHEIRO_PREVISAO = os.path.join(PASTA_PREVISOES, 'previsao_atual.json')
MODELO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_previsor.joblib')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')

def guardar_previsao_json(previsao_final: List[int], detalhes: List[Dict[str, Any]]):
    """Guarda a previsão final e os detalhes das heurísticas em um arquivo JSON."""
    os.makedirs(PASTA_PREVISOES, exist_ok=True)
    dados = {
        "previsao": previsao_final,
        "detalhes": detalhes
    }
    with open(FICHEIRO_PREVISAO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def gerar_previsao():
    """
    Gera uma previsão de números com base em múltiplas heurísticas
    e um decisor ponderado, utilizando a nova arquitetura modular.
    """
    try:
        # 1. Carrega o Despachante, que gerencia as heurísticas
        despachante = Despachante()
        
        # 2. Carrega o histórico de sorteios e obtém as dependências
        sorteios_historico = _carregar_sorteios()
        if not sorteios_historico:
            print("Erro: Nenhum sorteio histórico encontrado.")
            return

        todas_dependencias = despachante.get_todas_dependencias()

        # 3. Obtém as estatísticas necessárias de forma otimizada
        estatisticas = obter_estatisticas(todas_dependencias, sorteios_historico)
        
        # 4. Executa cada heurística usando o Despachante
        print("\n--- Previsões das Heurísticas ---\n")
        detalhes_previsoes = []
        previsoes_dict = despachante.get_previsoes(estatisticas)
        
        for nome, numeros in previsoes_dict.items():
            print(f"{nome:<35}: {sorted(numeros)}")
            detalhes_previsoes.append({"nome": nome, "numeros": sorted(numeros)})

        # 5. Inicializa o decisor com o novo pipeline completo
        print("\n--- Sugestão Final (Modelo de ML) ---")
        decisor = HeuristicDecisor(
            caminho_pipeline=MODELO_PATH,
            caminho_metadados=METADADOS_PATH
        )
        
        previsao_final = decisor.predict(detalhes_previsoes)
        
        print("Previsão Final (combinada):", sorted(previsao_final))
        print("---")
        
        # 6. Salva a previsão final
        guardar_previsao_json(sorted(previsao_final), detalhes_previsoes)

    except FileNotFoundError as e:
        print(f"Erro: Um ficheiro necessário não foi encontrado. {e}")
        print("Certifique-se de que treinou o modelo com 'treinar_decisor.py' primeiro.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    gerar_previsao()
