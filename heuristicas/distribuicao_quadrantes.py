# heuristicas/distribuicao_quadrantes.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "distribuicao_quadrantes"
DESCRICAO = "Sugere números de acordo com a distribuição mais comum por quadrantes.(# Quadrantes: divisão dos números em 4 faixas iguais)"
# Declara explicitamente as estatísticas necessárias.
DEPENDENCIAS = ["distribuicao_quadrantes", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na distribuição mais frequente por quadrantes.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa diretamente as estatísticas de distribuição de quadrantes e frequência total.
    padrao_ideal = estatisticas.get('distribuicao_quadrantes', (0, 0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return []

    # O ideal é ter uma lista de números para cada quadrante, ordenada por frequência.
    tamanho_quadrante = 49 // 4
    quadrantes = {
        0: sorted([num for num in range(1, tamanho_quadrante + 1)], key=lambda x: frequencia.get(x, 0), reverse=True),
        1: sorted([num for num in range(tamanho_quadrante + 1, (tamanho_quadrante * 2) + 1)], key=lambda x: frequencia.get(x, 0), reverse=True),
        2: sorted([num for num in range((tamanho_quadrante * 2) + 1, (tamanho_quadrante * 3) + 1)], key=lambda x: frequencia.get(x, 0), reverse=True),
        3: sorted([num for num in range((tamanho_quadrante * 3) + 1, 50)], key=lambda x: frequencia.get(x, 0), reverse=True),
    }

    sugeridos = []
    
    # Preenche a lista com base no padrão ideal de quadrantes.
    for i in range(len(padrao_ideal)):
        num_a_pegar = padrao_ideal[i]
        
        grupo_lista = quadrantes[i]
        
        for _ in range(num_a_pegar):
            if grupo_lista:
                num = grupo_lista.pop(0)
                if num not in sugeridos:
                    sugeridos.append(num)
    
    # Completa a lista se não houver 'n' números.
    if len(sugeridos) < n:
        todos_mais_frequentes = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        for num in todos_mais_frequentes:
            if num not in sugeridos:
                sugeridos.append(num)
            if len(sugeridos) >= n:
                break
    
    return sorted(sugeridos)
