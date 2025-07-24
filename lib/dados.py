# lib/dados.py
import os
import json

PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados_treino'))


def carregar_sorteios(pasta=PASTA_DADOS):
    """Carrega todos os sorteios da pasta especificada."""
    todos = []
    for ficheiro in sorted(os.listdir(pasta)):
        if ficheiro.endswith('.json'):
            with open(os.path.join(pasta, ficheiro), encoding='utf-8') as f:
                todos.extend(json.load(f))
    return todos


def contar_ocorrencias(sorteios):
    """Conta quantas vezes cada número apareceu."""
    from collections import Counter
    contador = Counter()
    for s in sorteios:
        for numero in s['numeros']:  # assumir estrutura {'data': ..., 'numeros': [...]}
            contador[numero] += 1
    return contador


def ultimos_n_sorteios(sorteios, n):
    """Retorna os últimos n sorteios."""
    return sorteios[-n:]
