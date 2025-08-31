# heuristicas/numeros_vizinhos.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "numeros_vizinhos"
DESCRICAO = "Sugere números vizinhos de sorteios recentes mais frequentes."
# Esta heurística precisa de uma nova estatística pré-calculada.
DEPENDENCIAS = ["frequencia_vizinhos", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na frequência de vizinhos sorteados.

    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'frequencia_vizinhos' pré-calculada.
    frequencia_vizinhos = estatisticas.get('frequencia_vizinhos', {})
    
    sugeridos = []

    if frequencia_vizinhos:
        # Sugere os números vizinhos mais frequentes
        vizinhos_ordenados = sorted(frequencia_vizinhos.items(), key=lambda x: x[1], reverse=True)
        sugeridos = [num for num, _ in vizinhos_ordenados[:n]]
    
    # Se ainda não tivermos 'n' números (por exemplo, se a estatística estiver vazia),
    # usamos um fallback para os números mais frequentes no geral.
    if len(sugeridos) < n:
        frequencia_total = estatisticas.get('frequencia_total', {})
        numeros_quentes = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
        for num in numeros_quentes:
            if num not in sugeridos:
                sugeridos.append(num)
            if len(sugeridos) >= n:
                break
                
    return sorted(sugeridos)
