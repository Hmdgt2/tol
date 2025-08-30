# heuristicas/comb_balanceadas.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "comb_balanceadas"
DESCRICAO = "Sugere combinações que equilibram números pares e ímpares, altos e baixos, com base em padrões históricos."
# Esta heurística precisa da estatística de frequência total.
DEPENDENCIAS = ["frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base em combinações balanceadas de paridade e posição.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa diretamente a estatística de frequência total.
    frequencia_total = estatisticas.get('frequencia_total', {})
    
    if not frequencia_total:
        return []

    # Divide números em pares/ímpares
    pares = sorted([num for num in frequencia_total if num % 2 == 0], key=lambda x: frequencia_total[x], reverse=True)
    impares = sorted([num for num in frequencia_total if num % 2 != 0], key=lambda x: frequencia_total[x], reverse=True)

    # Divide números em altos/baixos (1-24 baixos, 25-49 altos)
    baixos = sorted([num for num in frequencia_total if num <= 24], key=lambda x: frequencia_total[x], reverse=True)
    altos = sorted([num for num in frequencia_total if num >= 25], key=lambda x: frequencia_total[x], reverse=True)
    
    # Seleciona os mais frequentes de cada categoria de forma equilibrada.
    sugeridos = []
    grupos = [pares, impares, baixos, altos]
    
    # A lógica aqui foi simplificada para pegar um número de cada grupo por vez,
    # garantindo uma combinação mais balanceada desde o início.
    num_por_grupo = n // len(grupos)
    
    # Preenche a lista com base na frequência e no balanceamento.
    for grupo in grupos:
        for _ in range(num_por_grupo):
            if grupo:
                sugeridos.append(grupo.pop(0))

    # Se ainda faltarem números para atingir 'n', completa com os mais frequentes no geral.
    frequencia_ordenada = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
    for num in frequencia_ordenada:
        if len(sugeridos) >= n:
            break
        if num not in sugeridos:
            sugeridos.append(num)

    return sorted(sugeridos)
