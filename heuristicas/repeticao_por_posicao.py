# heuristicas/repeticao_por_posicao.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "repeticao_por_posicao"
DESCRICAO = "Sugere números com base na frequência em cada posição do sorteio, aproveitando padrões posicionais."
# Esta heurística precisa da frequência de cada número por posição.
DEPENDENCIAS = ["frequencia_por_posicao"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na repetição de números em posições específicas do sorteio.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'frequencia_por_posicao' pré-calculada.
    # Esta estatística deve ser um dicionário onde a chave é a posição (0 a 4)
    # e o valor é um Counter de números para essa posição.
    frequencia_por_posicao = estatisticas.get('frequencia_por_posicao', {})
    
    if not frequencia_por_posicao:
        return []

    sugeridos = []
    # Itera sobre as posições para obter o número mais frequente em cada uma.
    for pos in sorted(frequencia_por_posicao.keys()):
        contador_pos = frequencia_por_posicao[pos]
        if contador_pos:
            num_mais_frequente = sorted(contador_pos.items(), key=lambda item: item[1], reverse=True)[0][0]
            if num_mais_frequente not in sugeridos:
                sugeridos.append(num_mais_frequente)
        if len(sugeridos) >= n:
            break
            
    # Se não houver números suficientes, completa com os mais frequentes no geral.
    if len(sugeridos) < n:
        frequencia_total = estatisticas.get('frequencia_total', {})
        numeros_gerais = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
        
        for num in numeros_gerais:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return sorted(sugeridos)
