# heuristicas/frequencia_soma.py

from typing import Dict, Any, List
from collections import Counter

class FrequenciaSoma:
    NOME = "frequencia_soma"
    DESCRICAO = "Sugere os números que mais contribuem para as somas mais comuns."
    DEPENDENCIAS = ["soma_numero_individual", "soma_frequencia"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        soma_frequencia = estatisticas.get('soma_frequencia', {})
        soma_numero_individual = estatisticas.get('soma_numero_individual', {})

        if not soma_frequencia or not soma_numero_individual:
            return []

        # Encontra a soma mais frequente
        soma_mais_frequente = Counter(soma_frequencia).most_common(1)[0][0]
        
        # Filtra os números que têm uma frequência alta na soma mais comum
        candidatos = {
            num: freq for num, freq in soma_numero_individual.items()
            if freq.get(str(soma_mais_frequente), 0) > 0
        }
        
        if not candidatos:
            # Fallback seguro para evitar erro, usando os mais frequentes
            frequencia_total = estatisticas.get('frequencia_total', {})
            return sorted(Counter(frequencia_total).most_common(n))[:n]

        # Ordena os candidatos pela sua frequência na soma mais comum
        melhores_candidatos = sorted(
            candidatos.items(),
            key=lambda item: item[1].get(str(soma_mais_frequente), 0),
            reverse=True
        )

        sugeridos = [num for num, freq in melhores_candidatos[:n]]

        return sorted(sugeridos)
