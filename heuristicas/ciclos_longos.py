# heuristicas/ciclos_longos.py
from typing import Dict, Any, List

class CiclosLongos:
    # --- Metadados da Heurística ---
    NOME = "ciclos_longos"
    DESCRICAO = "Sugere números que estão atrasados em relação ao seu ciclo histórico, com base no intervalo médio entre aparições."
    DEPENDENCIAS = ["gaps_medios", "ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        gaps_medios = estatisticas.get('gaps_medios', {})
        ausencia = estatisticas.get('ausencia_atual', {})

        if not gaps_medios or not ausencia:
            return []

        # Apenas números com ausência > 1.5x gap médio
        candidatos = []
        for num in ausencia:
            if num in gaps_medios and gaps_medios[num] > 0:
                if ausencia[num] > 1.5 * gaps_medios[num]:
                    candidatos.append((num, ausencia[num] / gaps_medios[num]))
    
        # Ordenar pelo ratio e retornar até n
        candidatos.sort(key=lambda x: x[1], reverse=True)
        return [num for num, _ in candidatos[:n]]  # Pode retornar menos que n!
