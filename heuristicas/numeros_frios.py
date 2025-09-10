#heuristicas/numeros_frios.py

from typing import Dict, Any, List
from collections import Counter

class NumerosFrios:
    NOME = "numeros_frios"
    DESCRICAO = "Sugere os números que estão ausentes há mais tempo."
    DEPENDENCIAS = ["ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        ausencia = estatisticas.get('ausencia_atual', {})
        
        if not ausencia:
            return []

        # Ordena os números pela ausência (tempo de atraso) e pega os 'n' primeiros
        sugeridos = sorted(ausencia, key=ausencia.get, reverse=True)[:n]
        
        return sorted(sugeridos)
