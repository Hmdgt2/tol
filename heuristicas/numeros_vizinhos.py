# heuristicas/numeros_vizinhos.py
from typing import Dict, Any, List

class NumerosVizinhos:
    # --- Metadados da Heurística ---
    NOME = "numeros_vizinhos"
    DESCRICAO = "Sugere números vizinhos de sorteios recentes mais frequentes."
    DEPENDENCIAS = ["frequencia_vizinhos", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência de vizinhos sorteados.
        """
        frequencia_vizinhos = estatisticas.get('frequencia_vizinhos', {})
        
        sugeridos = []

        if frequencia_vizinhos:
            vizinhos_ordenados = sorted(frequencia_vizinhos.items(), key=lambda x: x[1], reverse=True)
            sugeridos = [num for num, _ in vizinhos_ordenados[:n]]
        
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            numeros_quentes = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
            for num in numeros_quentes:
                if num not in sugeridos:
                    sugeridos.append(num)
                if len(sugeridos) >= n:
                    break
                    
        return sorted(sugeridos)
