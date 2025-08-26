# heuristicas/balanceamento_tipos.py
from lib.dados import analisar_padrao_tipos_numeros, is_prime
from collections import Counter
from collections import defaultdict
import random

def prever(sorteios, n=2):
    padrao_ideal_pares_impares_primos = analisar_padrao_tipos_numeros(sorteios)
    
    todos_numeros_candidatos = list(range(1, 50))
    
    # Tentativa de construir um conjunto que se aproxime do padrão ideal
    # Esta heurística é mais complexa para gerar exatamente 'n' números
    # Vamos sugerir alguns números que ajudem a equilibrar, se o conjunto de 5 for criado mais tarde
    
    # Para simplificar, podemos sugerir os números mais frequentes que correspondem aos "tipos" necessários.
    # Ou, uma abordagem mais simples para esta heurística é apenas identificar os tipos que mais saem
    # e sugerir números que se encaixem nessa categoria, se ainda não houver suficientes na previsão combinada.

    # Abordagem: sugerir números aleatórios que se encaixem nas proporções mais comuns
    # Esta heurística tenta "forçar" uma composição de tipos.

    # Poderíamos também usar a frequência geral para dar preferência a números "quentes" que se encaixam no tipo.
    # Por agora, vamos apenas pegar nos números que têm aparecido mais e que se encaixam no padrão.
    
    # Contar a frequência geral para dar preferência
    frequencia_geral = Counter()
    for s in sorteios:
        frequencia_geral.update(s.get('numeros', []))
    
    candidatos_por_tipo = defaultdict(list)
    for num in sorted(todos_numeros_candidatos, key=lambda x: frequencia_geral[x], reverse=True):
        if num % 2 == 0:
            candidatos_por_tipo['par'].append(num)
        else:
            candidatos_por_tipo['impar'].append(num)
        if is_prime(num):
            candidatos_por_tipo['primo'].append(num)

    sugeridos = []
    # Idealmente, aqui construiríamos 5 números que correspondam ao padrão.
    # Para os n=2, vamos pegar nos números mais frequentes que encaixem nos tipos desejados.
    
    # Exemplo: Se o padrão ideal é (3 pares, 2 ímpares, X primos)
    # Podemos tentar pegar 1 par e 1 ímpar dos mais frequentes, ou 2 pares, etc.
    # Para n=2, é um desafio, pois não temos o contexto do sorteio completo.

    # Simplificando para 2 números: pega os 2 números mais frequentes que se encaixam 
    # na categoria mais predominante (par ou ímpar) OU os 2 mais frequentes que se destacam como primos.
    
    # Heurística simplificada para 2 números:
    # Se há mais pares no padrão, tenta sugerir 2 pares. Se mais ímpares, 2 ímpares.
    # Ou pega um par e um ímpar dos mais frequentes.

    # Escolha os n mais frequentes de uma mistura de pares/ímpares para tentar cobrir a probabilidade.
    # Esta heurística é mais eficaz quando combinamos 5 números. Para 2, é mais difícil.
    
    # Uma abordagem para n=2: Selecionar os 2 números que mais contribuíram para o padrão ideal nos sorteios passados.
    # Ou, pegar os n números mais frequentes, e se eles desequilibrarem muito o padrão, ajustar ligeiramente.
    
    # Versão simplificada: Pega os números mais frequentes que são pares E os mais frequentes que são ímpares
    # E seleciona os top n de uma lista combinada.
    
    candidatos_ordenados_por_freq = [num for num, _ in frequencia_geral.most_common(len(frequencia_geral))]
    
    sugeridos_balanceados = []
    num_pares_desejados = padrao_ideal_pares_impares_primos[0]
    num_impares_desejados = padrao_ideal_pares_impares_primos[1]
    
    # Tenta obter uma mistura dos mais frequentes que se encaixem na proporção
    # Para n=2, vamos escolher 1 par e 1 ímpar dos mais frequentes, se existirem
    pares_freq = [num for num in candidatos_ordenados_por_freq if num % 2 == 0]
    impares_freq = [num for num in candidatos_ordenados_por_freq if num % 2 != 0]

    if pares_freq and impares_freq:
        sugeridos_balanceados.append(pares_freq[0])
        sugeridos_balanceados.append(impares_freq[0])
    elif pares_freq and len(pares_freq) >= 2:
        sugeridos_balanceados.extend(pares_freq[:2])
    elif impares_freq and len(impares_freq) >= 2:
        sugeridos_balanceados.extend(impares_freq[:2])
    else: # Fallback, se não houver pares/ímpares suficientes
        sugeridos_balanceados.extend(candidatos_ordenados_por_freq[:n])

    return {
        "nome": "balanceamento_tipos",
        "numeros": sorted(list(set(sugeridos_balanceados)))[:n] # Garante que são n e únicos
    }
