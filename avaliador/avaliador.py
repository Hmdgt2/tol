#tol/avaliador/avaliador.py

import os
import sys
import json
import numpy as np
import joblib
import datetime
import importlib
from typing import Dict, Any, List
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Adiciona o diretório raiz do projeto ao caminho do sistema.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa as classes e funções corretas para a nova estrutura do projeto
from lib.despachante import Despachante
from lib.dados import Dados

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# --- Caminhos dos Ficheiros ---
# O caminho para o ficheiro de estado, que deve estar na pasta 'decisor'
ULTIMO_SORTEIO_PROCESSADO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'sorteio_processado.json')
# O caminho para os dados do sorteio atual
DADOS_ATUAL_PATH = os.path.join(PROJECT_ROOT, 'dados', 'sorteio_atual.json')
# Novos caminhos para os ficheiros
MODELOS_DIR = os.path.join(PROJECT_ROOT, 'decisor', 'modelos_salvos')
PERFORMANCE_PATH = os.path.join(MODELOS_DIR, 'performance_modelos.json')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
MODELOS_ML_DIR = os.path.join(PROJECT_ROOT, 'modelos_ml')

if not os.path.exists(MODELOS_DIR):
    os.makedirs(MODELOS_DIR)

def carregar_sorteio_processado(path: str) -> Dict[str, str]:
    """Carrega o identificador do último sorteio processado."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            print(f"Aviso: Erro ao carregar o estado do processamento em '{path}'. Começando do zero.")
            return {"ultimo_concurso_processado": ""}
    return {"ultimo_concurso_processado": ""}

def guardar_sorteio_processado(concurso: str, path: str):
    """Guarda o identificador do sorteio que acabou de ser processado."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"ultimo_concurso_processado": concurso}, f, indent=2, ensure_ascii=False)

