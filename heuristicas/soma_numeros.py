# heuristicas/soma_numeros.py
from typing import Dict, Any, List

class SomaNumeros:
    # --- Metadados da Heurística ---
    NOME = "soma_numeros"
    DESCRICAO = "Sugere números dos sorteios cuja soma total é mais frequente."
    DEPENDENCIAS = ["numeros_soma_mais_frequente", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na soma mais provável dos sorteios.
        """
        numeros_soma = estatisticas.get('numeros_soma_mais_frequente', [])
        
        if not numeros_soma:
            frequencia_total = estatisticas.get('frequencia_total', {})
            if frequencia_total:
                sugeridos = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)[:n]
                return sugeridos
            return []

        sugeridos = numeros_soma[:n]
        
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            numeros_gerais = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
            
            for num in numeros_gerais:
                if num not in sugeridos and len(sugeridos) < n:
                    sugeridos.append(num)

        return sorted(sugeridos)
