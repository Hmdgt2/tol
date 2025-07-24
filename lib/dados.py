# lib/dados.py

import os
import json
from datetime import datetime
from collections import Counter

# Caminho absoluto para a pasta de dados
PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados_treino'))


def carregar_sorteios(pasta=PASTA_DADOS):
    """
    Carrega todos os sorteios disponíveis na pasta especificada.
    Espera que cada ficheiro JSON tenha a estrutura { "ANO": [ sorteios... ] }.
    Retorna uma lista unificada de sorteios, ordenada cronologicamente.
    """
    todos = []
    for ficheiro in sorted(os.listdir(pasta)):
        if ficheiro.endswith('.json'):
            caminho = os.path.join(pasta, ficheiro)
            with open(caminho, encoding='utf-8') as f:
                conteudo = json.load(f)
                for ano_sorteios in conteudo.values():  # Ex: "2011": [ ... ]
                    todos.extend(ano_sorteios)
    
    # Ordenar por data (formato esperado: dd/mm/yyyy)
    todos.sort(key=lambda s: datetime.strptime(s['data'], '%d/%m/%Y'))
    return todos


def carregar_sorteios_ano(ano, pasta=PASTA_DADOS):
    """
    Carrega apenas os sorteios de um ano específico.
    """
    ficheiro = os.path.join(pasta, f"{ano}.json")
    if not os.path.exists(ficheiro):
        return []
    with open(ficheiro, encoding='utf-8') as f:
        conteudo = json.load(f)
        return conteudo.get(str(ano), [])


def contar_ocorrencias(sorteios):
    """
    Conta quantas vezes cada número apareceu na lista de sorteios.
    """
    contador = Counter()
    for s in sorteios:
        numeros = s.get('numeros')
        if isinstance(numeros, list):
            for numero in numeros:
                contador[numero] += 1
    return contador


def ultimos_n_sorteios(sorteios, n):
    """
    Retorna os últimos n sorteios da lista fornecida.
    """
    return sorteios[-n:]
