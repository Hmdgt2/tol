# heuristicas/clusters_recentes.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "clusters_recentes"
DESCRICAO = "Prioriza grupos de números que saíram juntos recentemente, capturando pequenos clusters ou padrões."
# Esta heurística precisa da estatística de pares recentes.
DEPENDENCIAS = ["pares_recentes"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base em clusters recentes, usando os pares mais frequentes.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa diretamente a estatística de pares recentes.
    # O dados.py agora deve ter uma função para calcular esta estatística.
    pares_recentes = estatisticas.get('pares_recentes', {})
    
    if not pares_recentes:
        return []

    # Seleciona os pares mais frequentes.
    # A sua lógica de pegar os 10 mais comuns é um bom ponto de partida.
    pares_mais_frequentes = [par for par, _ in pares_recentes.most_common(10)]
    
    # Conta a frequência individual de cada número dentro desses pares.
    contador_numeros = Counter()
    for par in pares_mais_frequentes:
        contador_numeros.update(par)
    
    # Sugere os números mais frequentes encontrados nos pares.
    sugeridos = [num for num, _ in contador_numeros.most_common(n)]
    
    return sorted(list(set(sugeridos)))
