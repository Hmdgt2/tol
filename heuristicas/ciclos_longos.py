# heuristicas/ciclos_longos.py
from typing import Dict, Any, List

class CiclosLongos:
    # --- Metadados da Heurística ---
    NOME = "ciclos_longos"
    DESCRICAO = "Sugere números que estão atrasados em relação ao seu ciclo histórico, com base no intervalo médio entre aparições."
    DEPENDENCIAS = ["gaps_medios", "ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nos ciclos longos, calculando o score de atraso.

        Args:
            estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
            n (int): O número de sugestões a retornar.

        Returns:
            list: Uma lista de números sugeridos.
        """
        gaps_medios = estatisticas.get('gaps_medios', {})
        ausencia = estatisticas.get('ausencia_atual', {})

        if not gaps_medios or not ausencia:
            return []

        score = {
            num: ausencia[num] / gaps_medios.get(num, 1)
            for num in ausencia if num in gaps_medios and gaps_medios[num] > 0
        }

        sugeridos = sorted(score, key=score.get, reverse=True)[:n]

        return sorted(sugeridos)
