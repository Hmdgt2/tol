# heuristicas/distribuicao_quadrantes.py
from typing import Dict, Any, List
from collections import Counter

class DistribuicaoQuadrantes:
    NOME = "distribuicao_quadrantes"
    DESCRICAO = "Sugere números de acordo com a distribuição mais comum por quadrantes."
    DEPENDENCIAS = ["distribuicao_quadrantes", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na distribuição mais frequente por quadrantes.
        """
        frequencia = estatisticas.get('frequencia_total', {})
        distribuicao = estatisticas.get('distribuicao_quadrantes', {})

        if not frequencia or not distribuicao:
            return []

        # 1. Encontrar o quadrante mais frequente
        quadrante_mais_frequente = max(distribuicao, key=distribuicao.get)

        # 2. Definir as faixas de números para cada quadrante
        tamanho_quadrante = 49 // 4
        faixas_quadrantes = {
            1: range(1, tamanho_quadrante + 1),
            2: range(tamanho_quadrante + 1, (tamanho_quadrante * 2) + 1),
            3: range((tamanho_quadrante * 2) + 1, (tamanho_quadrante * 3) + 1),
            4: range((tamanho_quadrante * 3) + 1, 50)
        }

        # 3. Filtrar os números do quadrante mais frequente
        numeros_do_quadrante = [
            num for num in faixas_quadrantes[quadrante_mais_frequente]
            if num in frequencia
        ]

        # 4. Ordenar por frequência e pegar os top 'n'
        sugeridos = sorted(
            numeros_do_quadrante,
            key=lambda num: frequencia.get(num, 0),
            reverse=True
        )[:n]

        return sorted(sugeridos)
