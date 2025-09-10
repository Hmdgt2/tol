# heuristicas/balanceamento_tipos.py

from typing import Dict, Any, List

class BalanceamentoTipos:
    NOME = "balanceamento_tipos"
    DESCRICAO = "Sugere uma combinação balanceada de pares, ímpares e primos, preenchendo a lista com os números menos frequentes para garantir diversidade."
    DEPENDENCIAS = ["padrao_tipos_numeros", "frequencia_total"]

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        padrao_ideal = estatisticas.get('padrao_tipos_numeros', (3, 2, 1))
        
        if not (isinstance(padrao_ideal, tuple) and len(padrao_ideal) == 3):
            padrao_ideal = (0, 0, 0)
            
        num_pares_desejados, num_impares_desejados, num_primos_desejados = padrao_ideal

        frequencia = estatisticas.get('frequencia_total', {})
        if not frequencia:
            return []

        todos_os_numeros_ordenados_por_frequencia = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        sugeridos = []
        
        # Seleção inicial: pega os mais frequentes de cada tipo
        pares_frequentes = [num for num in todos_os_numeros_ordenados_por_frequencia if num % 2 == 0]
        impares_frequentes = [num for num in todos_os_numeros_ordenados_por_frequencia if num % 2 != 0]
        primos_frequentes = [num for num in todos_os_numeros_ordenados_por_frequencia if self._is_prime(num)]
        
        sugeridos.extend(pares_frequentes[:num_pares_desejados])
        sugeridos.extend(impares_frequentes[:num_impares_desejados])
        sugeridos.extend(primos_frequentes[:num_primos_desejados])
        
        # Preenchimento: completa a lista com os números menos frequentes
        while len(sugeridos) < n:
            candidatos_restantes_por_frequencia = sorted(
                [num for num in todos_os_numeros_ordenados_por_frequencia if num not in sugeridos],
                key=lambda x: frequencia[x]
            )
            if not candidatos_restantes_por_frequencia:
                break
            
            sugeridos.append(candidatos_restantes_por_frequencia[0])

        return sorted(sugeridos)
