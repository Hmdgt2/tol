# lib/despachante.py

import os
import sys
import importlib
from typing import Dict, Any, List, Set
import json
import datetime

# Adiciona o diretório-pai (raiz do projeto) ao caminho para garantir que as importações funcionem
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# NOVO: Importar o gerador de heurísticas dinâmicas
try:
    from lib.gerador_heuristicas_dinamicas import GeradorHeuristicasDinamicas, HeuristicaDinamica
    GERADOR_DISPONIVEL = True
except ImportError as e:
    print(f"⚠️  GeradorHeuristicasDinamicas não disponível: {e}")
    GERADOR_DISPONIVEL = False
    # Criar classes dummy para evitar erros
    class HeuristicaDinamica:
        def __init__(self, *args, **kwargs):
            pass
    class GeradorHeuristicasDinamicas:
        def __init__(self, *args, **kwargs):
            self.heuristicas_ativas = {}
            self.historico_desempenho = []

class Despachante:
    """
    Gerencia o carregamento dinâmico de todas as heurísticas (fixas + dinâmicas)
    e orquestra o cálculo de estatísticas e a geração de previsões.
    """
    
    def __init__(self, pasta_heuristicas: str = 'heuristicas', usar_dinamicas: bool = True):
        self.pasta_heuristicas = os.path.join(PROJECT_ROOT, pasta_heuristicas)
        self.heuristicas: Dict[str, Any] = {}
        self.metadados: Dict[str, Dict[str, Any]] = {}
        
        # NOVO: Sistema de heurísticas dinâmicas
        self.usar_dinamicas = usar_dinamicas and GERADOR_DISPONIVEL
        self.gerador_dinamicas = GeradorHeuristicasDinamicas() if self.usar_dinamicas else None
        self.heuristicas_dinamicas: Dict[str, Any] = {}
        
        # NOVO: Configurações
        self.num_heuristicas_dinamicas = 20
        self.auto_otimizar = True
        
        # NOVO: Histórico de desempenho
        self.historico_desempenho = []
        self.ultima_avaliacao = None
        
        print("🎯 Inicializando Despachante...")
        self._carregar_heuristicas_fixas()
        
        if self.usar_dinamicas:
            self._carregar_heuristicas_dinamicas()
        else:
            print("🔧 Heurísticas dinâmicas desativadas")

    def _carregar_heuristicas_fixas(self):
        """
        Carrega todas as classes de heurísticas FIXAS da pasta especificada.
        """
        if not os.path.exists(self.pasta_heuristicas):
            print(f"❌ Erro: Pasta '{self.pasta_heuristicas}' não encontrada.")
            return

        sys.path.insert(0, self.pasta_heuristicas)

        heuristicas_carregadas = 0
        for file_name in os.listdir(self.pasta_heuristicas):
            if file_name.endswith('.py') and file_name != '__init__.py':
                module_name = file_name[:-3]
                try:
                    module = importlib.import_module(module_name)
                    
                    # Procura dinamicamente pela classe correta no módulo
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and obj.__module__ == module.__name__ and name[0].isupper():
                            heuristica_classe = obj
                            instance = heuristica_classe()
                            nome_heuristica = getattr(instance, 'NOME', module_name)
                            
                            # Verificar se a heurística tem o método prever
                            if not hasattr(instance, 'prever'):
                                print(f"⚠️  Heurística '{nome_heuristica}' não tem método 'prever'. Ignorando.")
                                continue
                            
                            self.heuristicas[nome_heuristica] = instance
                            self.metadados[nome_heuristica] = {
                                'descricao': getattr(instance, 'DESCRICAO', 'N/A'),
                                'dependencias': getattr(instance, 'DEPENDENCIAS', []),
                                'modulo': module_name,
                                'funcao': 'prever',
                                'tipo': 'fixa',  # NOVO: identificar tipo
                                'data_carregamento': datetime.datetime.now().isoformat()
                            }
                            heuristicas_carregadas += 1
                            print(f"✅ Heurística FIXA '{nome_heuristica}' carregada com sucesso.")
                            break
                    else:
                        print(f"⚠️  Nenhuma classe válida encontrada em {module_name}")
                    
                except Exception as e:
                    print(f"❌ Erro ao carregar a heurística fixa '{module_name}'. Detalhes: {e}")
        
        sys.path.pop(0)
        print(f"📦 Total de heurísticas fixas carregadas: {heuristicas_carregadas}")

    def _carregar_heuristicas_dinamicas(self, quantidade: int = None):
        """
        Carrega heurísticas dinâmicas geradas automaticamente
        """
        if not self.gerador_dinamicas:
            print("❌ Gerador de heurísticas dinâmicas não disponível")
            return
            
        print("🔄 Carregando heurísticas dinâmicas...")
        
        # Usar quantidade padrão se não especificada
        if quantidade is None:
            quantidade = self.num_heuristicas_dinamicas
        
        # Gerar heurísticas dinâmicas
        heuristicas_dinamicas = self.gerador_dinamicas.gerar_heuristicas_para_loteria(quantidade)
        
        for nome, heuristica in heuristicas_dinamicas.items():
            self.heuristicas[nome] = heuristica
            self.heuristicas_dinamicas[nome] = heuristica
            
            self.metadados[nome] = {
                'descricao': heuristica.DESCRICAO,
                'dependencias': heuristica.DEPENDENCIAS,
                'modulo': 'gerador_dinamico',
                'funcao': 'prever',
                'tipo': 'dinamica',  # NOVO: identificar tipo
                'logica': heuristica.logica,  # NOVO: salvar a lógica usada
                'data_carregamento': datetime.datetime.now().isoformat(),
                'versao': '1.0'
            }
            
            print(f"✅ Heurística DINÂMICA '{nome}' carregada com sucesso.")
        
        print(f"📦 Total de heurísticas dinâmicas carregadas: {len(heuristicas_dinamicas)}")

    def obter_metadados(self) -> Dict[str, Dict[str, Any]]:
        """
        Retorna os metadados de todas as heurísticas carregadas.
        """
        return self.metadados

    def obter_todas_dependencias(self) -> Set[str]:
        """
        Retorna um conjunto com todas as dependências de todas as heurísticas.
        """
        todas_dependencias = set()
        for meta in self.metadados.values():
            todas_dependencias.update(meta['dependencias'])
        return todas_dependencias

    def get_previsoes(self, estatisticas: Dict[str, Any], n: int = 5) -> Dict[str, List[int]]:
        """
        Gera previsões para todas as heurísticas carregadas (fixas + dinâmicas).
        """
        previsoes = {}
        previsoes_sucesso = 0
        previsoes_falha = 0
        
        print(f"🔍 Gerando previsões para {len(self.heuristicas)} heurísticas...")
        
        for nome, heuristica in self.heuristicas.items():
            try:
                resultado = heuristica.prever(estatisticas, n)
                
                # Validar resultado
                if (isinstance(resultado, list) and 
                    len(resultado) == n and 
                    all(isinstance(x, int) and 1 <= x <= 49 for x in resultado)):
                    
                    previsoes[nome] = resultado
                    previsoes_sucesso += 1
                else:
                    print(f"⚠️  Previsão inválida de '{nome}': {resultado}")
                    previsoes_falha += 1
                    
            except Exception as e:
                print(f"❌ Erro ao gerar previsão para a heurística '{nome}': {e}")
                previsoes_falha += 1
        
        print(f"📊 Previsões: {previsoes_sucesso} sucesso, {previsoes_falha} falha")
        return previsoes

    # ==================== NOVOS MÉTODOS PARA HEURÍSTICAS DINÂMICAS ====================

    def reavaliar_heuristicas_dinamicas(self, dados_manager, forcar_reatreinamento: bool = False):
        """
        Reavalia e otimiza as heurísticas dinâmicas baseado em desempenho
        
        Args:
            dados_manager: Instância da classe Dados com dados históricos
            forcar_reatreinamento: Força reavaliação mesmo se já foi feita recentemente
        """
        if not self.gerador_dinamicas:
            print("❌ Gerador de heurísticas dinâmicas não disponível para reavaliação")
            return False
            
        # Verificar se precisa reavaliar (evitar reavaliação muito frequente)
        if (not forcar_reatreinamento and 
            self.ultima_avaliacao and 
            (datetime.datetime.now() - self.ultima_avaliacao).days < 1):
            print("🔍 Reavaliação recente detectada, pulando...")
            return True

        print("🔄 Reavaliando heurísticas dinâmicas...")
        
        try:
            # Avaliar desempenho atual
            ranking = self.gerador_dinamicas.avaliar_desempenho_heuristicas(dados_manager)
            self.historico_desempenho = ranking
            self.ultima_avaliacao = datetime.datetime.now()
            
            if not ranking:
                print("⚠️  Nenhum resultado de avaliação obtido")
                return False
            
            # Manter apenas as melhores heurísticas
            melhores = self.gerador_dinamicas.obter_melhores_heuristicas(top_n=15)
            
            print(f"🏆 Selecionando {len(melhores)} melhores heurísticas dinâmicas...")
            
            # Remover heurísticas dinâmicas antigas
            heuristicas_removidas = 0
            for nome in list(self.heuristicas_dinamicas.keys()):
                if nome in self.heuristicas:
                    del self.heuristicas[nome]
                    heuristicas_removidas += 1
                if nome in self.metadados:
                    del self.metadados[nome]
            
            # Adicionar melhores heurísticas
            heuristicas_adicionadas = 0
            for nome, heuristica in melhores.items():
                self.heuristicas[nome] = heuristica
                self.heuristicas_dinamicas[nome] = heuristica
                
                # Atualizar metadados com informações de desempenho
                desempenho_info = next((h for h in ranking if h['nome'] == nome), {})
                
                self.metadados[nome] = {
                    'descricao': heuristica.DESCRICAO,
                    'dependencias': heuristica.DEPENDENCIAS,
                    'modulo': 'gerador_dinamico_otimizado',
                    'funcao': 'prever',
                    'tipo': 'dinamica_otimizada',
                    'logica': heuristica.logica,
                    'data_otimizacao': datetime.datetime.now().isoformat(),
                    'versao': '2.0',
                    'desempenho': {
                        'score': desempenho_info.get('score', 0),
                        'taxa_acerto': desempenho_info.get('taxa_acerto', 0),
                        'estabilidade': desempenho_info.get('estabilidade', 0),
                        'posicao_ranking': next((i for i, h in enumerate(ranking) if h['nome'] == nome), -1) + 1
                    }
                }
                heuristicas_adicionadas += 1
            
            print(f"✅ {heuristicas_adicionadas} heurísticas dinâmicas otimizadas carregadas "
                  f"(removidas {heuristicas_removidas} antigas)")
            
            # Salvar histórico de otimização
            self._salvar_historico_otimizacao(ranking)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante reavaliação: {e}")
            return False

    def _salvar_historico_otimizacao(self, ranking: List[Dict]):
        """
        Salva histórico das otimizações para análise
        """
        try:
            historico_path = os.path.join(PROJECT_ROOT, 'decisor', 'historico_otimizacao.json')
            os.makedirs(os.path.dirname(historico_path), exist_ok=True)
            
            historico_entry = {
                'data': datetime.datetime.now().isoformat(),
                'total_heuristicas_avaliadas': len(ranking),
                'melhores_5': ranking[:5],
                'estatisticas_gerais': {
                    'score_medio': np.mean([h['score'] for h in ranking]) if ranking else 0,
                    'score_maximo': max([h['score'] for h in ranking]) if ranking else 0,
                    'score_minimo': min([h['score'] for h in ranking]) if ranking else 0,
                }
            }
            
            # Carregar histórico existente ou criar novo
            if os.path.exists(historico_path):
                with open(historico_path, 'r', encoding='utf-8') as f:
                    historico_completo = json.load(f)
            else:
                historico_completo = []
            
            historico_completo.append(historico_entry)
            
            # Manter apenas as últimas 50 entradas
            if len(historico_completo) > 50:
                historico_completo = historico_completo[-50:]
            
            with open(historico_path, 'w', encoding='utf-8') as f:
                json.dump(historico_completo, f, indent=2, ensure_ascii=False)
                
            print(f"💾 Histórico de otimização salvo em {historico_path}")
            
        except Exception as e:
            print(f"⚠️  Erro ao salvar histórico: {e}")

    def obter_estatisticas_heuristicas(self) -> Dict[str, Any]:
        """
        Retorna estatísticas detalhadas sobre as heurísticas carregadas
        """
        heuristicas_fixas = [m for m in self.metadados.values() if m.get('tipo') == 'fixa']
        heuristicas_dinamicas = [m for m in self.metadados.values() if m.get('tipo', '').startswith('dinamica')]
        
        # Calcular estatísticas de desempenho para dinâmicas
        melhores_dinamicas = []
        if self.historico_desempenho:
            melhores_dinamicas = [h['nome'] for h in self.historico_desempenho[:5]]
        
        # Análise de dependências
        todas_dependencias = self.obter_todas_dependencias()
        dependencias_mais_usadas = {}
        for meta in self.metadados.values():
            for dep in meta.get('dependencias', []):
                dependencias_mais_usadas[dep] = dependencias_mais_usadas.get(dep, 0) + 1
        
        return {
            'total_heuristicas': len(self.heuristicas),
            'heuristicas_fixas': len(heuristicas_fixas),
            'heuristicas_dinamicas': len(heuristicas_dinamicas),
            'dependencias_unicas': len(todas_dependencias),
            'melhores_dinamicas': melhores_dinamicas,
            'dependencias_mais_usadas': sorted(
                dependencias_mais_usadas.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10],
            'ultima_avaliacao': self.ultima_avaliacao.isoformat() if self.ultima_avaliacao else None,
            'usando_dinamicas': self.usar_dinamicas,
            'gerador_disponivel': GERADOR_DISPONIVEL
        }

    def obter_relatorio_detalhado(self) -> Dict[str, Any]:
        """
        Retorna um relatório completo do sistema
        """
        estatisticas = self.obter_estatisticas_heuristicas()
        
        relatorio = {
            'estatisticas_gerais': estatisticas,
            'heuristicas_por_tipo': {},
            'dependencias_completas': list(self.obter_todas_dependencias()),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Agrupar heurísticas por tipo
        for nome, meta in self.metadados.items():
            tipo = meta.get('tipo', 'desconhecido')
            if tipo not in relatorio['heuristicas_por_tipo']:
                relatorio['heuristicas_por_tipo'][tipo] = []
            
            relatorio['heuristicas_por_tipo'][tipo].append({
                'nome': nome,
                'descricao': meta.get('descricao', ''),
                'dependencias': meta.get('dependencias', []),
                'modulo': meta.get('modulo', '')
            })
        
        return relatorio

    def exportar_configuracao(self, caminho: str = None):
        """
        Exporta a configuração atual do despachante para arquivo JSON
        """
        if caminho is None:
            caminho = os.path.join(PROJECT_ROOT, 'decisor', 'configuracao_despachante.json')
        
        try:
            config = {
                'relatorio': self.obter_relatorio_detalhado(),
                'metadados_completos': self.metadados,
                'configuracoes': {
                    'usar_dinamicas': self.usar_dinamicas,
                    'num_heuristicas_dinamicas': self.num_heuristicas_dinamicas,
                    'auto_otimizar': self.auto_otimizar
                }
            }
            
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Configuração exportada para: {caminho}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao exportar configuração: {e}")
            return False

    def limpar_heuristicas_dinamicas(self):
        """
        Remove todas as heurísticas dinâmicas atuais
        """
        if not self.heuristicas_dinamicas:
            print("ℹ️  Nenhuma heurística dinâmica para limpar")
            return
        
        removidas = 0
        for nome in list(self.heuristicas_dinamicas.keys()):
            if nome in self.heuristicas:
                del self.heuristicas[nome]
            if nome in self.metadados:
                del self.metadados[nome]
            removidas += 1
        
        self.heuristicas_dinamicas.clear()
        print(f"🗑️  {removidas} heurísticas dinâmicas removidas")

    def recarregar_heuristicas(self, incluir_dinamicas: bool = True):
        """
        Recarrega todas as heurísticas (fixas e dinâmicas)
        """
        print("🔄 Recarregando todas as heurísticas...")
        
        # Limpar estado atual
        self.heuristicas.clear()
        self.metadados.clear()
        self.heuristicas_dinamicas.clear()
        
        # Recarregar
        self._carregar_heuristicas_fixas()
        
        if incluir_dinamicas and self.usar_dinamicas:
            self._carregar_heuristicas_dinamicas()
        
        print("✅ Recarregamento completo concluído")


# Função de utilidade para uso rápido
def criar_despachante_otimizado() -> Despachante:
    """
    Cria um despachante pré-otimizado com heurísticas dinâmicas
    """
    print("🚀 Criando despachante otimizado...")
    despachante = Despachante(usar_dinamicas=True)
    
    # Tentar otimização inicial se houver dados
    try:
        from lib.dados import Dados
        dados_manager = Dados()
        if dados_manager.sorteios and len(dados_manager.sorteios) > 10:
            despachante.reavaliar_heuristicas_dinamicas(dados_manager)
    except Exception as e:
        print(f"⚠️  Otimização inicial não realizada: {e}")
    
    return despachante


if __name__ == '__main__':
    # Teste básico do despachante
    despachante = criar_despachante_otimizado()
    
    # Mostrar estatísticas
    stats = despachante.obter_estatisticas_heuristicas()
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS DO DESPACHANTE:")
    print(f"   Total heurísticas: {stats['total_heuristicas']}")
    print(f"   Fixas: {stats['heuristicas_fixas']}")
    print(f"   Dinâmicas: {stats['heuristicas_dinamicas']}")
    print(f"   Dependências únicas: {stats['dependencias_unicas']}")
    
    if stats['melhores_dinamicas']:
        print(f"   🏆 Melhores dinâmicas: {', '.join(stats['melhores_dinamicas'])}")