def carregar_modelos_ml():
    """Carrega dinamicamente todos os modelos de ML disponíveis."""
    modelos = {}
    if not os.path.exists(MODELOS_ML_DIR):
        print(f"Diretório de modelos de ML não encontrado: {MODELOS_ML_DIR}")
        return modelos
    
    for ficheiro in os.listdir(MODELOS_ML_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                # Usa importlib para carregar o módulo
                spec = importlib.util.spec_from_file_location(nome_modulo, os.path.join(MODELOS_ML_DIR, ficheiro))
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                
                # Procura por uma função get_model() no módulo
                if hasattr(modulo, 'get_model') and callable(modulo.get_model):
                    instance = modulo.get_model()
                    if hasattr(instance, 'fit') and hasattr(instance, 'predict'):
                        modelos[nome_modulo] = instance
            except ImportError as e:
                print(f"Aviso: Não foi possível importar o modelo {nome_modulo}. Erro: {e}")
    return modelos

def avaliar_e_incrementar():
    """
    Verifica se há um novo sorteio para processar e, se houver,
    re-treina o modelo com o histórico completo.
    """
    print("Iniciando a avaliação e atualização do modelo...")

    # 1. Carrega os dados do sorteio mais recente e verifica se já foi processado
    try:
        with open(DADOS_ATUAL_PATH, 'r', encoding='utf-8') as f:
            novo_sorteio = json.load(f)
        concurso_atual = novo_sorteio.get("concurso", "")
    except FileNotFoundError:
        print(f"Ficheiro de dados mais recente não encontrado em: {DADOS_ATUAL_PATH}. Nenhuma ação será feita.")
        return
    except json.JSONDecodeError:
        print(f"Erro ao ler o ficheiro {DADOS_ATUAL_PATH}. Verifique se o JSON está formatado corretamente.")
        return

    estado_processamento = carregar_sorteio_processado(ULTIMO_SORTEIO_PROCESSADO_PATH)
    ultimo_processado = estado_processamento.get("ultimo_concurso_processado", "")

    if concurso_atual == ultimo_processado:
        print(f"Sorteio '{concurso_atual}' já foi processado. Nenhuma ação necessária.")
        return

    print(f"Novo sorteio '{concurso_atual}' detectado. A re-treinar todos os modelos com os dados atualizados...")

    try:
        # 2. Carrega todas as heurísticas e o histórico de sorteios
        dados = Dados()
        sorteios_historico = dados.sorteios
        despachante = Despachante()
        todas_dependencias = despachante.obter_todas_dependencias()

        # Obtém a lista de heurísticas disponíveis a partir dos metadados.
        metadados_heuristicas = despachante.obter_metadados()
        heuristicas_ordenadas = sorted(list(metadados_heuristicas.keys()))

        if not heuristicas_ordenadas or not sorteios_historico or len(sorteios_historico) < 2:
            print("Dados ou heurísticas insuficientes para treino. O processo será encerrado.")
            return

        print("Simulando previsões de heurísticas para dados históricos...")
        X_treino = []
        y_treino = []
        
        for i in range(len(sorteios_historico) - 1):
            historico_parcial = sorteios_historico[:i+1]
            sorteio_alvo = sorteios_historico[i+1]
            
            # CORREÇÃO CRUCIAL:
            # O método 'get_previsoes' do despachante espera um dicionário de estatísticas,
            # não uma lista de sorteios. Criamos uma instância temporária de Dados
            # para calcular as estatísticas com base no histórico parcial.
            dados_parciais = Dados()
            dados_parciais.sorteios = historico_parcial
            estatisticas_parciais, _ = dados_parciais.obter_estatisticas(todas_dependencias)

            # Passa as estatísticas calculadas corretamente para o despachante.
            # Também removemos o `['previsoes']` que não existe no retorno do método.
            previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)

            for num in range(1, 50):
                feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
                X_treino.append(feature_vector)
                y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

        X_treino_np = np.array(X_treino)
        y_treino_np = np.array(y_treino)

        # 3. Carrega os modelos dinamicamente
        modelos_disponiveis = carregar_modelos_ml()
        if not modelos_disponiveis:
            print("Nenhum modelo de ML encontrado na pasta 'modelos_ml'. O treino será encerrado.")
            return

        resultados_treino = {}
        # 4. Treina e salva cada modelo
        print("\nConjunto de treino criado. Iniciando o treino dos modelos de ML...")
        for nome_modelo, modelo in modelos_disponiveis.items():
            print(f"Treinando o modelo: {nome_modelo}...")
            pipeline = Pipeline([
                ('scaler', StandardScaler()),
                ('model', modelo)
            ])
            pipeline.fit(X_treino_np, y_treino_np)

            # Avalia o modelo
            score_treino = pipeline.score(X_treino_np, y_treino_np)

            # Salva o pipeline
            modelo_path = os.path.join(MODELOS_DIR, f"{nome_modelo}_pipeline.joblib")
            joblib.dump(pipeline, modelo_path)

            resultados_treino[nome_modelo] = {
                'caminho': modelo_path,
                'score_treino': score_treino,
                'ultima_atualizacao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            print(f"✅ Modelo {nome_modelo} salvo com score: {score_treino:.4f}")

        # 5. Salva o ficheiro de performance
        with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
            json.dump(resultados_treino, f, indent=2, ensure_ascii=False)

        # 6. Salva os metadados das heurísticas
        json_data_metadados = {'heuristicas_ordenadas': heuristicas_ordenadas}
        with open(METADADOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_data_metadados, f, indent=2, ensure_ascii=False)

        print("\n✅ Treino de todos os modelos concluído com sucesso.")
        guardar_sorteio_processado(concurso_atual, ULTIMO_SORTEIO_PROCESSADO_PATH)
        print(f"✅ O sistema foi atualizado com o sorteio '{concurso_atual}'.")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: Ocorreu um erro durante o treino do modelo.")
        print(f"Detalhes: {e}")
        sys.exit(1)


if __name__ == "__main__":
    avaliar_e_incrementar()
