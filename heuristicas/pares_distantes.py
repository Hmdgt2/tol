# heuristicas/pares_distantes.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "pares_distantes"
DESCRICAO = "Prioriza números que raramente saem juntos, aumentando a diversidade do jogo."
# Esta heurística precisa da estatística de frequência de pares.
DEPENDENCIAS = ["pares_frequentes"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base em pares de números que raramente saíram juntos,
    buscando maximizar a cobertura de combinações incomuns.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    pares_frequentes = estatisticas.get('pares_frequentes', {})
    
    if not pares_frequentes:
        return []

    # Identifica os pares menos frequentes. O sorted() por padrão ordena da forma correta para este propósito.
    pares_menos_frequentes = sorted(pares_frequentes.items(), key=lambda x: x[1])
    
    # Cria um contador de números a partir dos pares menos frequentes.
    contador_numeros = Counter()
    for par, _ in pares_menos_frequentes:
        # A lógica é pegar os 20 pares menos frequentes.
        # Poderíamos otimizar e apenas pegar os pares necessários para 'n' números.
        if len(contador_numeros) < n:
            contador_numeros.update(par)
        else:
            break

    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return sorted(sugeridos)
