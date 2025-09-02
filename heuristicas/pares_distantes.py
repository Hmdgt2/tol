# heuristicas/pares_distantes.py
from typing import Dict, Any, List
from collections import Counter

class ParesDistantes:
    # --- Metadados da Heurística ---
    NOME = "pares_distantes"
    DESCRICAO = "Prioriza números que raramente saem juntos, aumentando a diversidade do jogo."
    DEPENDENCIAS = ["frequencia_pares"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base em pares de números que raramente saíram juntos,
        buscando maximizar a cobertura de combinações incomuns.
        """
        frequencia_pares = estatisticas.get('frequencia_pares', {})
        
        if not frequencia_pares:
            return []

        pares_menos_frequentes = sorted(frequencia_pares.items(), key=lambda x: x[1])
        
        contador_numeros = Counter()
        for par, _ in pares_menos_frequentes:
            if len(contador_numeros) < n:
                # O par de números é uma tupla, ex: (1, 5)
                contador_numeros.update(par)
            else:
                break

        sugeridos = [num for num, _ in contador_numeros.most_common(n)]
        
        return sorted(sugeridos)
