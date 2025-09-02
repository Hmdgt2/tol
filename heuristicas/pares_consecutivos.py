# heuristicas/pares_consecutivos.py
from typing import Dict, Any, List
from collections import Counter

class ParesConsecutivos:
    NOME = "pares_consecutivos"
    DESCRICAO = "Sugere números que formam pares consecutivos frequentes."
    DEPENDENCIAS = ["frequencia_pares_consecutivos"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de pares de números consecutivos.
        """
        pares_consecutivos = estatisticas.get('frequencia_pares_consecutivos', {})
        
        if not pares_consecutivos:
            return []

        contador_numeros = Counter()
        pares_mais_frequentes = pares_consecutivos.most_common(5)

        for par, _ in pares_mais_frequentes:
            contador_numeros.update(par)
        
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(sugeridos)
