# heuristicas/soma_numeros.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "soma_numeros"
DESCRICAO = "Sugere números dos sorteios cuja soma total é mais frequente."
# Esta heurística precisa da estatística de números que mais saem nos sorteios com soma frequente.
DEPENDENCIAS = ["numeros_soma_mais_frequente", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na soma mais provável dos sorteios.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'numeros_soma_mais_frequente' pré-calculada.
    numeros_soma = estatisticas.get('numeros_soma_mais_frequente', [])
    
    if not numeros_soma:
        # Fallback para os números mais frequentes no geral se a estatística estiver vazia.
        frequencia_total = estatisticas.get('frequencia_total', {})
        if frequencia_total:
            sugeridos = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)[:n]
            return sugeridos
        return []

    sugeridos = numeros_soma[:n]
    
    # Se faltar números, completa com os mais frequentes no geral
    if len(sugeridos) < n:
        frequencia_total = estatisticas.get('frequencia_total', {})
        numeros_gerais = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
        
        for num in numeros_gerais:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return sorted(sugeridos)
