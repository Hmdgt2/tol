# heuristicas/padrao_finais.py
from typing import Dict, Any, List
from collections import Counter

class PadraoFinais:
    # --- Metadados da Heurística ---
    NOME = "padrao_finais"
    DESCRICAO = "Sugere números com terminações semelhantes ao último sorteio."
    DEPENDENCIAS = ["frequencia_terminacoes_padrao", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nas terminações mais prováveis após o último sorteio.
        """
        frequencia_padrao = estatisticas.get('frequencia_terminacoes_padrao', {})
        frequencia_total = estatisticas.get('frequencia_total', {})
        
        if not frequencia_padrao or not frequencia_total:
            return []

        # Soma as frequências de todas as terminações futuras prováveis
        terminacoes_futuras_comuns = Counter()
        for terminacoes_seguintes in frequencia_padrao.values():
            terminacoes_futuras_comuns.update(terminacoes_seguintes)

        # Seleciona as terminações mais comuns
        finais_mais_comuns = [t for t, _ in terminacoes_futuras_comuns.most_common(2)]
        
        candidatos = []
        frequencia_ordenada = sorted(frequencia_total.items(), key=lambda item: item[1], reverse=True)
        
        # Encontra os números mais frequentes que correspondem às terminações mais comuns
        for num, _ in frequencia_ordenada:
            if (num % 10) in finais_mais_comuns:
                candidatos.append(num)
                if len(candidatos) >= n:
                    break
        
        # Fallback para os mais frequentes se não houver candidatos suficientes
        if len(candidatos) < n:
            sugeridos = [num for num, _ in frequencia_ordenada[:n]]
        else:
            sugeridos = candidatos
            
        return sorted(list(set(sugeridos)))
