# heuristicas/gap_medio.py
from typing import Dict, Any, List

class GapMedio:
    # --- Metadados da Heurística ---
    NOME = "gap_medio"
    DESCRICAO = "Sugere números 'em atraso' com base na sua ausência atual comparada ao seu intervalo médio de saídas."
    DEPENDENCIAS = ["gaps_medios", "ausencia_atual"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números que estão 'em atraso' em relação ao seu gap médio.
        """
        gaps_medios = estatisticas.get('gaps_medios', {})
        ausencia_atual = estatisticas.get('ausencia_atual', {})

        if not gaps_medios or not ausencia_atual:
            return []

        # Calcula a 'tendência de atraso' de cada número
        tendencia_atraso = {}
        for num, gap in gaps_medios.items():
            if gap > 0:
                atraso = ausencia_atual.get(num, 0)
                # A tendência é o quão atrasado o número está em relação ao seu ritmo
                tendencia_atraso[num] = atraso - gap

        # Sugere os números com a maior 'tendência de atraso' (os mais negativos)
        melhores = sorted(
            tendencia_atraso.items(),
            key=lambda x: x[1],
            reverse=True  # Pega os maiores valores (maior atraso)
        )
        
        # O teu código pode estar a ter um problema com o float('inf'), este método contorna.
        # Filtra os que não têm um gap médio válido.
        sugeridos_brutos = [num for num, _ in melhores]
        
        sugeridos = []
        for num in sugeridos_brutos:
            if len(sugeridos) >= n:
                break
            # Certifica-se de que a previsão tem números únicos.
            if num not in sugeridos:
                sugeridos.append(num)

        # Se não houver números suficientes, preenche com os mais frequentes
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            frequencia_ordenada = sorted(frequencia_total.keys(), key=lambda x: frequencia_total[x], reverse=True)
            for num in frequencia_ordenada:
                if len(sugeridos) >= n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)
        
        return sorted(sugeridos)
