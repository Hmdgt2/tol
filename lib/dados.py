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
            for i, num in enumerate(numeros):
                frequencia_posicao[i][num] += 1
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
        Calcula o intervalo de soma mais comum e retorna os números mais frequentes
        que saíram dentro desse intervalo.
        """
        somas = [sum(s['numeros']) for s in self.sorteios if s.get('numeros')]
        if not somas:
            return []
            
        soma_media = np.mean(somas)
        soma_desvio = np.std(somas)
        soma_minima = int(soma_media - soma_desvio)
        soma_maxima = int(soma_media + soma_desvio)
        
        frequencia_intervalo = Counter()
        for s in self.sorteios:
            if soma_minima <= sum(s.get('numeros', [])) <= soma_maxima:
                frequencia_intervalo.update(s['numeros'])
                
        return sorted(frequencia_intervalo.keys(), key=lambda k: frequencia_intervalo[k], reverse=True)

    def _calcular_padrao_tipos_numeros(self) -> Tuple[int, int, int]:
        """
        Calcula o padrão de balanceamento de pares, ímpares e primos mais frequente.
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
            
        if not padroes:
            return (0, 0, 0)
            
        return padroes.most_common(1)[0][0]

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
