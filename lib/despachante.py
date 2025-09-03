import os
import sys
import importlib
from typing import Dict, Any, List, Set

# Adiciona o diretório-pai (raiz do projeto) ao caminho para garantir que as importações funcionem
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class Despachante:
    """
    Gerencia o carregamento dinâmico de todas as heurísticas e orquestra
    o cálculo de estatísticas e a geração de previsões.
    """
    def __init__(self, pasta_heuristicas: str = 'heuristicas'):
        self.pasta_heuristicas = os.path.join(PROJECT_ROOT, pasta_heuristicas)
        self.heuristicas: Dict[str, Any] = {}
        self.metadados: Dict[str, Dict[str, Any]] = {}
        self._cache_previsoes: Dict[frozenset, Any] = {}
        self._carregar_heuristicas()

    def _carregar_heuristicas(self):
        """
        Carrega todas as classes de heurísticas da pasta especificada.
        """
        if not os.path.exists(self.pasta_heuristicas):
            print(f"Erro: Pasta '{self.pasta_heuristicas}' não encontrada.")
            return

        sys.path.insert(0, self.pasta_heuristicas)

        for file_name in os.listdir(self.pasta_heuristicas):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                try:
                    module = importlib.import_module(module_name)
                    
                    # Procura dinamicamente pela classe correta no módulo
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and obj.__module__ == module.__name__ and name[0].isupper():
                            instance = obj()
                            nome_heuristica = getattr(instance, 'NOME', module_name)
                            
                            self.heuristicas[nome_heuristica] = instance
                            self.metadados[nome_heuristica] = {
                                'descricao': getattr(instance, 'DESCRICAO', 'N/A'),
                                'dependencias': getattr(instance, 'DEPENDENCIAS', []),
                                'modulo': module_name,
                                'funcao': 'prever'
                            }
                            print(f"✅ Heurística '{nome_heuristica}' carregada com sucesso.")
                            break
                except Exception as e:
                    print(f"❌ Erro ao carregar a heurística '{module_name}': {e}")
        
        sys.path.pop(0)
        print(f"✅ Total de heurísticas carregadas: {len(self.heuristicas)}")

    def obter_metadados(self) -> Dict[str, Dict[str, Any]]:
        """Retorna os metadados de todas as heurísticas carregadas."""
        return self.metadados

    def obter_todas_dependencias(self) -> Set[str]:
        """Retorna um conjunto com todas as dependências de todas as heurísticas."""
        todas_dependencias = set()
        for meta in self.metadados.values():
            todas_dependencias.update(meta['dependencias'])
        return todas_dependencias

    def get_previsoes(self, estatisticas: Dict[str, Any], n: int = 5) -> Dict[str, List[int]]:
        """
        Gera previsões para todas as heurísticas carregadas.
        Filtra automaticamente as estatísticas por dependência.
        Utiliza cache interno para otimizar chamadas repetidas.
        """
        previsoes = {}
        for nome, heuristica in self.heuristicas.items():
            deps = set(self.metadados[nome]['dependencias'])
            stats_filtradas = {k: estatisticas[k] for k in deps if k in estatisticas}
            key = frozenset(stats_filtradas.items())

            if key in self._cache_previsoes:
                previsoes[nome] = self._cache_previsoes[key]
                continue

            try:
                resultado = heuristica.prever(stats_filtradas, n)
                previsoes[nome] = resultado
                self._cache_previsoes[key] = resultado
            except Exception as e:
                print(f"❌ Erro ao gerar previsão para a heurística '{nome}': {e}")
                previsoes[nome] = []

        return previsoes
