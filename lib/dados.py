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
    for numero in range(1, 50):
        concursos = posicoes.get(numero, [])
        if len(concursos) < 2:
            gaps[numero] = float('inf')
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
