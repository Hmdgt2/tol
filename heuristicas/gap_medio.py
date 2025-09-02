# heuristicas/gap_medio.py
from typing import Dict, Any, List

class GapMedio:
    # --- Metadados da Heurística ---
    NOME = "gap_medio"
    DESCRICAO = "Sugere números com menor intervalo médio entre saídas."
    DEPENDENCIAS = ["gaps_medios"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base no seu gap médio (intervalo médio entre saídas),
        sugerindo os números com o gap mais curto.
        """
        gaps_medios = estatisticas.get('gaps_medios', {})

        if not gaps_medios:
            return []

        melhores = sorted(
            [item for item in gaps_medios.items() if item[1] != -1],
            key=lambda x: x[1]
        )

        sugeridos = [num for num, _ in melhores[:n]]
        
        return sorted(sugeridos)
