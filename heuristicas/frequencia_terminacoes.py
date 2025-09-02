# heuristicas/frequencia_terminacoes.py
from typing import Dict, Any, List
from collections import Counter

class FrequenciaTerminacoes:
    # --- Metadados da Heurística ---
    NOME = "frequencia_terminacoes"
    DESCRICAO = "Sugere números com terminações mais frequentes."
    DEPENDENCIAS = ["frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na frequência das terminações (último dígito).
        """
        frequencia_total = estatisticas.get('frequencia_total', {})

        if not frequencia_total:
            return []
        
        contador_terminacoes = Counter()
        for num, freq in frequencia_total.items():
            terminacao = num % 10
            contador_terminacoes[terminacao] += freq

        terminacoes_mais_frequentes = [t for t, _ in contador_terminacoes.most_common(3)]
        
        candidatos = []
        frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
        
        for num, _ in frequencia_ordenada:
            if (num % 10) in terminacoes_mais_frequentes:
                candidatos.append(num)
                if len(candidatos) >= n:
                    break

        sugeridos = candidatos[:n]
        
        return sorted(list(set(sugeridos)))
