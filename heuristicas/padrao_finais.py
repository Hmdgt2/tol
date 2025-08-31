# heuristicas/padrao_finais.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "padrao_finais"
DESCRICAO = "Sugere números com terminações semelhantes ao último sorteio."
# Esta heurística precisa de uma estatística que liga a terminação do último sorteio
# com a frequência de terminações nos sorteios seguintes.
DEPENDENCIAS = ["frequencia_terminacoes_padrao", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base nas terminações mais prováveis após o último sorteio.

    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acede à estatística pré-calculada do padrão de terminações
    frequencia_padrao = estatisticas.get('frequencia_terminacoes_padrao', {})
    frequencia_total = estatisticas.get('frequencia_total', {})
    
    if not frequencia_padrao or not frequencia_total:
        return []

    # A estatística 'frequencia_terminacoes_padrao' deve ter a forma:
    # { term_do_ultimo_sorteio: { term_seguinte: frequencia, ... } }
    
    # Encontra a terminação mais provável para o próximo sorteio, com base
    # nas terminações do último sorteio (que estão no 'estatisticas').
    terminacoes_sorteio_atual = estatisticas.get('terminacoes_sorteio_atual', [])
    if not terminacoes_sorteio_atual:
        return []

    contador_terminacoes_sugeridas = Counter()
    for term_atual in terminacoes_sorteio_atual:
        if term_atual in frequencia_padrao:
            contador_terminacoes_sugeridas.update(frequencia_padrao[term_atual])
    
    # Se não houver padrão, a lista ficará vazia.
    terminacoes_comuns = [t for t, _ in contador_terminacoes_sugeridas.most_common(2)]
    
    candidatos = []
    # Usar a frequência total para ordenar os candidatos com as terminações comuns
    frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
    
    for num, _ in frequencia_ordenada:
        if (num % 10) in terminacoes_comuns:
            candidatos.append(num)
            if len(candidatos) >= n:
                break
    
    # Fallback se não houver candidatos suficientes.
    if len(candidatos) < n:
        sugeridos = [num for num, _ in frequencia_ordenada[:n]]
    else:
        sugeridos = candidatos
    
    return sorted(list(set(sugeridos)))
