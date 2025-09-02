# heuristicas/quentes_frios.py
from typing import Dict, Any, List
from collections import Counter

class QuentesFrios:
    # --- Metadados da Heurística ---
    NOME = "quentes_frios"
    DESCRICAO = "Sugere números quentes recentes e números frios ausentes."
    DEPENDENCIAS = ["frequencia_recente", "ausencia_atual", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nos números "quentes" (mais frequentes recentemente)
        e "frios" (mais ausentes).
        """
        frequencia_recente = estatisticas.get('frequencia_recente', {})
        ausencia = estatisticas.get('ausencia_atual', {})
        
        if not frequencia_recente or not ausencia:
            return []

        numeros_quentes = [num for num, _ in Counter(frequencia_recente).most_common(n)]
        
        numeros_frios = sorted(ausencia, key=ausencia.get, reverse=True)[:n]

        sugeridos = list(set(numeros_quentes + numeros_frios))
        
        if len(sugeridos) < n:
            frequencia_geral = estatisticas.get('frequencia_total', {})
            todos_frequentes = [num for num, _ in Counter(frequencia_geral).most_common()]
            for num in todos_frequentes:
                if num not in sugeridos and len(sugeridos) < n:
                    sugeridos.append(num)
        
        return sorted(sugeridos)
