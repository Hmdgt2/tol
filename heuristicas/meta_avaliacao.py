import importlib
from typing import Dict, Any, List
from collections import Counter
import numpy as np

class MetaAvaliacao:
    # --- Metadados da Heurística ---
    NOME = "meta_avaliacao"
    DESCRICAO = "Avalia a precisão posicional histórica para sugerir os números mais frequentes das posições mais precisas."
    # As dependências continuam as mesmas.
    DEPENDENCIAS = ["precisao_posicional_historica", "frequencia_por_posicao"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base nas posições de maior precisão histórica,
        agregando dados das posições mais precisas.
        
        Args:
            estatisticas (Dict[str, Any]): Dicionário de estatísticas dos sorteios.
            n (int): O número de sugestões a serem retornadas.
            num_posicoes_a_considerar (int): O número de posições mais precisas a serem consideradas.
        
        Returns:
            List[int]: Uma lista de números inteiros sugeridos.
        """
        precisao_posicional = estatisticas.get('precisao_posicional_historica', {})
        frequencia_por_posicao = estatisticas.get('frequencia_por_posicao', {})
        
        # Define o número de posições a serem consideradas, com um valor padrão de 3.
        num_posicoes_a_considerar = 3

        if not precisao_posicional or not frequencia_por_posicao:
            # Fallback se não houver dados de precisão ou frequência por posição
            print("Aviso: Dados insuficientes para a heurística 'meta_avaliacao'. A retornar lista vazia.")
            return []

        try:
            # 1. Encontra as posições com a menor pontuação de precisão (mais precisas).
            # A precisão é a distância da média, então um valor menor é melhor.
            posicoes_ordenadas = sorted(precisao_posicional.keys(), key=lambda p: precisao_posicional[p])
            top_posicoes = posicoes_ordenadas[:num_posicoes_a_considerar]

            # 2. Agrega os números mais frequentes dessas posições.
            frequencia_combinada = Counter()
            for posicao in top_posicoes:
                numeros_da_posicao = frequencia_por_posicao.get(posicao, {})
                frequencia_combinada.update(numeros_da_posicao)

            # 3. Ordena os números agregados por frequência e retorna os 'n' mais comuns.
            previsao = sorted(frequencia_combinada, key=frequencia_combinada.get, reverse=True)[:n]
            
            return previsao

        except Exception as e:
            print(f"Erro ao executar a heurística 'meta_avaliacao': {e}")
            return []
