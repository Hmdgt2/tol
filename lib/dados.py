import os
import sys
import json
from collections import Counter, defaultdict
from itertools import combinations
import datetime
import numpy as np
import inspect
from typing import Dict, Any, List, Tuple

# --- Configurações do projeto ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

PASTA_DADOS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dados'))
ARQUIVO_CACHE_ESTATISTICAS = os.path.join(PASTA_DADOS, 'estatisticas_cache.json')


class Dados:
    """
    Classe central para carregar sorteios, calcular estatísticas e fornecer dados
    para o pipeline de heurísticas.
    """
    def __init__(self, caminho_dados: str = PASTA_DADOS):
        self.caminho_dados = caminho_dados
        self.sorteios = self._carregar_sorteios()
        self.mapeamento_calculos = self._get_mapeamento_calculos()
        self._estatisticas_cache = {}

    # ------------------ CARREGAMENTO DE DADOS ------------------
    def _carregar_sorteios(self) -> List[Dict[str, Any]]:
        """Carrega todos os sorteios do diretório, ordenados por data."""
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
                    print(f"Erro ao ler {nome_arquivo}: {e}")

        sorteios_validos = [s for s in todos if isinstance(s, dict) and 'data' in s and 'numeros' in s]
        sorteios_validos.sort(key=lambda s: datetime.datetime.strptime(s['data'], '%d/%m/%Y'))
        return sorteios_validos

    # ------------------ UTILITÁRIOS ------------------
    def _is_prime(self, n: int) -> bool:
        """Verifica se um número é primo."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _calcular_frequencia_combinacoes(self, tamanho: int, janela: int = None) -> Counter:
        """Calcula frequência de combinações de tamanho N, opcionalmente limitada a uma janela."""
        sorteios_para_analisar = self.sorteios[-janela:] if janela else self.sorteios
        frequencia = Counter()
        for sorteio in sorteios_para_analisar:
            if sorteio.get('numeros'):
                frequencia.update(combinations(sorted(sorteio['numeros']), tamanho))
        return frequencia

    # ------------------ FUNÇÕES DE CÁLCULO DE ESTATÍSTICAS ------------------
    def _calcular_frequencia_total(self) -> Counter:
        return Counter(num for s in self.sorteios for num in s['numeros'])

    def _calcular_ausencia_atual(self) -> Dict[int, int]:
        todos_numeros = set(range(1, 50))
        ultima_ocorrencia = {num: -1 for num in todos_numeros}
        for i, s in enumerate(self.sorteios):
            for num in s['numeros']:
                ultima_ocorrencia[num] = i
        total = len(self.sorteios)
        return {num: total - ultima_ocorrencia[num] - 1 for num in todos_numeros}

    def _calcular_gaps_medios(self) -> Dict[int, float]:
        posicoes = defaultdict(list)
        for i, s in enumerate(self.sorteios):
            for num in s['numeros']:
                posicoes[num].append(i)
        gaps = {}
        for num in range(1, 50):
            concursos = posicoes.get(num, [])
            if len(concursos) < 2:
                gaps[num] = float('inf')
            else:
                gaps[num] = np.mean([j - i for i, j in zip(concursos[:-1], concursos[1:])])
        return gaps

    def _calcular_frequencia_pares(self) -> Counter:
        return self._calcular_frequencia_combinacoes(2)

    def _calcular_frequencia_trios(self) -> Counter:
        return self._calcular_frequencia_combinacoes(3)

    def _calcular_frequencia_grupos(self) -> Counter:
        freq = Counter()
        for i in range(2, 5):
            freq.update(self._calcular_frequencia_combinacoes(i))
        return freq

    def _calcular_frequencia_recente(self, janela=15) -> Counter:
        return self._calcular_frequencia_combinacoes(1, janela=janela)

    def _calcular_frequencia_por_posicao(self) -> Dict[int, Counter]:
        freq = defaultdict(Counter)
        if not self.sorteios or not self.sorteios[0]['numeros']:
            return freq
        for s in self.sorteios:
            numeros = sorted(s['numeros'])
            for i, num in enumerate(numeros):
                freq[i][num] += 1
        return freq

    def _calcular_frequencia_terminacoes_padrao(self) -> Dict[int, Counter]:
        padrao = defaultdict(Counter)
        for i in range(len(self.sorteios) - 1):
            nums_atual = sorted(self.sorteios[i]['numeros'])
            nums_seguinte = sorted(self.sorteios[i+1]['numeros'])
            for term_atual in {n % 10 for n in nums_atual}:
                padrao[term_atual].update({n % 10 for n in nums_seguinte})
        return padrao

    def _calcular_numeros_soma_mais_frequente(self) -> List[int]:
        somas = [sum(s['numeros']) for s in self.sorteios]
        if not somas:
            return []
        media, desvio = np.mean(somas), np.std(somas)
        min_soma, max_soma = int(media - desvio), int(media + desvio)
        freq = Counter()
        for s in self.sorteios:
            total = sum(s['numeros'])
            if min_soma <= total <= max_soma:
                freq.update(s['numeros'])
        return [k for k, _ in freq.most_common()]

    def _calcular_padrao_tipos_numeros(self) -> Tuple[int, int, int]:
        padroes = Counter()
        for s in self.sorteios:
            nums = s['numeros']
            padroes.update([(sum(n % 2 == 0 for n in nums),
                             sum(n % 2 != 0 for n in nums),
                             sum(self._is_prime(n) for n in nums))])
        return padroes.most_common(1)[0][0] if padroes else (0, 0, 0)

    def _calcular_distribuicao_quadrantes(self) -> Dict[int, int]:
        dist = defaultdict(int)
        for s in self.sorteios:
            for n in s['numeros']:
                if n <= 12: dist[1] += 1
                elif n <= 24: dist[2] += 1
                elif n <= 36: dist[3] += 1
                else: dist[4] += 1
        return dist

    def _calcular_frequencia_vizinhos(self) -> Dict[int, int]:
        freq = defaultdict(int)
        for s in self.sorteios:
            nums = set(s['numeros'])
            for n in nums:
                if n-1 in nums or n+1 in nums:
                    freq[n] += 1
        return freq

    def _calcular_pares_recentes(self) -> Counter:
        return self._calcular_frequencia_combinacoes(2, janela=20)

    def _calcular_frequencia_pares_consecutivos(self) -> Counter:
        freq = Counter()
        for s in self.sorteios:
            nums = sorted(s['numeros'])
            for i in range(len(nums)-1):
                if nums[i+1] == nums[i]+1:
                    freq[(nums[i], nums[i+1])] += 1
        return freq

    def _calcular_precisao_posicional_historica(self) -> Dict[int, float]:
        precisao = defaultdict(list)
        if not self.sorteios:
            return {}
        num_pos = len(self.sorteios[0]['numeros'])
        medias = [np.mean([s['numeros'][i] for s in self.sorteios]) for i in range(num_pos)]
        for s in self.sorteios:
            for i, n in enumerate(s['numeros']):
                precisao[i].append(abs(n - medias[i]))
        return {k: np.mean(v) for k, v in precisao.items()}

    def _calcular_frequencia_por_ano(self) -> Dict[int, Counter]:
        freq = defaultdict(Counter)
        for s in self.sorteios:
            ano = datetime.datetime.strptime(s['data'], '%d/%m/%Y').year
            freq[ano].update(s['numeros'])
        return freq

    def _calcular_distribuicao_dezenas(self) -> Dict[int, int]:
        dist = defaultdict(int)
        for s in self.sorteios:
            for n in s['numeros']:
                dist[n//10] += 1
        return dist

    def _calcular_probabilidades_repeticoes(self) -> Dict[int, float]:
        probs = defaultdict(float)
        if len(self.sorteios) < 2:
            return probs
        ocorrencias = defaultdict(int)
        freq_total = self._calcular_frequencia_total()
        for i in range(1, len(self.sorteios)):
            repetidos = set(self.sorteios[i-1]['numeros']).intersection(self.sorteios[i]['numeros'])
            for n in repetidos:
                ocorrencias[n] += 1
        for n, count in ocorrencias.items():
            probs[n] = count / freq_total[n] if freq_total[n] else 0
        return probs

    # ------------------ MAPEAR FUNÇÕES ------------------
    def _get_mapeamento_calculos(self) -> Dict[str, callable]:
        return {name.replace('_calcular_', ''): func
                for name, func in inspect.getmembers(self, predicate=inspect.ismethod)
                if name.startswith('_calcular_')}

    # ------------------ INTERFACE PARA PIPELINE ------------------
    def obter_estatisticas(self, dependencias: set) -> Tuple[Dict[str, Any], List[str]]:
        stats, erros = {}, []
        for dep in dependencias:
            if dep in self.mapeamento_calculos:
                try:
                    stats[dep] = self.mapeamento_calculos[dep]()
                except Exception as e:
                    stats[dep] = {}
                    erros.append(f"Erro em '{dep}': {e}")
            else:
                stats[dep] = {}
                erros.append(f"Função '{dep}' não encontrada.")
        return stats, erros

    def obter_resumo_calculos_com_metadados(self) -> Dict[str, Dict[str, Any]]:
        mapeamento_logica = {
            'frequencia_total': ['frequencia', 'geral', 'total'],
            'ausencia_atual': ['ausencia', 'atraso', 'tempo'],
            'gaps_medios': ['gaps', 'intervalo', 'distancia'],
            'frequencia_pares': ['pares', 'duplas', 'frequencia'],
            'frequencia_trios': ['trios', 'frequencia', 'grupos'],
            'frequencia_grupos': ['grupos', 'padroes'],
            'frequencia_recente': ['frequencia', 'recente', 'janela'],
            'frequencia_por_posicao': ['frequencia', 'posicao'],
            'frequencia_terminacoes_padrao': ['terminacoes', 'padrao', 'finais'],
            'numeros_soma_mais_frequente': ['soma', 'frequencia'],
            'padrao_tipos_numeros': ['pares', 'impares', 'primos', 'balanceamento'],
            'distribuicao_quadrantes': ['distribuicao', 'quadrantes', 'grupos'],
            'frequencia_vizinhos': ['vizinhos', 'proximidade'],
            'pares_recentes': ['pares', 'recente', 'duplas'],
            'frequencia_pares_consecutivos': ['consecutivos', 'pares', 'sequencia'],
            'precisao_posicional_historica': ['precisao', 'posicao'],
            'frequencia_por_ano': ['frequencia', 'anual', 'ano'],
            'distribuicao_dezenas': ['distribuicao', 'dezenas'],
            'trios_frequentes': ['trios', 'frequencia', 'grupos'],
            'probabilidades_repeticoes': ['probabilidade', 'repeticoes']
        }
        resumo = {}
        for name, func in self.mapeamento_calculos.items():
            resumo[name] = {
                'descricao': inspect.getdoc(func).strip() if inspect.getdoc(func) else "",
                'logica_principais': mapeamento_logica.get(name, [])
            }
        return resumo

    # ------------------ CACHE ------------------
    def salvar_cache(self, estatisticas: Dict[str, Any], caminho: str = ARQUIVO_CACHE_ESTATISTICAS):
        serializaveis = {k: dict(v) if isinstance(v, Counter) else v for k, v in estatisticas.items()}
        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(serializaveis, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")

    def carregar_cache(self, caminho: str = ARQUIVO_CACHE_ESTATISTICAS) -> Dict[str, Any]:
        if not os.path.exists(caminho):
            return {}
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            for k, v in stats.items():
                if isinstance(v, dict):
                    stats[k] = Counter(v)
            return stats
        except Exception as e:
            print(f"Erro ao carregar cache: {e}")
            return {}
