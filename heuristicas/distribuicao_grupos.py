# heuristicas/distribuicao_grupos.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "distribuicao_grupos"
DESCRICAO = "Sugere números seguindo a distribuição mais comum por grupos de dezenas."
# Declara explicitamente as estatísticas necessárias.
DEPENDENCIAS = ["distribuicao_dezenas", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na distribuição mais frequente por grupos (dezenas).
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa diretamente as estatísticas.
    padrao_ideal = estatisticas.get('distribuicao_dezenas', (0, 0, 0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return []

    # O ideal aqui é ter uma lista de números para cada grupo, ordenada por frequência.
    grupos_por_frequencia = {
        'grupo_1_10': sorted([num for num in range(1, 11)], key=lambda x: frequencia.get(x, 0), reverse=True),
        'grupo_11_20': sorted([num for num in range(11, 21)], key=lambda x: frequencia.get(x, 0), reverse=True),
        'grupo_21_30': sorted([num for num in range(21, 31)], key=lambda x: frequencia.get(x, 0), reverse=True),
        'grupo_31_40': sorted([num for num in range(31, 41)], key=lambda x: frequencia.get(x, 0), reverse=True),
        'grupo_41_49': sorted([num for num in range(41, 50)], key=lambda x: frequencia.get(x, 0), reverse=True)
    }

    sugeridos = []
    
    # Itera sobre o padrão ideal para preencher a lista de sugeridos.
    for i in range(len(padrao_ideal)):
        num_a_pegar = padrao_ideal[i]
        
        # Encontra o grupo correspondente ao índice.
        grupo_chave = list(grupos_por_frequencia.keys())[i]
        grupo_lista = grupos_por_frequencia[grupo_chave]

        # Adiciona o número necessário de cada grupo.
        for _ in range(num_a_pegar):
            if grupo_lista:
                num = grupo_lista.pop(0)
                if num not in sugeridos:
                    sugeridos.append(num)
    
    # Completa a lista se não houver 5 números.
    if len(sugeridos) < n:
        todos_mais_frequentes = [num for num, _ in Counter(frequencia).most_common(len(frequencia))]
        for num in todos_mais_frequentes:
            if num not in sugeridos:
                sugeridos.append(num)
            if len(sugeridos) >= n:
                break
    
    return sorted(sugeridos)
