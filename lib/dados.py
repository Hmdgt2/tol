# lib/dados.py

import os
import sys
import json
from collections import Counter, defaultdict
from itertools import combinations
import datetime
import numpy as np
import inspect
from typing import Dict, Any, List, Tuple

# A pasta de dados principal
PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados'))
ARQUIVO_CACHE_ESTATISTICAS = os.path.join(PASTA_DADOS, 'estatisticas_cache.json')

class Dados:
    def __init__(self, caminho_dados: str = PASTA_DADOS):
        self.caminho_dados = caminho_dados
        self.sorteios = self._carregar_sorteios()
        self.mapeamento_calculos = self._get_mapeamento_calculos()
        self._estatisticas_cache = {}

    def _carregar_sorteios(self) -> List[Dict[str, Any]]:
        """Carrega todos os sorteios de arquivos JSON, ordenando-os por data."""
        todos = []
        if not os.path.exists(self.caminho_dados):
            print(f"Diretório '{self.caminho_dados}' não encontrado.")
            return []

        for nome_arquivo in sorted(os.listdir(self.caminho_dados)):
            if nome_arquivo.endswith('.json'):
                caminho_completo = os.path.join(self.caminho_dados, nome_arquivo)
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
    
    # Função auxiliar para verificar se um número é primo
    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    # --- Funções de Cálculo ---
    def _calcular_frequencia_total(self) -> Counter:
        """Calcula a frequência total de todos os números."""
        frequencia = Counter()
        for sorteio in self.sorteios:
            frequencia.update(sorteio['numeros'])
        return frequencia

    def _calcular_ausencia_atual(self) -> Dict[int, int]:
        """Calcula o tempo de ausência de cada número."""
        ausencia = {}
        todos_numeros = set(range(1, 50))
        ultima_ocorrencia = {num: -1 for num in todos_numeros}
        for i, sorteio in enumerate(self.sorteios):
            for num in sorteio['numeros']:
                ultima_ocorrencia[num] = i
            
        total_concursos = len(self.sorteios)
        for num in todos_numeros:
            ausencia[num] = total_concursos - ultima_ocorrencia[num] - 1
        return ausencia

    def _calcular_gaps_medios(self) -> Dict[int, float]:
        """Calcula o gap médio entre as saídas de cada número."""
        posicoes = defaultdict(list)
        gaps_medios = {}
        todos_numeros = set(range(1, 50))
        for i, sorteio in enumerate(self.sorteios):
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

    def _calcular_frequencia_pares(self) -> Counter:
        """Calcula a frequência de todos os pares de números."""
        frequencia_pares = Counter()
        for sorteio in self.sorteios:
            pares = combinations(sorted(sorteio['numeros']), 2)
            frequencia_pares.update(pares)
        return frequencia_pares

    def _calcular_frequencia_trios(self) -> Counter:
        """Calcula a frequência de todos os trios de números."""
        frequencia_trios = Counter()
        for sorteio in self.sorteios:
            trios = combinations(sorted(sorteio['numeros']), 3)
            frequencia_trios.update(trios)
        return frequencia_trios
        
    def _calcular_frequencia_grupos(self) -> Counter:
        """
        Calcula a frequência de grupos de 2, 3 e 4 números.
        Isso é usado pela heurística de padrões de grupos.
        """
        frequencia_grupos = Counter()
        for sorteio in self.sorteios:
            numeros = sorted(sorteio['numeros'])
            for i in range(2, 5): # Grupos de tamanho 2, 3 e 4
                grupos = combinations(numeros, i)
                frequencia_grupos.update(grupos)
        return frequencia_grupos

    def _calcular_frequencia_recente(self, janela=15) -> Counter:
        """Calcula a frequência dos números numa janela de tempo recente."""
        janela_sorteios = self.sorteios[-janela:]
        frequencia = Counter()
        for sorteio in janela_sorteios:
            frequencia.update(sorteio['numeros'])
        return frequencia

    def _calcular_frequencia_por_posicao(self) -> Dict[int, Counter]:
        """Calcula a frequência de cada número por posição."""
        frequencia_posicao = defaultdict(Counter)
        if not self.sorteios or not self.sorteios[0]['numeros']:
            return frequencia_posicao
            
        num_posicoes = len(self.sorteios[0]['numeros'])
        for sorteio in self.sorteios:
            numeros = sorted(sorteio['numeros'])
            if len(numeros) != num_posicoes: # Adicionando validação para sorteios incompletos
                continue
            for i, num in enumerate(numeros):
                frequencia_posicao[i].update([num])
        return frequencia_posicao

    def _calcular_frequencia_terminacoes_padrao(self) -> Dict[int, Counter]:
        """Calcula a frequência de terminações após um determinado final de sorteio."""
        padrao = defaultdict(Counter)
        if len(self.sorteios) < 2:
            return padrao
            
        for i in range(len(self.sorteios) - 1):
            numeros_atual = sorted(self.sorteios[i].get('numeros', []))
            numeros_seguinte = sorted(self.sorteios[i+1].get('numeros', []))
            terminacoes_atual = {num % 10 for num in numeros_atual}
            terminacoes_seguinte = {num % 10 for num in numeros_seguinte}
            
            for term_atual in terminacoes_atual:
                padrao[term_atual].update(terminacoes_seguinte)
                
        return padrao

    def _calcular_numeros_soma_mais_frequente(self) -> List[int]:
        """
        Calcula o intervalo de soma mais comum (usando percentis) e retorna os números mais frequentes
        que saíram dentro desse intervalo.
        """
        somas = [sum(s['numeros']) for s in self.sorteios if s.get('numeros')]
        if not somas:
            return []
            
        # Usa percentis para encontrar um intervalo mais robusto
        soma_25_percentil = np.percentile(somas, 25)
        soma_75_percentil = np.percentile(somas, 75)
        
        frequencia_intervalo = Counter()
        for s in self.sorteios:
            soma_sorteio = sum(s.get('numeros', []))
            if soma_25_percentil <= soma_sorteio <= soma_75_percentil:
                frequencia_intervalo.update(s['numeros'])
            
        return sorted(frequencia_intervalo.keys(), key=lambda k: frequencia_intervalo[k], reverse=True)

    def _calcular_padrao_tipos_numeros(self) -> Counter:
        """
        Calcula a distribuição de frequência de padrões de pares, ímpares e primos.
        Retorna o Counter completo, com todos os padrões encontrados.
        """
        padroes = Counter()
        for sorteio in self.sorteios:
            if not sorteio.get('numeros'):
                continue
            
            numeros = sorteio['numeros']
            contagem_pares = sum(1 for n in numeros if n % 2 == 0)
            contagem_impares = sum(1 for n in numeros if n % 2 != 0)
            contagem_primos = sum(1 for n in numeros if self._is_prime(n))
            
            padroes.update([(contagem_pares, contagem_impares, contagem_primos)])
            
        return padroes

    # --- NOVAS FUNÇÕES DE CÁLCULO PARA AS DEPENDÊNCIAS FALTANTES ---
    def _calcular_distribuicao_quadrantes(self) -> Dict[int, int]:
        """Calcula a frequência de números por quadrante (1-12, 13-24, 25-36, 37-49)."""
        distribuicao = defaultdict(int)
        for sorteio in self.sorteios:
            for num in sorteio['numeros']:
                if 1 <= num <= 12:
                    distribuicao[1] += 1
                elif 13 <= num <= 24:
                    distribuicao[2] += 1
                elif 25 <= num <= 36:
                    distribuicao[3] += 1
                else: # 37 <= num <= 49
                    distribuicao[4] += 1
        return distribuicao

    def _calcular_frequencia_vizinhos(self) -> Dict[int, int]:
        """Calcula a frequência de cada número ter um de seus vizinhos sorteado."""
        frequencia = defaultdict(int)
        for sorteio in self.sorteios:
            numeros_sorteados = set(sorteio['numeros'])
            for num in numeros_sorteados:
                if (num - 1) in numeros_sorteados or (num + 1) in numeros_sorteados:
                    frequencia[num] += 1
        return frequencia

    def _calcular_pares_recentes(self) -> Counter:
        """Calcula a frequência de pares de números nos últimos 20 sorteios."""
        janela_sorteios = self.sorteios[-20:]
        frequencia_pares = Counter()
        for sorteio in janela_sorteios:
            pares = combinations(sorted(sorteio['numeros']), 2)
            frequencia_pares.update(pares)
        return frequencia_pares

    def _calcular_frequencia_pares_consecutivos(self) -> Counter:
        """Calcula a frequência de pares de números consecutivos (ex: 5 e 6)."""
        frequencia = Counter()
        for sorteio in self.sorteios:
            numeros = sorted(sorteio['numeros'])
            for i in range(len(numeros) - 1):
                if numeros[i+1] == numeros[i] + 1:
                    frequencia[(numeros[i], numeros[i+1])] += 1
        return frequencia

    def _calcular_precisao_posicional_historica(self) -> Dict[int, float]:
        """Calcula a precisão média de cada posição do sorteio, de forma otimizada."""
        if not self.sorteios:
            return {}

        num_posicoes = len(self.sorteios[0]['numeros'])
        
        # PASSO 1: Pré-calcular a média de cada posição uma única vez.
        somas_por_posicao = defaultdict(int)
        for sorteio in self.sorteios:
            numeros_sorteio = sorted(sorteio['numeros'])
            if len(numeros_sorteio) != num_posicoes: # Adicionando validação para sorteios incompletos
                continue
            for i, num in enumerate(numeros_sorteio):
                if i < num_posicoes:
                    somas_por_posicao[i] += num
        
        media_posicoes = {
            i: somas_por_posicao[i] / len(self.sorteios)
            for i in range(num_posicoes)
        }
        
        # PASSO 2: Calcular o desvio de cada número em relação à sua média de posição.
        precisao_por_posicao = defaultdict(list)
        for sorteio in self.sorteios:
            numeros = sorted(sorteio['numeros'])
            if len(numeros) != num_posicoes: # Adicionando validação
                continue
            for i, num in enumerate(numeros):
                if i < num_posicoes:
                    # Usamos a média pré-calculada, não a recalculamos a cada iteração
                    precisao = abs(num - media_posicoes[i])
                    precisao_por_posicao[i].append(precisao)

        # PASSO 3: Calcular a média desses desvios.
        medias_precisao = {pos: np.mean(vals) for pos, vals in precisao_por_posicao.items()}
        
        return medias_precisao

    def _calcular_frequencia_por_ano(self) -> Dict[int, Counter]:
        """Calcula a frequência de números por ano."""
        frequencia_anual = defaultdict(Counter)
        for sorteio in self.sorteios:
            ano = datetime.datetime.strptime(sorteio['data'], '%d/%m/%Y').year
            frequencia_anual[ano].update(sorteio['numeros'])
        return frequencia_anual

    def _calcular_distribuicao_dezenas(self) -> Dict[int, int]:
        """Calcula a frequência de números por dezena (1-10, 11-20, etc.)."""
        distribuicao = defaultdict(int)
        for sorteio in self.sorteios:
            for num in sorteio['numeros']:
                if num == 0:
                    continue
                dezena = (num - 1) // 10 + 1
                distribuicao[dezena] += 1
        return distribuicao

    def _calcular_trios_frequentes(self) -> Counter:
        """Calcula a frequência de todos os trios de números (alternativa)."""
        frequencia_trios = Counter()
        for sorteio in self.sorteios:
            trios = combinations(sorted(sorteio['numeros']), 3)
            frequencia_trios.update(trios)
        return frequencia_trios

    def _calcular_probabilidades_repeticoes(self) -> Dict[int, float]:
        """Calcula a probabilidade de um número se repetir no sorteio seguinte, dado que saiu no anterior."""
        probabilidades = defaultdict(float)
        if len(self.sorteios) < 2:
            return {}

        ocorrencias = defaultdict(int)
        saidas_anteriores = defaultdict(int)

        for i in range(1, len(self.sorteios)):
            numeros_anteriores = set(self.sorteios[i-1]['numeros'])
            numeros_atuais = set(self.sorteios[i]['numeros'])

            for num in numeros_anteriores:
                saidas_anteriores[num] += 1
                if num in numeros_atuais:
                    ocorrencias[num] += 1
        
        # Calcula a probabilidade para cada número
        for num in saidas_anteriores:
            if saidas_anteriores[num] > 0:
                probabilidades[num] = ocorrencias[num] / saidas_anteriores[num]
        
        return probabilidades

    def _calcular_frequencia_por_ciclo(self) -> Dict[str, Any]:
        """
        Calcula a frequência de cada número em múltiplos ciclos de sorteios.
        Retorna a frequência para ciclos de 10, 20 e 30 sorteios.
        """
        frequencia_por_ciclo = {}
        if not self.sorteios:
            return frequencia_por_ciclo

        janelas = [10, 20, 30]
        for janela in janelas:
            sorteios_do_ciclo = self.sorteios[-janela:]
            frequencia = Counter()
            for sorteio in sorteios_do_ciclo:
                frequencia.update(sorteio.get('numeros', []))
            frequencia_por_ciclo[f'ultimos_{janela}'] = frequencia
            
        return frequencia_por_ciclo

    # --- Lógica de Mapeamento e Obtenção de Estatísticas ---
    def _get_mapeamento_calculos(self) -> Dict[str, callable]:
        """Mapeia automaticamente nomes de estatísticas para funções de cálculo internas."""
        mapeamento = {}
        for name, obj in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('_calcular_'):
                estatistica_name = name.replace('_calcular_', '')
                mapeamento[estatistica_name] = obj
        return mapeamento

    def obter_estatisticas(self, dependencias: set) -> Tuple[Dict[str, Any], List[str]]:
        """
        Calcula e retorna apenas as estatísticas necessárias, juntamente com uma lista de erros.
        """
        estatisticas = {}
        erros = []
        for dep in dependencias:
            if dep in self.mapeamento_calculos:
                try:
                    # Chamada do método da classe
                    estatisticas[dep] = self.mapeamento_calculos[dep]()
                except Exception as e:
                    erros.append(f"Erro ao calcular a estatística '{dep}': {e}")
                    estatisticas[dep] = {}
            else:
                erros.append(f"Função de cálculo para '{dep}' não encontrada.")
                estatisticas[dep] = {}
            
        return estatisticas, erros

    def obter_resumo_calculos_com_metadados(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna um resumo das funções de cálculo disponíveis, com descrições
        e palavras-chave associadas. Serve para o gerar_resumo_analise.py.
        """
        return {
            "frequencia_total": {
                "descricao": "Frequência total de ocorrência de cada número ao longo de todos os sorteios.",
                "logica_principais": ["frequencia", "global", "historico"]
            },
            "ausencia_atual": {
                "descricao": "Número de concursos decorridos desde a última vez que cada número saiu.",
                "logica_principais": ["ausencia", "atraso", "recencia"]
            },
            "gaps_medios": {
                "descricao": "Intervalo médio de concursos entre aparições sucessivas de cada número.",
                "logica_principais": ["gap", "periodicidade", "ritmo"]
            },
            "frequencia_pares": {
                "descricao": "Contagem de todas as combinações de pares que já saíram nos sorteios.",
                "logica_principais": ["pares", "combinacoes", "associacao"]
            },
            "frequencia_trios": {
                "descricao": "Contagem de todas as combinações de trios que já saíram nos sorteios.",
                "logica_principais": ["trios", "combinacoes", "associacao"]
            },
            "frequencia_recente": {
                "descricao": "Frequência dos números considerando apenas uma janela dos últimos sorteios.",
                "logica_principais": ["frequencia", "recente", "tendencia"]
            },
            "frequencia_por_posicao": {
                "descricao": "Frequência de cada número por posição no sorteio.",
                "logica_principais": ["posicao", "frequencia", "historico"]
            },
            "distribuicao_dezenas": {
                "descricao": "Distribuição de frequência dos números por grupo de dezenas (0-9, 10-19, etc.).",
                "logica_principais": ["distribuicao", "dezenas", "agrupamento"]
            },
            "distribuicao_quadrantes": {
                "descricao": "Distribuição de frequência dos números pelos quadrantes (1-12, 13-24, 25-36, 37-49).",
                "logica_principais": ["distribuicao", "quadrantes", "agrupamento"]
            },
            "frequencia_por_ciclo": {
                "descricao": "Frequência de ocorrência dos números dentro de ciclos recentes de concursos.",
                "logica_principais": ["ciclos", "recente", "frequencia"]
            },
            "frequencia_vizinhos": {
                "descricao": "Número de vezes que cada número saiu acompanhado de um vizinho (n-1 ou n+1).",
                "logica_principais": ["vizinhos", "pares", "proximidade"]
            },
            "pares_recentes": {
                "descricao": "Frequência dos pares de números nos últimos concursos.",
                "logica_principais": ["pares", "recente", "tendencia"]
            },
            "frequencia_pares_consecutivos": {
                "descricao": "Frequência de pares consecutivos (ex: 5 e 6).",
                "logica_principais": ["pares", "consecutivos", "sequencias"]
            },
            "frequencia_por_ano": {
                "descricao": "Distribuição de frequência dos números em cada ano.",
                "logica_principais": ["frequencia", "temporal", "ano"]
            },
            "probabilidades_repeticoes": {
                "descricao": "Probabilidade de um número se repetir do sorteio anterior.",
                "logica_principais": ["repeticao", "probabilidade", "historico"]
            },
            "padrao_tipos_numeros": {
                "descricao": "Padrão mais frequente de pares, ímpares e primos dentro dos sorteios.",
                "logica_principais": ["pares", "impares", "primos"]
            },
            "numeros_soma_mais_frequente": {
                "descricao": "Números mais comuns em sorteios cuja soma total caiu no intervalo típico.",
                "logica_principais": ["soma", "intervalo", "frequencia"]
            },
            "precisao_posicional_historica": {
                "descricao": "Desvio médio entre os números sorteados e a média histórica da sua posição.",
                "logica_principais": ["precisao", "posicao", "historico"]
            },
            "frequencia_grupos": {
                "descricao": "Frequência de grupos de 2, 3 e 4 números que já saíram juntos.",
                "logica_principais": ["grupos", "combinacoes", "frequencia"]
            }
        }

    # --- Lógica de Cache (ajustada para a classe) ---
    def salvar_cache(self, estatisticas: Dict[str, Any], caminho: str = ARQUIVO_CACHE_ESTATISTICAS):
        """Salva as estatísticas calculadas em um arquivo JSON."""
        try:
            stats_serializaveis = {k: dict(v) if isinstance(v, Counter) else v for k, v in estatisticas.items()}
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(stats_serializaveis, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar as estatísticas: {e}")

    def carregar_cache(self, caminho: str = ARQUIVO_CACHE_ESTATISTICAS) -> Dict[str, Any]:
        """Carrega as estatísticas de um arquivo JSON."""
        if not os.path.exists(caminho):
            return None
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            for k, v in stats.items():
                if isinstance(v, dict):
                    stats[k] = Counter(v)
            return stats
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Erro ao carregar o arquivo de estatísticas: {e}")
            return None
