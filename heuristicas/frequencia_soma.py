# heuristicas/frequencia_soma.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "frequencia_soma"
DESCRICAO = "Sugere números que ajudam a formar a soma mais frequente dos sorteios."
# Esta heurística precisa da soma mais comum e da frequência total.
DEPENDENCIAS = ["soma_mais_comum", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na soma mais frequente dos sorteios, usando uma abordagem otimizada.

    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    soma_ideal = estatisticas.get('soma_mais_comum', 0)
    frequencia = estatisticas.get('frequencia_total', {})

    if not frequencia or soma_ideal == 0:
        return []

    # Cria uma lista de candidatos ordenada por frequência
    candidatos = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
    
    sugeridos = []
    soma_atual = 0
    
    # Abordagem gananciosa para selecionar números que se aproximam da soma ideal.
    # Esta abordagem é muito mais eficiente do que calcular combinações.
    for num in candidatos:
        # Pega números que ajudam a alcançar a soma ideal sem a exceder drasticamente
        if (soma_atual + num) <= (soma_ideal + 10) and len(sugeridos) < n:
            sugeridos.append(num)
            soma_atual += num
            
    # Se ainda não tivermos números suficientes, preenchemos com os restantes mais frequentes.
    if len(sugeridos) < n:
        for num in candidatos:
            if len(sugeridos) >= n:
                break
            if num not in sugeridos:
                sugeridos.append(num)
                
    return sorted(sugeridos)
