import importlib
from typing import Dict, Any, List
from collections import Counter
import numpy as np

class MetaAvaliacao:
    # --- Metadados da Heurística ---
    NOME = "meta_avaliacao"
    DESCRICAO = "Avalia a precisão posicional histórica para sugerir os números mais frequentes das posições mais precisas."
    # Adicionada a dependência 'frequencia_por_posicao' para a nova lógica.
    DEPENDENCIAS = ["precisao_posicional_historica", "frequencia_por_posicao"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nas posições de maior precisão histórica.
        """
        precisao_posicional = estatisticas.get('precisao_posicional_historica', {})
        frequencia_por_posicao = estatisticas.get('frequencia_por_posicao', {})

        if not precisao_posicional or not frequencia_por_posicao:
            # Fallback se não houver dados de precisão ou frequência por posição
            print("Aviso: Dados insuficientes para a heurística 'meta_avaliacao'. A retornar lista vazia.")
            return []

        try:
            # Encontra a posição com a menor pontuação de precisão (mais precisa)
            # A precisão é a distância da média, então um valor menor é melhor.
            posicao_vencedora = min(precisao_posicional, key=precisao_posicional.get)

            # Obtém os números mais frequentes para a posição vencedora
            numeros_da_posicao = frequencia_por_posicao.get(posicao_vencedora, {})
            
            # Ordena os números por frequência e retorna os 'n' primeiros
            previsao = sorted(numeros_da_posicao, key=numeros_da_posicao.get, reverse=True)[:n]
            
            return previsao

        except Exception as e:
            print(f"Erro ao executar a heurística 'meta_avaliacao': {e}")
            return []
