# lib/despachante.py

import os
import sys
import importlib
from typing import Dict, Any, List, Tuple, Set

# Adiciona o diretório-pai (raiz do projeto) ao caminho
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib import dados

class Despachante:
    """
    Gerencia o carregamento dinâmico de todas as heurísticas e orquestra
    o cálculo de estatísticas e a geração de previsões.
    """
    def __init__(self, pasta_heuristicas: str = 'heuristicas'):
        self.pasta_heuristicas = os.path.join(PROJECT_ROOT, 'lib', pasta_heuristicas)
        self.heuristics: Dict[str, Any] = {}
        self.dependencias: Dict[str, Set[str]] = {}
        self._carregar_heuristicas()

    def _carregar_heuristicas(self):
        """
        Carrega todas as classes de heurísticas da pasta especificada.
        """
        if not os.path.exists(self.pasta_heuristicas):
            print(f"Erro: Pasta '{self.pasta_heuristicas}' não encontrada.")
            return

        for file_name in os.listdir(self.pasta_heuristicas):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                try:
                    module = importlib.import_module(f'lib.heuristicas.{module_name}')
                    # Espera que a classe da heurística tenha o mesmo nome do ficheiro (com a primeira letra maiúscula)
                    heuristic_class = getattr(module, module_name.capitalize())
                    instance = heuristic_class()
                    
                    self.heuristics[module_name] = instance
                    # Puxa as dependências diretamente do atributo de classe
                    self.dependencias[module_name] = set(getattr(instance, 'DEPENDENCIAS', []))
                except (AttributeError, ImportError) as e:
                    print(f"Aviso: Não foi possível carregar a heurística '{module_name}'. Detalhes: {e}")

    def get_todas_dependencias(self) -> Set[str]:
        """Retorna um conjunto com todas as dependências necessárias de todas as heurísticas carregadas."""
        all_dependencies = set()
        for deps in self.dependencias.values():
            all_dependencies.update(deps)
        return all_dependencies

    def get_previsoes(self, sorteios_historico: list) -> Dict[str, Any]:
        """
        Calcula as estatísticas necessárias e gera as previsões para todas as heurísticas.
        Retorna as previsões e os logs de erros.
        """
        deps_necessarias = self.get_todas_dependencias()
        estatisticas_completas, erros_estatisticas = dados.obter_estatisticas(deps_necessarias, sorteios_historico)

        previsoes = {}
        erros_heuristicas = []

        for nome_heuristica, heuristica_obj in self.heuristics.items():
            try:
                deps = self.dependencias.get(nome_heuristica, set())
                dados_para_heuristica = {key: estatisticas_completas[key] for key in deps if key in estatisticas_completas}

                if len(deps) != len(dados_para_heuristica):
                    erros_heuristicas.append(f"Dependências incompletas para '{nome_heuristica}'. A retornar lista vazia.")
                    previsoes[nome_heuristica] = []
                    continue

                previsao = heuristica_obj.prever(**dados_para_heuristica)
                previsoes[nome_heuristica] = previsao
            except Exception as e:
                erros_heuristicas.append(f"Erro ao executar a heurística '{nome_heuristica}': {e}.")
                previsoes[nome_heuristica] = []
        
        return {
            "previsoes": previsoes,
            "logs": {
                "erros_estatisticas": erros_estatisticas,
                "erros_heuristicas": erros_heuristicas
            }
        }
