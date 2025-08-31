# dados.py
import os
import json
from collections import Counter, defaultdict
from itertools import combinations
import datetime
import numpy as np

# A pasta de dados principal
PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados'))
ARQUIVO_CACHE_ESTATISTICAS = os.path.join(PASTA_DADOS, 'estatisticas_cache.json')

def _carregar_sorteios():
    """Carrega todos os sorteios de arquivos JSON, ordenando-os por data."""
    todos = []
    if not os.path.exists(PASTA_DADOS):
        print(f"Diretório '{PASTA_DADOS}' não encontrado.")
        return []

    for nome_arquivo in sorted(os.listdir(PASTA_DADOS)):
        if nome_arquivo.endswith('.json'):
            caminho_completo = os.path.join(PASTA_DADOS, nome_arquivo)
            try:
                with open(caminho_completo, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, dict):
                        for sorteios_do_ano in dados.values():
                            if isinstance(sorteios_do_ano, list):
                                todos.extend(sorteios_do_ano)
                    elif isinstance(dados, list):
                        todos.extend(dados)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
                
    if todos:
        sorteios_validos = [s for s in todos if isinstance(s, dict) and 'data' in s and 'numeros' in s]
        sorteios_validos.sort(key=lambda s: datetime.datetime.strptime(s.get('data'), '%d/%m/%Y'))
        return sorteios_validos
    return []

def _calcular_frequencia_total(sorteios):
    """Calcula a frequência total de todos os números."""
    frequencia = Counter()
    for sorteio in sorteios:
        frequencia.update(sorteio['numeros'])
    return frequencia

def _calcular_ausencia_atual(sorteios):
    """Calcula o tempo de ausência de cada número."""
    ausencia = {}
    todos_numeros = set(range(1, 50))
    ultima_ocorrencia = {num: -1 for num in todos_numeros}
    for i, sorteio in enumerate(sorteios):
        for num in sorteio['numeros']:
            ultima_ocorrencia[num] = i
    
    total_concursos = len(sorteios)
    for num in todos_numeros:
        ausencia[num] = total_concursos - ultima_ocorrencia[num] - 1
    return ausencia

def _calcular_gaps_medios(sorteios):
    """Calcula o gap médio entre as saídas de cada número."""
    posicoes = defaultdict(list)
    gaps_medios = {}
    todos_numeros = set(range(1, 50))
    for i, sorteio in enumerate(sorteios):
        for num in sorteio['numeros']:
            posicoes[num].append(i)
    
    for num in todos_numeros:
        concursos = posicoes.get(num, [])
        if len(concursos) < 2:
            gaps_medios[num] = float('inf')
        else:
            diferencas = [j - i for i, j in zip(concursos[:-1], concursos[1:])]
            gaps_medios[num] = sum(diferencas) / len(diferencas)
    return gaps_medios

def _calcular_frequencia_pares(sorteios):
    """Calcula a frequência de todos os pares de números."""
    frequencia_pares = Counter()
    for sorteio in sorteios:
        pares = combinations(sorted(sorteio['numeros']), 2)
        frequencia_pares.update(pares)
    return frequencia_pares

def _calcular_frequencia_trios(sorteios):
    """Calcula a frequência de todos os trios de números."""
    frequencia_trios = Counter()
    for sorteio in sorteios:
        trios = combinations(sorted(sorteio['numeros']), 3)
        frequencia_trios.update(trios)
    return frequencia_trios

def _calcular_frequencia_recente(sorteios, janela=15):
    """Calcula a frequência dos números numa janela de tempo recente."""
    janela_sorteios = sorteios[-janela:]
    frequencia = Counter()
    for sorteio in janela_sorteios:
        frequencia.update(sorteio['numeros'])
    return frequencia

def _calcular_frequencia_por_posicao(sorteios):
    """Calcula a frequência de cada número por posição."""
    frequencia_posicao = defaultdict(Counter)
    if not sorteios or not sorteios[0]['numeros']:
        return frequencia_posicao
    
    num_posicoes = len(sorteios[0]['numeros'])
    for sorteio in sorteios:
        numeros = sorted(sorteio['numeros'])
        for i, num in enumerate(numeros):
            frequencia_posicao[i][num] += 1
    return frequencia_posicao

