# heuristicas/balanceamento_tipos.py

from typing import Dict, Any, List

class BalanceamentoTipos:
    NOME = "balanceamento_tipos"
    DESCRICAO = "Sugere números equilibrando pares, ímpares e primos conforme o padrão mais comum."
    DEPENDENCIAS = ["padrao_tipos_numeros", "frequencia_total"]

    def _is_prime(self, n: int) -> bool:
        """Função auxiliar para verificar se um número é primo."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def prever(self, estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
        """
        Prevê números com base no padrão de balanceamento de pares, ímpares e primos.
        """
        padrao_ideal = estatisticas.get('padrao_tipos_numeros', (0, 0, 0))
        frequencia = estatisticas.get('frequencia_total', {})

        if not frequencia:
            return []

        candidatos_por_tipo = {
            'par': sorted([num for num in frequencia if num % 2 == 0], key=lambda x: frequencia[x], reverse=True),
            'impar': sorted([num for num in frequencia if num % 2 != 0], key=lambda x: frequencia[x], reverse=True),
            'primo': sorted([num for num in frequencia if self._is_prime(num)], key=lambda x: frequencia[x], reverse=True),
        }

        sugeridos = []
        num_pares, num_impares, num_primos = padrao_ideal

        for _ in range(num_pares):
            if candidatos_por_tipo['par']:
                sugeridos.append(candidatos_por_tipo['par'].pop(0))

        for _ in range(num_impares):
            if candidatos_por_tipo['impar']:
                sugeridos.append(candidatos_por_tipo['impar'].pop(0))

        for _ in range(num_primos):
            if candidatos_por_tipo['primo'] and candidatos_por_tipo['primo'][0] not in sugeridos:
                sugeridos.append(candidatos_por_tipo['primo'].pop(0))

        frequencia_ordenada = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
        for num in frequencia_ordenada:
            if len(sugeridos) >= n:
                break
            if num not in sugeridos:
                sugeridos.append(num)

        return sorted(sugeridos)
