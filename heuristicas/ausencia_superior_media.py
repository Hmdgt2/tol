# heuristicas/ausencia_superior_media.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
# A nova arquitetura usa um padrão de metadados para saber o que a heurística faz e o que precisa.
class Ausencia_superior_media:
    NOME = "ausencia_superior_media"
    DESCRICAO = "Sugere números ausentes há mais tempo que a média."
    DEPENDENCIAS = ["ausencia_atual"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base na ausência, favorecendo aqueles ausentes por mais tempo que a média.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa diretamente a estatística 'ausencia_atual' do dicionário de entrada.
    # O sistema já garante que esta chave existe porque foi declarada nas DEPENDENCIAS.
    ausencia = estatisticas.get('ausencia_atual', {})

    if not ausencia:
        return []

    # O código a seguir é a sua lógica original, que é perfeita para o propósito.
    
    # Calcula a média de ausência
    numeros_presentes = [d for d in ausencia.values() if d != -1 and d != float('inf')]
    if not numeros_presentes:
        media = 0
    else:
        media = sum(numeros_presentes) / len(numeros_presentes)

    # Filtra os números com ausência superior à média
    candidatos = [num for num, dias in ausencia.items() if dias > media]

    # Ordena os candidatos do maior para o menor e pega os n primeiros
    sugeridos = sorted(candidatos, key=lambda x: ausencia[x], reverse=True)[:n]

    return sugeridos
