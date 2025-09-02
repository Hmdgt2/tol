# heuristicas/trios_frequentes.py
from typing import Dict, Any, List
from collections import Counter

class TriosFrequentes:
    # --- Metadados da Heurística ---
    NOME = "trios_frequentes"
    DESCRICAO = "Sugere números que aparecem juntos em trios frequentes nos sorteios passados."
    DEPENDENCIAS = ["trios_frequentes"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de trios de números.
        """
        trios_frequentes = estatisticas.get('trios_frequentes', {})
        
        if not trios_frequentes:
            return []
        
        trios_mais_frequentes = Counter(trios_frequentes).most_common(10)
        
        contador_numeros = Counter()
        for trio, _ in trios_mais_frequentes:
            contador_numeros.update(trio)
            
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(sugeridos)
