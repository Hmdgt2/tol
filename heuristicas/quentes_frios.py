# heuristicas/quentes_frios.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "quentes_frios"
DESCRICAO = "Sugere números quentes recentes e números frios ausentes."
# Esta heurística precisa da frequência recente (quentes) e da ausência atual (frios).
# A 'frequencia_recente' será um novo tipo de estatística calculada pelo 'dados.py'.
DEPENDENCIAS = ["frequencia_recente", "ausencia_atual", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base nos números "quentes" (mais frequentes recentemente)
    e "frios" (mais ausentes).
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa as estatísticas pré-calculadas
    frequencia_recente = estatisticas.get('frequencia_recente', {})
    ausencia = estatisticas.get('ausencia_atual', {})
    
    if not frequencia_recente or not ausencia:
        return []

    # Seleciona os números quentes
    numeros_quentes = [num for num, _ in Counter(frequencia_recente).most_common(n)]
    
    # Seleciona os números frios
    numeros_frios = sorted(ausencia, key=ausencia.get, reverse=True)[:n]

    # Combina os dois, garantindo que não haja duplicados
    sugeridos = list(set(numeros_quentes + numeros_frios))
    
    # Garante que a lista tenha pelo menos n números, se possível
    if len(sugeridos) < n:
        frequencia_geral = estatisticas.get('frequencia_total', {})
        todos_frequentes = [num for num, _ in Counter(frequencia_geral).most_common()]
        for num in todos_frequentes:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)
    
    return sorted(sugeridos)
