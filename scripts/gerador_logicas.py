# script/gerador_logicas.py
import random
import operator
from typing import List, Dict, Any, Callable

# Variáveis de entrada que a lógica usará
def calcular_variaveis(numeros: List[int]) -> Dict[str, Any]:
    if not numeros:
        return {}
    variaveis = {
        'soma': sum(numeros),
        'maior': max(numeros),
        'menor': min(numeros),
        'media': sum(numeros) // len(numeros),
        'primeiro': sorted(numeros)[0],
        'ultimo': sorted(numeros)[-1],
        'diferenca_maior_menor': max(numeros) - min(numeros),
        'soma_pares': sum(n for n in numeros if n % 2 == 0),
        'soma_impares': sum(n for n in numeros if n % 2 != 0),
        'soma_ultimos_digitos': sum(n % 10 for n in numeros),
        'total_numeros': len(numeros),
    }
    return variaveis

# Operadores matemáticos
OPERADORES = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '//': operator.floordiv,
    '%': operator.mod,
}

# O Gerador de Lógicas
def gerar_logicas(variaveis: Dict[str, Any], num_logicas: int = 200) -> List[Dict[str, Any]]:
    chaves_variaveis = list(variaveis.keys())
    chaves_operadores = list(OPERADORES.keys())
    logicas_geradas = []

    for _ in range(num_logicas):
        var1_nome = random.choice(chaves_variaveis)
        var2_nome = random.choice(chaves_variaveis)
        op_simbolo = random.choice(chaves_operadores)

        # Evitar a divisão por zero
        if (op_simbolo in ['//', '%']) and variaveis[var2_nome] == 0:
            continue

        nome_logica = f"{var1_nome}_{op_simbolo}_{var2_nome}"
        
        # A função lambda que será testada
        func_logica = lambda v, v1=var1_nome, v2=var2_nome, op=op_simbolo: OPERADORES[op](v[v1], v[v2])
        
        logicas_geradas.append({'nome': nome_logica, 'func': func_logica})

    return logicas_geradas
