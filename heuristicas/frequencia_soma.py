# heuristicas/frequencia_soma.py
from typing import Dict, Any, List
from collections import Counter

class FrequenciaSoma:
    NOME = "frequencia_soma"
    DESCRICAO = "Sugere números que ajudam a formar a soma mais frequente dos sorteios."
    DEPENDENCIAS = ["soma_mais_comum", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na soma mais frequente dos sorteios, usando uma abordagem otimizada.
        """
        soma_ideal = estatisticas.get('soma_mais_comum', 0)
        frequencia = estatisticas.get('frequencia_total', {})

        if not frequencia or soma_ideal == 0:
            return []

        candidatos = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        
        sugeridos = []
        soma_atual = 0
        
        for num in candidatos:
            if (soma_atual + num) <= (soma_ideal + 10) and len(sugeridos) < n:
                sugeridos.append(num)
                soma_atual += num
                
        if len(sugeridos) < n:
            for num in candidatos:
                if len(sugeridos) >= n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)
                    
        return sorted(sugeridos)
