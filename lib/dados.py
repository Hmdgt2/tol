# lib/dados.py
import os
import json
from collections import Counter, defaultdict
from itertools import combinations

PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados_treino'))

def carregar_sorteios(pasta=PASTA_DADOS):
    todos = []
    for ficheiro in sorted(os.listdir(pasta)):
        if ficheiro.endswith('.json'):
            with open(os.path.join(pasta, ficheiro), encoding='utf-8') as f:
                dados_ano = json.load(f)
                for sorteios_ano in dados_ano.values():
                    todos.extend(sorteios_ano)
    return todos

def contar_ocorrencias(sorteios):
    contador = Counter()
    for s in sorteios:
        for numero in s.get('numeros', []):
            contador[numero] += 1
    return contador

def calcular_frequencia_por_ano(sorteios):
    freq_ano = defaultdict(lambda: defaultdict(int))
    for sorteio in sorteios:
        try:
            ano = int(sorteio['data'].split('/')[-1])
        except Exception:
            continue
        for num in sorteio.get('numeros', []):
            freq_ano[ano][num] += 1
    return freq_ano

def calcular_ausencia_atual(sorteios):
    ultima_ocorrencia = defaultdict(lambda: -1)
    total_concursos = len(sorteios)
    for idx, concurso in enumerate(sorteios):
        for numero in concurso.get('numeros', []):
            ultima_ocorrencia[numero] = idx
    return {num: total_concursos - idx - 1 for num, idx in ultima_ocorrencia.items()}

def calcular_gaps_por_numero(sorteios):
    posicoes = defaultdict(list)
    for idx, concurso in enumerate(sorteios):
        for numero in concurso.get('numeros', []):
            posicoes[numero].append(idx)

    gaps = {}
    for numero in range(1, 50): # Assumindo números de 1 a 49
        concursos = posicoes.get(numero, [])
        if len(concursos) < 2:
            gaps[numero] = float('inf') # Se só apareceu 0 ou 1 vez
        else:
            diferencas = [j - i for i, j in zip(concursos[:-1], concursos[1:])]
            gaps[numero] = sum(diferencas) / len(diferencas)
    return gaps

def contar_pares_frequentes(sorteios):
    contador_pares = Counter()
    for concurso in sorteios:
        numeros = concurso.get('numeros', [])
        pares = combinations(sorted(numeros), 2)
        contador_pares.update(pares)
    return contador_pares

def calcular_trios_frequentes(sorteios):
    trios_count = Counter()
    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        trios = combinations(sorted(numeros), 3)
        trios_count.update(trios)
    return trios_count

# --- Novas Funções para lib/dados.py ---

def is_prime(n):
    """Verifica se um número é primo."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def analisar_padrao_tipos_numeros(sorteios):
    """
    Analisa a proporção de números pares, ímpares e primos em cada sorteio.
    Retorna a contagem mais frequente de (pares, ímpares, primos).
    """
    padroes_contagem = Counter()
    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        if not numeros:
            continue
        pares = sum(1 for n in numeros if n % 2 == 0)
        impares = len(numeros) - pares
        primos = sum(1 for n in numeros if is_prime(n))
        padroes_contagem[(pares, impares, primos)] += 1
    
    # Retorna o padrão de contagem (pares, ímpares, primos) mais comum
    return padroes_contagem.most_common(1)[0][0] if padroes_contagem else (0, 0, 0)

def calcular_somas_sorteios(sorteios):
    """
    Calcula a soma dos números para cada sorteio e a frequência dessas somas.
    Retorna a soma mais frequente e o seu intervalo.
    """
    somas = []
    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        if numeros:
            somas.append(sum(numeros))
    
    if not somas:
        return {'soma_mais_comum': 0, 'intervalo_inferior': 0, 'intervalo_superior': 0}

    contador_somas = Counter(somas)
    soma_mais_comum = contador_somas.most_common(1)[0][0]

    # Calcular um intervalo em torno da soma mais comum (e.g., +/- 10%)
    # Pode ser ajustado para um desvio padrão ou um percentil, dependendo da distribuição
    min_soma = min(somas)
    max_soma = max(somas)
    
    # Uma abordagem simples para intervalo: 10% da amplitude total
    # Ou um intervalo fixo em torno da moda
    intervalo_inferior = max(min_soma, soma_mais_comum - (max_soma - min_soma) * 0.1)
    intervalo_superior = min(max_soma, soma_mais_comum + (max_soma - min_soma) * 0.1)

    return {
        'soma_mais_comum': soma_mais_comum,
        'intervalo_inferior': int(intervalo_inferior),
        'intervalo_superior': int(intervalo_superior)
    }

def analisar_distribuicao_quadrantes(sorteios, num_quadrantes=4, max_numero=49):
    """
    Analisa como os números se distribuem pelos quadrantes (grupos de números).
    Retorna a contagem mais frequente de números por quadrante.
    """
    tamanho_quadrante = max_numero // num_quadrantes
    distribuicoes_contagem = Counter()

    for sorteio in sorteios:
        numeros = sorteio.get('numeros', [])
        if not numeros:
            continue
        
        contagem_por_quadrante = [0] * num_quadrantes
        for num in numeros:
            for i in range(num_quadrantes):
                limite_inferior = i * tamanho_quadrante + 1
                limite_superior = (i + 1) * tamanho_quadrante
                if i == num_quadrantes - 1: # Último quadrante vai até ao max_numero
                    limite_superior = max_numero
                
                if limite_inferior <= num <= limite_superior:
                    contagem_por_quadrante[i] += 1
                    break
        distribuicoes_contagem[tuple(contagem_por_quadrante)] += 1
    
    return distribuicoes_contagem.most_common(1)[0][0] if distribuicoes_contagem else tuple([0] * num_quadrantes)

def calcular_repeticoes_ultimos_sorteios(sorteios, num_sorteios_anteriores=5):
    """
    Analisa a frequência de repetição de números de sorteios anteriores.
    Retorna um dicionário com a frequência de repetições (0, 1, 2, etc. números repetidos).
    """
    frequencia_repeticoes = Counter()
    
    for i in range(num_sorteios_anteriores, len(sorteios)):
        sorteio_atual = set(sorteios[i].get('numeros', []))
        
        numeros_anteriores = set()
        for j in range(1, num_sorteios_anteriores + 1):
            if i - j >= 0:
                numeros_anteriores.update(sorteios[i-j].get('numeros', []))
        
        repeticoes = len(sorteio_atual.intersection(numeros_anteriores))
        frequencia_repeticoes[repeticoes] += 1
        
    # Calcula as probabilidades com base na frequência
    total_observacoes = sum(frequencia_repeticoes.values())
    probabilidades = {k: v / total_observacoes for k, v in frequencia_repeticoes.items()}
    return probabilidades

# --- Fim das Novas Funções ---
