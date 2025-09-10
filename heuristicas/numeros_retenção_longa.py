# heuristicas/numeros_retencao_longa.py
from typing import Dict, Any, List

class NumerosRetencaoLonga:
    NOME = "numeros_retencao_longa"
    DESCRICAO = "Prioriza números que estão a demorar mais para sair do que o seu padrão histórico."
    DEPENDENCIAS = ["ausencia_atual", "gaps_medios"] # Adicionámos a nova dependência

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        ausencia_atual = estatisticas.get('ausencia_atual', {})
        gaps_medios = estatisticas.get('gaps_medios', {})

        if not ausencia_atual or not gaps_medios:
            return []

        # Diferença absoluta entre ausência atual e gap médio
        candidatos = []
        for num in ausencia_atual:
            if num in gaps_medios and gaps_medios[num] > 0:
                diferenca = ausencia_atual[num] - gaps_medios[num]
                if diferenca > 0:  # Apenas se está realmente atrasado
                    candidatos.append((num, diferenca))
    
        # Ordenar pela diferença e retornar até n
        candidatos.sort(key=lambda x: x[1], reverse=True)
        return [num for num, _ in candidatos[:n]]  # Pode retornar menos que n!
