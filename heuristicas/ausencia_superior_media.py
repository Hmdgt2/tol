# heuristicas/ausencia_superior_media.py

from typing import Dict, Any, List

class AusenciaSuperiorMedia:  # Nome da classe capitalizado, sem sublinhados
    # --- Metadados da Heurística ---
    NOME = "ausencia_superior_media"
    DESCRICAO = "Sugere números ausentes há mais tempo que a média."
    DEPENDENCIAS = ["ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        A lógica de previsão deve ser um método dentro da classe.
        """
        ausencia = estatisticas.get('ausencia_atual', {})
        if not ausencia:
            return []
        
        numeros_presentes = [d for d in ausencia.values() if d != -1 and d != float('inf')]
        media = sum(numeros_presentes) / len(numeros_presentes) if numeros_presentes else 0
        
        candidatos = [num for num, dias in ausencia.items() if dias > media]
        sugeridos = sorted(candidatos, key=lambda x: ausencia[x], reverse=True)[:n]
        return sugeridos
