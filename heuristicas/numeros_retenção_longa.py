# heuristicas/numeros_retencao_longa.py
from typing import Dict, Any, List

class NumerosRetencaoLonga:
    NOME = "numeros_retencao_longa"
    DESCRICAO = "Prioriza números que estão a demorar mais para sair do que o seu padrão histórico."
    DEPENDENCIAS = ["ausencia_atual", "gaps_medios"] # Adicionámos a nova dependência

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base na sua "retenção longa", comparando a ausência atual
        com o seu gap médio histórico.
        """
        ausencia_atual = estatisticas.get('ausencia_atual', {})
        gaps_medios = estatisticas.get('gaps_medios', {})

        if not ausencia_atual or not gaps_medios:
            return []

        pontuacoes = {}
        for num in ausencia_atual:
            # Protege contra o caso de um gap médio ser 0 (não deve acontecer) ou infinito
            gap = gaps_medios.get(num, float('inf'))
            if gap > 0 and gap != float('inf'):
                pontuacao = ausencia_atual[num] / gap
                pontuacoes[num] = pontuacao

        # Ordena pela pontuação para encontrar os números com a maior "retenção"
        sugeridos_brutos = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        sugeridos = [num for num, _ in sugeridos_brutos[:n]]

        # O fallback para o caso de não haver números suficientes
        if len(sugeridos) < n:
            frequencia_total = estatisticas.get('frequencia_total', {})
            freq_ordenada = sorted(frequencia_total.items(), key=lambda x: x[1], reverse=True)
            for num, _ in freq_ordenada:
                if len(sugeridos) == n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)

        return sorted(sugeridos)
