# heuristicas/ausencia_superior_media.py

from typing import Dict, Any, List

class AusenciaSuperiorMedia:  # Nome da classe capitalizado, sem sublinhados
    # --- Metadados da Heurística ---
    NOME = "ausencia_superior_media"
    DESCRICAO = "Sugere números ausentes há mais tempo que a média."
    DEPENDENCIAS = ["ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        ausencia = estatisticas.get('ausencia_atual', {})
        if not ausencia:
            return []
    
        # Calcular média e desvio padrão
        ausencias = list(ausencia.values())
        media = sum(ausencias) / len(ausencias)
        desvio_padrao = (sum((x - media) ** 2 for x in ausencias) / len(ausencias)) ** 0.5
    
        # Critério rigoroso: ausência > média + 1 desvio
        limite = media + desvio_padrao
        candidatos = [num for num, dias in ausencia.items() if dias > limite]
    
        # Ordenar pelos mais ausentes e retornar até n
        candidatos.sort(key=lambda x: ausencia[x], reverse=True)
        return candidatos[:n]  # Pode retornar menos que n!
