# heuristicas/frequencia_total.py
from typing import Dict, Any, List
from collections import Counter

class FrequenciaTotal:
    # --- Metadados da Heurística ---
    NOME = "frequencia_total"
    DESCRICAO = "Sugere os números mais frequentes no histórico."
    DEPENDENCIAS = ["frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na sua frequência histórica total.
        
        Args:
            estatisticas (dict): Dicionário com as estatísticas pré-calculadas de que a heurística depende.
            n (int): O número de sugestões a retornar.
            
        Returns:
            list: Uma lista de números sugeridos.
        """
        frequencia = estatisticas.get('frequencia_total', {})
        
        if not frequencia:
            return []

        sugeridos = [num for num, _ in Counter(frequencia).most_common(n)]

        return sorted(sugeridos)
