# heuristicas/balanceamento_tipos.py

from typing import Dict, Any, List

class BalanceamentoTipos:
    NOME = "balanceamento_tipos"
    DESCRICAO = "Sugere números equilibrando pares, ímpares e primos conforme o padrão mais comum."
    DEPENDENCIAS = ["padrao_tipos_numeros", "frequencia_total"]

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        padrao_ideal = estatisticas.get('padrao_tipos_numeros', (3, 2, 1)) # Padrão ideal (Pares, Ímpares, Primos)
        
        if not (isinstance(padrao_ideal, tuple) and len(padrao_ideal) == 3):
            padrao_ideal = (0, 0, 0)
            
        num_pares, num_impares, num_primos = padrao_ideal

        frequencia = estatisticas.get('frequencia_total', {})
        if not frequencia:
            return []

        todos_os_numeros = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        sugeridos = []
        
        # Seleciona os pares mais frequentes
        pares_candidatos = [num for num in todos_os_numeros if num % 2 == 0]
        sugeridos.extend(pares_candidatos[:num_pares])
        
        # Seleciona os ímpares mais frequentes
        impares_candidatos = [num for num in todos_os_numeros if num % 2 != 0 and num not in sugeridos]
        sugeridos.extend(impares_candidatos[:num_impares])
        
        # Seleciona os primos mais frequentes
        primos_candidatos = [num for num in todos_os_numeros if self._is_prime(num) and num not in sugeridos]
        sugeridos.extend(primos_candidatos[:num_primos])

        # Preenche com os mais frequentes se a lista ainda não tiver n números
        if len(sugeridos) < n:
            for num in todos_os_numeros:
                if len(sugeridos) >= n:
                    break
                if num not in sugeridos:
                    sugeridos.append(num)

        return sorted(sugeridos)
