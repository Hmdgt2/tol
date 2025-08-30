# heuristicas/crescimento_ano.py
from typing import Dict, Any, List
from collections import Counter

# --- Metadados da Heurística ---
NOME = "crescimento_ano"
DESCRICAO = "Sugere números cuja frequência tem aumentado de ano para ano."
# Esta heurística precisa da estatística de frequência por ano.
DEPENDENCIAS = ["frequencia_por_ano"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base no crescimento da sua frequência ao longo dos anos.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    freq_ano = estatisticas.get('frequencia_por_ano', {})
    
    if not freq_ano:
        return []

    anos = sorted(freq_ano.keys())
    pontos = Counter()
    
    # Se houver menos de 2 anos, não é possível calcular crescimento.
    if len(anos) < 2:
        return []
    
    for num in range(1, 50):
        crescimentos = 0
        for i in range(1, len(anos)):
            ano_anterior = anos[i - 1]
            ano_atual = anos[i]
            
            freq_anterior = freq_ano.get(ano_anterior, {}).get(num, 0)
            freq_atual = freq_ano.get(ano_atual, {}).get(num, 0)
            
            if freq_atual > freq_anterior:
                crescimentos += 1
                
        # Atribui pontos baseados no número de crescimentos
        if crescimentos > 0:
            pontos[num] = crescimentos * 3
            
    # Sugere os n números com mais pontos
    sugeridos = [num for num, _ in pontos.most_common(n)]

    return sorted(sugeridos)
