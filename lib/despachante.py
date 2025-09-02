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
        # Caminho da pasta de heurísticas corrigido
        self.pasta_heuristicas = os.path.join(PROJECT_ROOT, pasta_heuristicas)
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

        # A CORREÇÃO PRINCIPAL: Adiciona a pasta de heurísticas ao sys.path
        # para que o Python a reconheça como um local para procurar módulos.
        sys.path.insert(0, self.pasta_heuristicas)

        for file_name in os.listdir(self.pasta_heuristicas):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                try:
                    # Altera a importação para usar apenas o nome do módulo.
                    # O Python agora pode encontrá-lo porque o caminho da pasta
                    # já foi adicionado ao sys.path.
                    module = importlib.import_module(module_name)
                    
                    # Espera que a classe da heurística tenha o mesmo nome do ficheiro (com a primeira letra maiúscula)
                    heuristic_class = getattr(module, module_name.capitalize())
                    instance = heuristic_class()
                    
                    self.heuristics[module_name] = instance
                    self.dependencias[module_name] = set(getattr(instance, 'DEPENDENCIAS', []))
                except (AttributeError, ImportError) as e:
                    print(f"Aviso: Não foi possível carregar a heurística '{module_name}'. Detalhes: {e}")
        
        # É crucial remover o caminho temporário para evitar conflitos futuros
        sys.path.pop(0)

# ... (resto do código) ...
