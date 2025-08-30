from typing import Dict, Any, List

# --- Metadados da Heurística ---
# A nova arquitetura usa um padrão de metadados para saber o que a heurística precisa.
NOME = "ciclos_longos"
DESCRICAO = "Sugere números que estão atrasados em relação ao seu ciclo histórico, com base no intervalo médio entre aparições."
# Declara explicitamente as estatísticas necessárias do dados.py.
DEPENDENCIAS = ["gaps_medios", "ausencia_atual"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base nos ciclos longos, calculando o score de atraso.

    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.

    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa as estatísticas pré-calculadas pelo dados.py.
    # O "gaps_medios" e a "ausencia_atual" já são calculados de forma otimizada.
    gaps_medios = estatisticas.get('gaps_medios', {})
    ausencia = estatisticas.get('ausencia_atual', {})

    if not gaps_medios or not ausencia:
        return []

    # Combina as estatísticas para calcular o score de atraso.
    # O código agora é mais simples e focado, pois não precisa fazer os cálculos do zero.
    score = {
        num: ausencia[num] / gaps_medios.get(num, 1)
        for num in ausencia if num in gaps_medios and gaps_medios[num] > 0
    }

    # Ordena os números pelo score de atraso e pega os n mais altos.
    sugeridos = sorted(score, key=score.get, reverse=True)[:n]

    return sorted(sugeridos)
