# heuristicas/distribuicao_uniforme_faixas.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "distribuicao_uniforme_faixas"
DESCRICAO = "Sugere números distribuídos de forma equilibrada entre as faixas do jogo, evitando concentrações."
# Esta heurística precisa da estatística de frequência total.
DEPENDENCIAS = ["frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números garantindo distribuição uniforme entre as faixas do jogo.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    frequencia_total = estatisticas.get('frequencia_total', {})

    if not frequencia_total:
        return []

    # Definindo faixas
    faixas = [(1,10), (11,20), (21,30), (31,40), (41,49)]
    numeros_sugeridos = []

    for inicio, fim in faixas:
        candidatos = [num for num in range(inicio, fim+1) if num in frequencia_total]
        if candidatos:
            # Escolhe o número mais frequente na faixa
            mais_frequente = max(candidatos, key=lambda x: frequencia_total[x])
            numeros_sugeridos.append(mais_frequente)
        if len(numeros_sugeridos) >= n:
            break

    # Se ainda faltar completar n números, adiciona os mais frequentes gerais
    if len(numeros_sugeridos) < n:
        restantes = [num for num, _ in Counter(frequencia_total).most_common(n)]
        for num in restantes:
            if num not in numeros_sugeridos and len(numeros_sugeridos) < n:
                numeros_sugeridos.append(num)

    return sorted(numeros_sugeridos)
