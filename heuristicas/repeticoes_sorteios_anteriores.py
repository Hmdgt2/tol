# heuristicas/repeticoes_sorteios_anteriores.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "repeticoes_sorteios_anteriores"
DESCRICAO = "Sugere números com base na probabilidade de repetição de números de sorteios anteriores."
DEPENDENCIAS = ["probabilidades_repeticoes", "frequencia_recente", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na probabilidade de repetição de números de sorteios anteriores.

    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    probabilidades_repeticoes = estatisticas.get('probabilidades_repeticoes', {})
    frequencia_recente = estatisticas.get('frequencia_recente', {})
    frequencia_geral = estatisticas.get('frequencia_total', {})

    if not probabilidades_repeticoes or not frequencia_recente or not frequencia_geral:
        return []
    
    # Identifica o número de repetições mais provável
    num_repeticoes_mais_provavel = max(probabilidades_repeticoes, key=probabilidades_repeticoes.get, default=0)

    sugeridos = []
    
    if num_repeticoes_mais_provavel > 0:
        # Se é provável que haja repetições, sugere os números mais frequentes dos sorteios recentes
        sugeridos.extend([num for num, _ in Counter(frequencia_recente).most_common(n)])
    else:
        # Se é provável que NÃO haja repetições, sugere os números que não saíram recentemente
        numeros_recentes_set = set(frequencia_recente.keys())
        numeros_nao_recentes = [num for num in frequencia_geral.keys() if num not in numeros_recentes_set]
        
        # Ordena os não recentes pela frequência geral
        numeros_nao_recentes.sort(key=lambda x: frequencia_geral.get(x, 0), reverse=True)
        sugeridos.extend(numeros_nao_recentes[:n])
    
    # Fallback para garantir que sempre retorna n números
    if len(sugeridos) < n:
        todos_frequentes_geral = [num for num, _ in Counter(frequencia_geral).most_common()]
        for num in todos_frequentes_geral:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)
    
    return sorted(list(set(sugeridos)))
