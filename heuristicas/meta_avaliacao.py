# heuristicas/meta_avaliacao.py
from typing import Dict, Any, List
import os
import json

# --- Metadados da Heurística ---
# A meta-heurística precisa de um novo tipo de dependência: o histórico de desempenho.
NOME = "meta_avaliacao"
DESCRICAO = "Escolhe a heurística mais precisa dos últimos sorteios, com base nos resultados de treino."
# Esta heurística depende dos resultados de performance pré-calculados.
DEPENDENCIAS = ["precisao_posicional_historica", "frequencia_total", "ausencia_atual", "...todas as dependências das outras heurísticas"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na heurística mais precisa, conforme o histórico de treino.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende,
                             incluindo os resultados do treino.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos pela heurística vencedora.
    """
    # A meta-heurística precisa de um novo tipo de dado: o histórico de performance.
    # O 'treinar_decisor.py' será responsável por criar e atualizar este ficheiro.
    performance_historica = estatisticas.get('precisao_posicional_historica', {})

    if not performance_historica:
        # Se não houver dados de treino, retorna os números mais frequentes como um fallback.
        frequencia = estatisticas.get('frequencia_total', {})
        return sorted([num for num in frequencia.keys()][:n])

    # Encontra a heurística com a melhor pontuação global
    melhor_heuristica = None
    melhor_pontuacao = -1
    
    for nome_heuristica, dados_heuristica in performance_historica.items():
        # A pontuação pode ser a soma dos acertos ou uma métrica mais complexa.
        # Por enquanto, vamos somar os acertos nas diferentes posições.
        pontuacao_total = sum(dados_heuristica.values())
        if pontuacao_total > melhor_pontuacao:
            melhor_pontuacao = pontuacao_total
            melhor_heuristica = nome_heuristica
            
    # Chama a heurística vencedora com os dados necessários
    if melhor_heuristica:
        try:
            # Importa dinamicamente a heurística vencedora
            modulo = __import__(f"heuristicas.{melhor_heuristica}")
            funcao_prever = modulo.prever
            
            # Chama a função 'prever' da heurística vencedora
            # O orquestrador tem que garantir que todas as dependências da heurística vencedora
            # são fornecidas no dicionário 'estatisticas'.
            previsao_final = funcao_prever(estatisticas, n=n)
            return sorted(list(set(previsao_final)))
        except (ImportError, AttributeError):
            pass

    # Fallback caso algo falhe
    frequencia = estatisticas.get('frequencia_total', {})
    return sorted([num for num in frequencia.keys()][:n])
