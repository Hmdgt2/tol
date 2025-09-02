# heuristicas/clusters_recentes.py
from typing import Dict, Any, List
from collections import Counter

class ClustersRecentes:
    NOME = "clusters_recentes"
    DESCRICAO = "Prioriza grupos de números que saíram juntos recentemente, capturando pequenos clusters ou padrões."
    DEPENDENCIAS = ["pares_recentes"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base em clusters recentes, usando os pares mais frequentes.
        """
        pares_recentes = estatisticas.get('pares_recentes', {})
        
        if not pares_recentes:
            return []

        pares_mais_frequentes = [par for par, _ in pares_recentes.most_common(10)]
        
        contador_numeros = Counter()
        for par in pares_mais_frequentes:
            contador_numeros.update(par)
            
        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(list(set(sugeridos)))
