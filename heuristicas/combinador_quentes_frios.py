# /heuristicas/combinador_quentes_frios.py

from typing import Dict, Any, List
from collections import Counter

# Importa as heurísticas que serão combinadas
from .numeros_quentes import NumerosQuentes
from .numeros_frios import NumerosFrios

class CombinadorQuentesFrios:
    # --- Metadados do Combinador ---
    NOME = "combinador_quentes_frios"
    DESCRICAO = "Combina os números mais frequentes e os mais ausentes."
    DEPENDENCIAS = ["frequencia_recente", "ausencia_atual", "frequencia_total"]

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Combina os números das heurísticas Quentes e Frios para uma previsão.
        """
        # Divide o número de sugestões que serão pegas de cada heurística
        num_quentes = n // 2 + (n % 2)
        num_frios = n // 2

        # 1. Pega os números quentes
        # Instancia a heurística NumerosQuentes
        quentes = NumerosQuentes()
        # Chama o seu método 'prever' para obter a previsão
        numeros_quentes = quentes.prever(estatisticas, n=num_quentes)

        # 2. Pega os números frios
        frios = NumerosFrios()
        numeros_frios = frios.prever(estatisticas, n=num_frios)

        # 3. Combina as listas e remove duplicados
        sugeridos = list(set(numeros_quentes + numeros_frios))
        
        # 4. Se a lista final tiver menos de 'n' números (devido a duplicados),
        # preenche com os mais frequentes no geral
        if len(sugeridos) < n:
            frequencia_geral = estatisticas.get('frequencia_total', {})
            todos_frequentes = [num for num, _ in Counter(frequencia_geral).most_common()]
            for num in todos_frequentes:
                if num not in sugeridos and len(sugeridos) < n:
                    sugeridos.append(num)
        
        return sorted(sugeridos)
