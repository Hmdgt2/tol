import os
import sys
import importlib.util
from typing import Dict, Any, List, Callable

# Adiciona o diretório-pai (raiz do projeto) ao caminho
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class Despachante:
    """
    Gerencia o carregamento dinâmico de todas as heurísticas e suas funções.
    Fornece uma interface para obter previsões e metadados.
    """
    def __init__(self, pasta_heuristicas: str = 'heuristicas'):
        self.pasta_heuristias = os.path.join(PROJECT_ROOT, pasta_heuristicas)
        self.heuristicas: Dict[str, Dict[str, Any]] = {}
        self._carregar_heuristicas()

    def _carregar_heuristicas(self):
        """
        Carrega todas as heurísticas da pasta especificada, extraindo metadados
        e a função de previsão 'prever'.
        """
        if not os.path.exists(self.pasta_heuristias):
            print(f"Erro: Pasta '{self.pasta_heuristias}' não encontrada.")
            return

        for nome_arquivo in os.listdir(self.pasta_heuristias):
            if nome_arquivo.endswith('.py') and not nome_arquivo.startswith('__'):
                nome_modulo = nome_arquivo[:-3]
                caminho_completo = os.path.join(self.pasta_heuristias, nome_arquivo)
                
                try:
                    spec = importlib.util.spec_from_file_location(nome_modulo, caminho_completo)
                    modulo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modulo)

                    # Verifica se o módulo tem as dependências necessárias
                    if hasattr(modulo, 'NOME') and hasattr(modulo, 'prever') and hasattr(modulo, 'DEPENDENCIAS'):
                        self.heuristicas[modulo.NOME] = {
                            'funcao_prever': modulo.prever,
                            'dependencias': set(modulo.DEPENDENCIAS),
                            'descricao': getattr(modulo, 'DESCRICAO', 'N/A')
                        }
                    else:
                        print(f"⚠️ Aviso: Arquivo '{nome_arquivo}' ignorado. Faltam atributos (NOME, prever, DEPENDENCIAS).")
                except Exception as e:
                    print(f"❌ Erro ao carregar a heurística '{nome_arquivo}': {e}")
    
    def get_previsoes(self, estatisticas: Dict[str, Any], n: int = 5) -> Dict[str, List[int]]:
        """
        Executa a função de previsão de cada heurística e retorna os resultados.
        """
        previsoes = {}
        for nome, dados in self.heuristicas.items():
            previsoes[nome] = dados['funcao_prever'](estatisticas, n)
        return previsoes
        
    def get_todas_dependencias(self) -> set:
        """
        Retorna um conjunto com todas as dependências necessárias para todas as heurísticas.
        """
        todas_dependencias = set()
        for dados in self.heuristicas.values():
            todas_dependencias.update(dados['dependencias'])
        return todas_dependencias

    def get_metadados(self) -> Dict[str, Any]:
        """
        Retorna os metadados de todas as heurísticas.
        """
        return {nome: {'descricao': h['descricao'], 'dependencias': list(h['dependencias'])} 
                for nome, h in self.heuristicas.items()}

if __name__ == '__main__':
    # Exemplo de como usar o Despachante
    despachante = Despachante()
    
    print("--- Heurísticas Carregadas ---")
    for nome, meta in despachante.get_metadados().items():
        print(f"📦 {nome}: {meta['descricao']} -> Dependências: {meta['dependencias']}")
        
    todas_deps = despachante.get_todas_dependencias()
    print(f"\n✅ Todas as dependências necessárias: {todas_deps}")
