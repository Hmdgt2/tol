# heuristicas/gap_medio.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
NOME = "gap_medio"
DESCRICAO = "Sugere números com menor intervalo médio entre saídas."
# A heurística declara explicitamente que precisa da estatística 'gaps_medios'.
DEPENDENCIAS = ["gaps_medios"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base no seu gap médio (intervalo médio entre saídas),
    sugerindo os números com o gap mais curto.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa a estatística 'gaps_medios' do dicionário de entrada.
    gaps_medios = estatisticas.get('gaps_medios', {})

    if not gaps_medios:
        return []

    # Ordena os números pelo seu gap médio, do menor para o maior
    # Filtra os números que têm gap médio (gap != -1).
    melhores = sorted(
        [item for item in gaps_medios.items() if item[1] != -1],
        key=lambda x: x[1]
    )

    sugeridos = [num for num, _ in melhores[:n]]
    
    return sorted(sugeridos)
