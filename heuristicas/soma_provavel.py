# heuristicas/soma_provavel.py
from typing import Dict, Any, List

class SomaProvavel:
    # --- Metadados da Heurística ---
    NOME = "soma_provavel"
    DESCRICAO = "Sugere números cuja soma tende à soma mais frequente nos sorteios."
    DEPENDENCIAS = ["numeros_soma_mais_frequente", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na soma mais provável dos sorteios.
        """
        sugeridos_da_soma = estatisticas.get('numeros_soma_mais_frequente', [])
        
        if not sugeridos_da_soma:
            frequencia = estatisticas.get('frequencia_total', {})
            if frequencia:
                return sorted([num for num in frequencia.keys()][:n])
            return []

        sugeridos = sugeridos_da_soma[:n]
        
        if len(sugeridos) < n:
            frequencia = estatisticas.get('frequencia_total', {})
            numeros_gerais = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
            
            for num in numeros_gerais:
                if num not in sugeridos and len(sugeridos) < n:
                    sugeridos.append(num)

        return sorted(sugeridos)
