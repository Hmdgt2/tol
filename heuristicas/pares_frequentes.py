# heuristicas/pares_frequentes.py
from typing import Dict, Any, List
from collections import Counter

class ParesFrequentes:
    NOME = "pares_frequentes"
    DESCRICAO = "Sugere números presentes nos pares mais frequentes."
    DEPENDENCIAS = ["frequencia_pares"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de pares de números.
        """
        pares_frequentes = estatisticas.get('frequencia_pares', {})
        
        if not pares_frequentes:
            return []
        
        pares_mais_frequentes = Counter(pares_frequentes).most_common(10)
        
        contador_numeros = Counter()
        for par, _ in pares_mais_frequentes:
            contador_numeros.update(par)
            
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(sugeridos)
