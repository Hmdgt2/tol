# heuristicas/numeros_quentes.py

from typing import Dict, Any, List
from collections import Counter

class NumerosQuentes:
    NOME = "numeros_quentes"
    DESCRICAO = "Sugere os números mais frequentes nos sorteios recentes."
    DEPENDENCIAS = ["frequencia_recente"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        frequencia_recente = estatisticas.get('frequencia_recente', {})
        
        if not frequencia_recente:
            return []

        sugeridos = [
            num for num, _ in Counter(frequencia_recente).most_common(n)
        ]
        
        return sorted(sugeridos)
