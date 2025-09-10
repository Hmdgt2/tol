# heuristicas/gap_medio.py
from typing import Dict, Any, List

class GapMedio:
    NOME = "gap_medio"
    DESCRICAO = "Sugere números que historicamente têm os maiores intervalos médios entre saídas."
    DEPENDENCIAS = ["gaps_medios"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base no seu gap médio histórico.
        """
        gaps_medios = estatisticas.get('gaps_medios', {})

        if not gaps_medios:
            return []

        # Remove os números que nunca saíram, pois têm um gap infinito
        gaps_validos = {num: gap for num, gap in gaps_medios.items() if gap != float('inf')}

        # Ordena os números pelo seu gap médio (do maior para o menor)
        sugeridos_brutos = sorted(
            gaps_validos.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Seleciona os 'n' primeiros números
        sugeridos = [num for num, _ in sugeridos_brutos[:n]]

        return sorted(sugeridos)
