from typing import Dict, Any, List
from collections import Counter

class FrequenciaSoma:
    NOME = "frequencia_soma"
    DESCRICAO = "Sugere números que ajudam a formar a soma mais frequente dos sorteios."
    DEPENDENCIAS = ["numeros_soma_mais_frequente", "frequencia_total"] # Dependência corrigida

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na soma mais frequente dos sorteios, usando uma abordagem otimizada.
        """
        # A dependência agora retorna uma lista de números.
        numeros_soma_comum = estatisticas.get('numeros_soma_mais_frequente', [])
        
        # CORREÇÃO: Calculamos a soma ideal a partir da lista de números recebida.
        soma_ideal = sum(numeros_soma_comum)

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
