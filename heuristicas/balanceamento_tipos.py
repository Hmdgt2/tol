# heuristicas/balanceamento_tipos.py
from typing import Dict, Any, List

# --- Metadados da Heurística ---
# A nova arquitetura usa um padrão de metadados para saber o que a heurística faz e o que precisa.
NOME = "balanceamento_tipos"
DESCRICAO = "Sugere números equilibrando pares, ímpares e primos conforme o padrão mais comum."
# A heurística declara explicitamente que precisa de duas estatísticas do dados.py.
DEPENDENCIAS = ["padrao_tipos_numeros", "frequencia_total"]

def prever(estatisticas: Dict[str, Any], n: int = 5) -> List[int]:
    """
    Prevê números com base no padrão de balanceamento de pares, ímpares e primos.
    
    Args:
        estatisticas (dict): Dicionário com as estatísticas de que a heurística depende.
        n (int): O número de sugestões a retornar.
        
    Returns:
        list: Uma lista de números sugeridos.
    """
    # Acessa as estatísticas de padrão de tipos e frequência total
    padrao_ideal = estatisticas.get('padrao_tipos_numeros', (0, 0, 0))
    frequencia = estatisticas.get('frequencia_total', {})
    
    if not frequencia:
        return []

    # Separa os números mais frequentes por tipo
    candidatos_por_tipo = {
        'par': sorted([num for num in frequencia if num % 2 == 0], key=lambda x: frequencia[x], reverse=True),
        'impar': sorted([num for num in frequencia if num % 2 != 0], key=lambda x: frequencia[x], reverse=True),
        'primo': sorted([num for num in frequencia if _is_prime(num)], key=lambda x: frequencia[x], reverse=True),
    }

    # Lógica de seleção
    sugeridos = []
    num_pares, num_impares, num_primos = padrao_ideal
    
    # Adiciona os números pares mais frequentes
    for _ in range(num_pares):
        if candidatos_por_tipo['par']:
            sugeridos.append(candidatos_por_tipo['par'].pop(0))

    # Adiciona os números ímpares mais frequentes
    for _ in range(num_impares):
        if candidatos_por_tipo['impar']:
            sugeridos.append(candidatos_por_tipo['impar'].pop(0))

    # Adiciona os números primos mais frequentes
    for _ in range(num_primos):
        if candidatos_por_tipo['primo'] and candidatos_por_tipo['primo'][0] not in sugeridos:
            sugeridos.append(candidatos_por_tipo['primo'].pop(0))

    # Preenche o restante com os números mais frequentes que ainda não foram selecionados
    frequencia_ordenada = sorted(frequencia.keys(), key=lambda x: frequencia[x], reverse=True)
    for num in frequencia_ordenada:
        if len(sugeridos) >= n:
            break
        if num not in sugeridos:
            sugeridos.append(num)
            
    return sorted(sugeridos)

# A função _is_prime() deve ser movida para o dados.py, para centralizar a lógica.
# No entanto, para esta heurística funcionar de forma isolada, pode mantê-la temporariamente.
def _is_prime(n: int) -> bool:
    """Função auxiliar para verificar se um número é primo."""
    if n < 2: 
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: 
            return False
    return True
