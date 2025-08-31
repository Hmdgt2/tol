# heuristicas/soma_provavel.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "soma_provavel"
DESCRICAO = "Sugere números cuja soma tende à soma mais frequente nos sorteios."
# Esta heurística precisa de uma estatística que já contenha os números mais frequentes
# dentro das somas mais prováveis.
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
    # Acessa a estatística 'numeros_soma_mais_frequente' pré-calculada,
    # que já contém a lista de números que melhor se encaixam.
    sugeridos_da_soma = estatisticas.get('numeros_soma_mais_frequente', [])
    
    if not sugeridos_da_soma:
        # Fallback para os números mais frequentes no geral se a estatística estiver vazia.
        frequencia = estatisticas.get('frequencia_total', {})
        if frequencia:
            return sorted([num for num in frequencia.keys()][:n])
        return []

    # Se a lista da estatística já existir, simplesmente a utiliza.
    sugeridos = sugeridos_da_soma[:n]
    
    # Se faltar números, completa com os mais frequentes no geral.
    if len(sugeridos) < n:
        frequencia = estatisticas.get('frequencia_total', {})
        numeros_gerais = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        
        for num in numeros_gerais:
            if num not in sugeridos and len(sugeridos) < n:
                sugeridos.append(num)

    return sorted(sugeridos)
