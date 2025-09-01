# avaliador.py

import os
import sys
import json
import numpy as np
import joblib
from typing import Dict, Any, List

# Adicione o diretório raiz ao caminho do sistema para resolver caminhos relativos
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importamos a nossa nova arquitetura
from lib.dados import _carregar_sorteios, obter_estatisticas
from lib.despachante import Despachante
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# --- Caminhos dos Ficheiros ---
ULTIMO_SORTEIO_PROCESSADO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'sorteio_processado.json')
MODELO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'modelo_previsor.joblib')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
DADOS_ATUAL_PATH = os.path.join(PROJECT_ROOT, 'dados', 'sorteio_atual.json')

def carregar_sorteio_processado(path: str) -> Dict[str, str]:
    """Carrega o identificador do último sorteio processado."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"ultimo_concurso_processado": ""}

def guardar_sorteio_processado(concurso: str, path: str):
    """Guarda o identificador do sorteio que acabou de ser processado."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"ultimo_concurso_processado": concurso}, f, indent=2, ensure_ascii=False)

def avaliar_e_incrementar():
    """
    Verifica se há um novo sorteio para processar, e se houver,
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

    print(f"Novo sorteio '{concurso_atual}' detectado. A re-treinar o modelo com todos os dados...")

    # 2. Carrega todas as heurísticas e o histórico de sorteios
    despachante = Despachante()
    sorteios_historico = _carregar_sorteios()
    if not sorteios_historico or len(sorteios_historico) < 2:
        print("Histórico de sorteios insuficiente para treino.")
        return
    
    todas_dependencias = despachante.get_todas_dependencias()
    metadados_heuristicas = despachante.get_metadados()
    heuristicas_ordenadas = sorted(list(metadados_heuristicas.keys()))

    # 3. Recria o conjunto de treino com o histórico completo
    X_treino = []
    y_treino = []

    for i in range(len(sorteios_historico) - 1):
        historico_parcial = sorteios_historico[:i+1]
        sorteio_alvo = sorteios_historico[i+1]
        
        estatisticas_parciais = obter_estatisticas(todas_dependencias, historico_parcial)
        previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)
        
        for num in range(1, 50):
            feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
            X_treino.append(feature_vector)
            y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

    X_treino_np = np.array(X_treino)
    y_treino_np = np.array(y_treino)

    # 4. Re-treina o pipeline completo
    print("A re-treinar o pipeline de ML...")
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(solver='liblinear'))
    ])
    pipeline.fit(X_treino_np, y_treino_np)

    # 5. Salva o pipeline atualizado e o estado
    os.makedirs(os.path.dirname(MODELO_PATH), exist_ok=True)
    joblib.dump(pipeline, MODELO_PATH)
    guardar_sorteio_processado(concurso_atual, ULTIMO_SORTEIO_PROCESSADO_PATH)

    print(f"✅ Modelo atualizado com o sorteio '{concurso_atual}' e salvo em '{MODELO_PATH}'.")

if __name__ == "__main__":
    avaliar_e_incrementar()
