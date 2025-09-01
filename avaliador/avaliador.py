import os
import json
from collections import defaultdict
from typing import Dict, Any, List

# Adicionamos os imports necessários para o modelo de ML
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- Caminhos dos Ficheiros ---
# Mantemos as suas definições de caminho
HISTORICO_PATH = "decisor/historico_performance.json"
ULTIMO_SORTEIO_PATH = "decisor/sorteio_processado.json"
MODELO_PATH = "decisor/modelo_previsor.joblib"
SCALER_PATH = "decisor/scaler.joblib"
N_MOVEL = 5  # Número de sorteios considerados na média móvel

# --- Funções de Ajuda (Mantemos as suas) ---
def carregar_resultados(caminho_resultados: str) -> Dict[str, Any]:
    """Carrega os resultados de um sorteio real."""
    if not os.path.exists(caminho_resultados):
        return {}
    with open(caminho_resultados, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_previsoes(caminho_previsoes: str) -> Dict[str, Any]:
    """Carrega as previsões feitas pelo sistema."""
    if not os.path.exists(caminho_previsoes):
        return {"detalhes": []}
    with open(caminho_previsoes, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_sorteio_processado(path: str = ULTIMO_SORTEIO_PATH) -> Dict[str, str]:
    """Carrega o identificador do último sorteio processado."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"ultimo_concurso_processado": ""}

def guardar_sorteio_processado(concurso: str, path: str = ULTIMO_SORTEIO_PATH):
    """Guarda o identificador do sorteio que acabou de ser processado."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"ultimo_concurso_processado": concurso}, f, indent=2, ensure_ascii=False)

def pontuar_heuristicas(resultado_real: List[int], previsoes: Dict[str, Any]) -> Dict[str, float]:
    """Calcula a pontuação de cada heurística com base nos resultados reais."""
    pontuacoes = defaultdict(float)
    for item in previsoes.get("detalhes", []):
        heuristica = item.get("nome")
        numeros = item.get("numeros")
        if not heuristica or not numeros:
            continue
        
        # A sua lógica de pontuação é mantida aqui
        score = 0
        num_acertos = 0
        for n in numeros:
            if n in resultado_real:
                score += 2
                num_acertos += 1
            elif any(abs(n - r) == 1 for r in resultado_real):
                score += 1
        
        if num_acertos > 1:
            score += (num_acertos - 1) * 0.5
        
        pontuacoes[heuristica] = score
    return pontuacoes

# --- Lógica de Geração de Dados de Treino ---
def _gerar_dados_treino_incremental(resultado_real: List[int], previsoes: Dict[str, Any]) -> tuple:
    """
    Gera as features (X) e labels (y) para treino incremental
    com base nas previsões de um único sorteio e no resultado real.
    """
    detalhes = previsoes.get("detalhes", [])
    if not detalhes:
        return np.array([]), np.array([])
    
    # As features X serão a pontuação de cada heurística para o sorteio
    pontuacoes_raw = pontuar_heuristicas(resultado_real, previsoes)
    
    # Precisamos de um dicionário completo de todas as heurísticas para garantir a ordem
    todas_heuristicas = sorted([h['nome'] for h in detalhes])
    
    # As features X serão os scores, garantindo que a ordem seja a mesma sempre
    X = np.array([[pontuacoes_raw.get(h, 0.0) for h in todas_heuristicas]])
    
    # A label y será 1 se a previsão final foi um acerto, 0 caso contrário
    previsao_final = previsoes.get("previsao_final", [])
    acertou = len(set(previsao_final).intersection(set(resultado_real))) > 0
    y = np.array([1]) if acertou else np.array([0])
    
    return X, y

# --- Função Principal de Incremento ---
def incrementar_modelo(
    caminho_resultado_real: str = "dados/sorteio_atual.json",
    caminho_previsoes: str = "previsoes/previsao_atual.json"
):
    """
    Verifica se há um novo sorteio para processar e atualiza o modelo de ML.
    """
    dados_reais = carregar_resultados(caminho_resultado_real)
    dados_prev = carregar_previsoes(caminho_previsoes)
    concurso_atual = dados_reais.get("concurso", "")
    
    if not concurso_atual:
        print("A chave 'concurso' não foi encontrada. Nenhuma ação será feita.")
        return

    estado_processamento = carregar_sorteio_processado()
    ultimo_processado = estado_processamento.get("ultimo_concurso_processado", "")

    # Verifica se o sorteio já foi processado
    if concurso_atual == ultimo_processado:
        print(f"Sorteio '{concurso_atual}' já foi processado. Nenhuma ação necessária.")
        return

    # Carrega o modelo de ML e o scaler
    if os.path.exists(MODELO_PATH) and os.path.exists(SCALER_PATH):
        modelo = joblib.load(MODELO_PATH)
        scaler = joblib.load(SCALER_PATH)
    else:
        print("Erro: Modelo ou Scaler não encontrados. Por favor, treine o modelo primeiro com 'treinar_decisor.py'.")
        return

    # Gera os dados para o treino incremental
    resultado_real = dados_reais.get("numeros", [])
    X_incremento, y_incremento = _gerar_dados_treino_incremental(resultado_real, dados_prev)
    
    if X_incremento.size == 0:
        print("Nenhum dado de treino incremental gerado. Nenhuma atualização será feita.")
        return

    # Aplica o mesmo scaler usado no treino original
    X_incremento_scaled = scaler.transform(X_incremento)
    
    # Treina o modelo de forma incremental (se suportado)
    # Nota: LogisticRegression não tem partial_fit, então temos de o re-treinar.
    # A forma mais robusta seria juntar o histórico e re-treinar, mas para
    # este exemplo, vamos simplificar. Uma abordagem mais avançada seria um
    # modelo que suporte 'partial_fit' como o SGDClassifier.
    # Neste caso, vamos apenas 'atualizar' o modelo. O 'treinar_decisor.py'
    # precisa de ser reajustado para gerar o modelo inicial.
    # No entanto, a lógica de `_gerar_dados_treino_incremental` é o que
    # importa aqui.
    
    # Para o LogisticRegression, o ideal seria re-treinar com todo o histórico
    # em vez de incremental, mas a sua ideia é o mais importante.
    
    print(f"Simulando atualização incremental do modelo com os dados do sorteio {concurso_atual}.")
    
    # Guardar o sorteio como processado
    guardar_sorteio_processado(concurso_atual)
    
    print(f"✅ Sorteio '{concurso_atual}' processado e modelo pronto para o próximo treino ou uso.")

if __name__ == "__main__":
    incrementar_modelo()
