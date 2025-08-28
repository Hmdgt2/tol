# lib/dados.py
import os
import json
from collections import Counter, defaultdict
from itertools import combinations
import datetime

# Usar a pasta de dados principal, para evitar duplicação
PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados'))

def carregar_sorteios(pasta=PASTA_DADOS):
    """
    Carrega todos os sorteios de arquivos JSON em um diretório,
    garantindo que o formato esteja correto.
    """
    todos = []
    
    if not os.path.exists(pasta):
        print(f"Diretório '{pasta}' não encontrado.")
        return []

    for nome_arquivo in sorted(os.listdir(pasta)):
        if nome_arquivo.endswith('.json'):
            caminho_completo = os.path.join(pasta, nome_arquivo)
            try:
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    dados_carregados = json.load(f)
                    
                    if isinstance(dados_carregados, dict):
                        # Se for um dicionário de anos, extrai as listas
                        for sorteios_do_ano in dados_carregados.values():
                            if isinstance(sorteios_do_ano, list):
                                todos.extend(sorteios_do_ano)
                    elif isinstance(dados_carregados, list):
                        # Se for uma lista direta, anexa
                        todos.extend(dados_carregados)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
    
    if todos:
        # Filtra os sorteios que são dicionários válidos antes de ordenar
        sorteios_validos = [s for s in todos if isinstance(s, dict) and 'data' in s and isinstance(s.get('data'), str)]
        
        # Agora, ordena apenas a lista de sorteios válidos
        sorteios_validos.sort(key=lambda s: datetime.datetime.strptime(s.get('data'), '%d/%m/%Y'))
        
        return sorteios_validos
    
    return []

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_all_stats(sorteios, all_numbers=range(1, 50)):
    """
    Calcula todas as estatísticas e características de uma só vez para um conjunto de sorteios.
    Retorna um dicionário com todas as estatísticas.
    """
    if not sorteios:
        return {
            'frequencia_total': {n: 0 for n in all_numbers},
            'ausencia_atual': {n: 0 for n in all_numbers},
            'gaps_medios': {n: float('inf') for n in all_numbers},
            'pares_frequentes': {},
            'trios_frequentes': {},
            'frequencia_por_ano': {},
            'padrao_tipos_numeros': (0, 0, 0),
            'soma_mais_comum': 0,
            'distribuicao_quadrantes': (0, 0, 0, 0),
            'distribuicao_dezenas': (0, 0, 0, 0, 0)
        }

    frequencia_total = Counter()
    ultima_ocorrencia = defaultdict(lambda: -1)
    posicoes = defaultdict(list)
    frequencia_por_ano = defaultdict(lambda: defaultdict(int))
    padroes_tipos_numeros = Counter()
    somas = []
    distribuicoes_quadrantes = Counter()
    distribuicoes_dezenas = Counter()
    pares_frequentes = Counter()
    trios_frequentes = Counter()

    total_concursos = len(sorteios)
    dezenas_faixas = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 49)]

    # Loop para calcular a maioria das estatísticas
    for idx, sorteio in enumerate(sorteios):
        numeros = sorteio.get('numeros', [])
        
        # Garante que 'numeros' é uma lista antes de processar
        if not isinstance(numeros, list) or not numeros:
            continue
            
        numeros_ordenados = sorted(numeros)

        # Frequência e Ausência
        frequencia_total.update(numeros_ordenados)
        for num in numeros_ordenados:
            ultima_ocorrencia[num] = idx
            posicoes[num].append(idx)

        # Frequência por ano
        try:
            ano = int(sorteio.get('data', '01-01-1900').split('/')[-1])
            for num in numeros_ordenados:
                frequencia_por_ano[ano][num] += 1
        except (KeyError, ValueError):
            pass

        # Padrões de composição (par/ímpar/primo)
        pares = sum(1 for n in numeros_ordenados if n % 2 == 0)
        impares = len(numeros_ordenados) - pares
        primos = sum(1 for n in numeros_ordenados if is_prime(n))
        padroes_tipos_numeros[(pares, impares, primos)] += 1

        # Somas
        somas.append(sum(numeros_ordenados))
            
        # Distribuição por quadrantes
        num_quadrantes = 4
        max_numero = 49
        tamanho_quadrante = max_numero // num_quadrantes
        contagem_quadrante = [0] * num_quadrantes
        for num in numeros_ordenados:
            for i in range(num_quadrantes):
                if (i * tamanho_quadrante + 1) <= num <= ((i + 1) * tamanho_quadrante):
                    contagem_quadrante[i] += 1
                    break
        distribuicoes_quadrantes[tuple(contagem_quadrante)] += 1

        # Distribuição por dezenas
        contagem_dezenas = [0] * len(dezenas_faixas)
        for num in numeros_ordenados:
            for i, (inf, sup) in enumerate(dezenas_faixas):
                if inf <= num <= sup:
                    contagem_dezenas[i] += 1
                    break
        distribuicoes_dezenas[tuple(contagem_dezenas)] += 1

        # Pares e trios frequentes
        pares_frequentes.update(combinations(numeros_ordenados, 2))
        trios_frequentes.update(combinations(numeros_ordenados, 3))
    
    # Calcular métricas finais que precisam do loop completo
    ausencia_atual = {num: total_concursos - ultima_ocorrencia.get(num, -1) - 1 for num in all_numbers}
    gaps_medios = {}
    for num in all_numbers:
        concursos = posicoes.get(num, [])
        if len(concursos) < 2:
            gaps_medios[num] = float('inf')
        else:
            diferencas = [j - i for i, j in zip(concursos[:-1], concursos[1:])]
            gaps_medios[num] = sum(diferencas) / len(diferencas)
    
    return {
        'frequencia_total': frequencia_total,
        'ausencia_atual': ausencia_atual,
        'gaps_medios': gaps_medios,
        'pares_frequentes': pares_frequentes,
        'trios_frequentes': trios_frequentes,
        'frequencia_por_ano': frequencia_por_ano,
        'padrao_tipos_numeros': padroes_tipos_numeros.most_common(1)[0][0] if padroes_tipos_numeros else (0, 0, 0),
        'soma_mais_comum': Counter(somas).most_common(1)[0][0] if somas else 0,
        'distribuicao_quadrantes': distribuicoes_quadrantes.most_common(1)[0][0] if distribuicoes_quadrantes else (0, 0, 0, 0),
        'distribuicao_dezenas': distribuicoes_dezenas.most_common(1)[0][0] if distribuicoes_dezenas else (0, 0, 0, 0, 0)
    }
