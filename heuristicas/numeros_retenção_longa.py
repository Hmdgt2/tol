# heuristicas/numeros_retencao_longa.py
from typing import Dict, Any, List
from collections import Counter

class NumerosRetencaoLonga:
    NOME = "numeros_retencao_longa"
    DESCRICAO = "Prioriza números que não saem há muitos sorteios, com base no histórico de ausência (gaps longos)."
    DEPENDENCIAS = ["ausencia_atual", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números que estão 'atrasados', ou seja, não saem há muito tempo.
        """
        ausencia = estatisticas.get('ausencia_atual', {})
        frequencia_total = estatisticas.get('frequencia_total', {})

        if not ausencia or not frequencia_total:
            return []

        ausentes_mais_longo = sorted(ausencia.items(), key=lambda x: x[1], reverse=True)

        sugeridos = [num for num, _ in ausentes_mais_longo[:n]]

        if len(sugeridos) < n:
            freq_ordenada = sorted(frequencia_total.items(), key=lambda x: x[1], reverse=True)
            for num, _ in freq_ordenada:
                if num not in sugeridos:
                    sugeridos.append(num)
                    if len(sugeridos) == n:
                        break

        return sorted(sugeridos)