def _calcular_frequencia_terminacoes_padrao(sorteios):
    """Calcula a frequência de terminações após um determinado final de sorteio."""
    padrao = defaultdict(Counter)
    if len(sorteios) < 2:
        return padrao
    
    for i in range(len(sorteios) - 1):
        numeros_atual = sorted(sorteios[i].get('numeros', []))
        numeros_seguinte = sorted(sorteios[i+1].get('numeros', []))
        terminacoes_atual = {num % 10 for num in numeros_atual}
        terminacoes_seguinte = {num % 10 for num in numeros_seguinte}
        
        for term_atual in terminacoes_atual:
            padrao[term_atual].update(terminacoes_seguinte)
            
    return padrao

def _calcular_numeros_soma_mais_frequente(sorteios):
    """
    Calcula o intervalo de soma mais comum e retorna os números mais frequentes
    que saíram dentro desse intervalo.
    """
    somas = [sum(s['numeros']) for s in sorteios if s.get('numeros')]
    if not somas:
        return []
        
    soma_media = np.mean(somas)
    soma_desvio = np.std(somas)
    soma_minima = int(soma_media - soma_desvio)
    soma_maxima = int(soma_media + soma_desvio)
    
    frequencia_intervalo = Counter()
    for s in sorteios:
        if soma_minima <= sum(s.get('numeros', [])) <= soma_maxima:
            frequencia_intervalo.update(s['numeros'])
            
    return sorted(frequencia_intervalo.keys(), key=lambda k: frequencia_intervalo[k], reverse=True)


# Mapeamento de estatísticas para as suas funções de cálculo
# A chave é o nome da estatística (dependência), o valor é a função.
MAP_ESTATISTICAS = {
    'frequencia_total': _calcular_frequencia_total,
    'ausencia_atual': _calcular_ausencia_atual,
    'gaps_medios': _calcular_gaps_medios,
    'pares_frequentes': _calcular_frequencia_pares,
    'trios_frequentes': _calcular_frequencia_trios,
    'frequencia_recente': _calcular_frequencia_recente,
    'frequencia_por_posicao': _calcular_frequencia_por_posicao,
    'frequencia_terminacoes_padrao': _calcular_frequencia_terminacoes_padrao,
    'numeros_soma_mais_frequente': _calcular_numeros_soma_mais_frequente
    # Outras estatísticas podem ser adicionadas aqui
}

def obter_estatisticas(dependencias: set, sorteios_historico: list) -> Dict[str, Any]:
    """
    Calcula e retorna apenas as estatísticas necessárias para um conjunto de heurísticas.
    
    Args:
        dependencias (set): Um conjunto com os nomes das estatísticas necessárias.
        sorteios_historico (list): A lista completa de sorteios.
        
    Returns:
        dict: Um dicionário com as estatísticas calculadas.
    """
    estatisticas = {}
    for dep in dependencias:
        if dep in MAP_ESTATISTICAS:
            try:
                # Chama a função de cálculo correspondente à dependência
                estatisticas[dep] = MAP_ESTATISTICAS[dep](sorteios_historico)
            except Exception as e:
                print(f"Erro ao calcular a estatística '{dep}': {e}")
                estatisticas[dep] = {} # Retorna um dicionário vazio em caso de erro
    
    return estatisticas

def salvar_estatisticas(estatisticas, caminho=ARQUIVO_CACHE_ESTATISTICAS):
    """Salva as estatísticas calculadas em um arquivo JSON."""
    try:
        # Serializa os objetos Counter para dicionários
        stats_serializaveis = {k: dict(v) if isinstance(v, Counter) else v for k, v in estatisticas.items()}
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(stats_serializaveis, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar as estatísticas: {e}")

def carregar_estatisticas(caminho=ARQUIVO_CACHE_ESTATISTICAS):
    """Carrega as estatísticas de um arquivo JSON."""
    if not os.path.exists(caminho):
        return None
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            stats = json.load(f)
            # Reverte os dicionários de volta para Counter, se necessário
            for k, v in stats.items():
                if isinstance(v, dict):
                    stats[k] = Counter(v)
            return stats
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao carregar o arquivo de estatísticas: {e}")
        return None
