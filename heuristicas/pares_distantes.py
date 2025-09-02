# heuristicas/pares_distantes.py
from typing import Dict, Any, List
from collections import Counter

class ParesDistantes:
    NOME = "pares_distantes"
    DESCRICAO = "Prioriza números que raramente saem juntos, aumentando a diversidade do jogo."
    DEPENDENCIAS = ["pares_frequentes"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base em pares de números que raramente saíram juntos,
        buscando maximizar a cobertura de combinações incomuns.
        """
        pares_frequentes = estatisticas.get('pares_frequentes', {})
        
        if not pares_frequentes:
            return []

        pares_menos_frequentes = sorted(pares_frequentes.items(), key=lambda x: x[1])
        
        contador_numeros = Counter()
        for par, _ in pares_menos_frequentes:
            if len(contador_numeros) < n:
                contador_numeros.update(par)
            else:
                break

        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(sugeridos)
