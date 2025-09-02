# heuristicas/tendencia_recentes.py
from typing import Dict, Any, List
from collections import Counter

class TendenciaRecentes:
    # --- Metadados da Heurística ---
    NOME = "tendencia_recentes"
    DESCRICAO = "Sugere os números mais frequentes nos últimos sorteios."
    DEPENDENCIAS = ["frequencia_recente"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na sua frequência nos sorteios mais recentes.
        """
        frequencia_recente = estatisticas.get('frequencia_recente', {})
        
        if not frequencia_recente:
            return []

        sugeridos = [num for num, _ in Counter(frequencia_recente).most_common(n)]
        
        return sorted(sugeridos)
