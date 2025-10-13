# decisor_final.py
import joblib
import json
import os
import sys
import numpy as np
from typing import Dict, Any, List

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

class HeuristicDecisor:
    def __init__(self, caminho_base_decisor: str = None):
        """
        Inicializa o decisor, carregando todos os pipelines de ML para um ensemble.
        Agora compatível com heurísticas dinâmicas.

        Args:
            caminho_base_decisor (str): O caminho para a pasta 'decisor'. Se None, usa PROJECT_ROOT.
        """
        if caminho_base_decisor is None:
            caminho_base_decisor = PROJECT_ROOT
            
        self.modelos_dir = os.path.join(caminho_base_decisor, 'decisor', 'modelos_salvos')
        self.performance_path = os.path.join(self.modelos_dir, 'performance_modelos.json')
        self.metadados_path = os.path.join(caminho_base_decisor, 'decisor', 'metadados_modelo.json')
        self.pipelines: Dict[str, Any] = {}
        self.performance_data: Dict[str, Any] = {}
        self.heuristicas_ordenadas: List[str] = []
        self.metadados_completos: Dict[str, Any] = {}

        print("🎯 Inicializando HeuristicDecisor...")
        
        try:
            # 1. Carrega o ficheiro de performance de todos os modelos
            if not os.path.exists(self.performance_path):
                raise FileNotFoundError(f"Ficheiro de performance não encontrado: {self.performance_path}")
                
            with open(self.performance_path, 'r', encoding='utf-8') as f:
                self.performance_data = json.load(f)

            # 2. Carrega todos os pipelines salvos e suas pontuações de desempenho
            modelos_carregados = 0
            for modelo_nome, dados in self.performance_data.items():
                pipeline_path = dados['caminho']
                if os.path.exists(pipeline_path):
                    self.pipelines[modelo_nome] = joblib.load(pipeline_path)
                    modelos_carregados += 1
                    print(f"   ✅ {modelo_nome} (Score: {dados['score_treino']:.4f})")
                else:
                    print(f"   ⚠️ Pipeline não encontrado: {modelo_nome}")
            
            if not self.pipelines:
                raise RuntimeError("Nenhum pipeline de modelo de ML válido foi encontrado.")
                
            print(f"📦 Modelos carregados: {modelos_carregados}")

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise RuntimeError(f"Erro ao carregar os modelos. Detalhes: {e}")

        try:
            # 3. Carrega metadados atualizados (com heurísticas dinâmicas)
            if not os.path.exists(self.metadados_path):
                raise FileNotFoundError(f"Ficheiro de metadados não encontrado: {self.metadados_path}")
                
            with open(self.metadados_path, 'r', encoding='utf-8') as f:
                self.metadados_completos = json.load(f)

            # NOVO: Suporte à estrutura de metadados atualizada
            if 'heuristicas_ordenadas' in self.metadados_completos:
                self.heuristicas_ordenadas = self.metadados_completos['heuristicas_ordenadas']
            else:
                # Fallback para estrutura antiga
                self.heuristicas_ordenadas = self.metadados_completos.get('heuristicas_ordenadas', [])
                
            print(f"🔧 Heurísticas carregadas: {len(self.heuristicas_ordenadas)}")
            
            # NOVO: Estatísticas do sistema
            if 'estatisticas_sistema' in self.metadados_completos:
                stats = self.metadados_completos['estatisticas_sistema']
                print(f"📊 Sistema: {stats.get('total_heuristicas', 0)} heurísticas "
                      f"({stats.get('heuristicas_fixas', 0)}F + {stats.get('heuristicas_dinamicas', 0)}D)")

        except FileNotFoundError:
            raise FileNotFoundError(f"Ficheiro de metadados não encontrado em: {self.metadados_path}.")

    def _get_feature_vector(self, previsoes_atuais: Dict[str, List[int]]) -> np.ndarray:
        """
        Cria um array NumPy de características (features) para um único sorteio.
        ATUALIZADO: Agora aceita dicionário diretamente do despachante.
        
        Args:
            previsoes_atuais: Dicionário {nome_heuristica: [numeros_previstos]}
            
        Returns:
            np.ndarray: Array de características (49 × num_heuristicas)
        """
        feature_vectors = []
        
        for num in range(1, 50):
            # Vetor binário que indica se cada heurística sugeriu o número
            vector = [1 if num in previsoes_atuais.get(nome, []) else 0 for nome in self.heuristicas_ordenadas]
            feature_vectors.append(vector)
            
        return np.array(feature_vectors)

    def predict(self, previsoes_heurísticas: Dict[str, List[int]], n_resultados: int = 5) -> List[int]:
        """
        Faz a previsão usando o ensemble de modelos e retorna os N números mais prováveis.
        ATUALIZADO: Interface simplificada.
        
        Args:
            previsoes_heurísticas: Dicionário com previsões de todas as heurísticas
            n_resultados: Número de números a prever (padrão: 5)
            
        Returns:
            List[int]: Lista dos números mais prováveis
        """
        if not previsoes_heurísticas:
            raise ValueError("Dicionário de previsões vazio")
            
        if not self.heuristicas_ordenadas:
            raise RuntimeError("Lista de heurísticas não carregada")
            
        print(f"🔍 Gerando previsão com {len(self.pipelines)} modelos e {len(self.heuristicas_ordenadas)} heurísticas...")
        
        feature_vectors = self._get_feature_vector(previsoes_heurísticas)
        
        if feature_vectors.size == 0:
            return []
            
        probabilidades_combinadas = np.zeros(49)
        total_score = sum(d['score_treino'] for d in self.performance_data.values())
        
        if total_score == 0:
            raise RuntimeError("Scores dos modelos totais é zero")
        
        # 1. Obter as probabilidades de cada modelo e ponderá-las
        for nome_modelo, pipeline in self.pipelines.items():
            score = self.performance_data[nome_modelo]['score_treino']
            peso = score / total_score  # Peso proporcional ao score
            
            try:
                # O pipeline irá automaticamente normalizar os dados e fazer a previsão
                probabilidades = pipeline.predict_proba(feature_vectors)[:, 1]
                probabilidades_combinadas += probabilidades * peso
            except Exception as e:
                print(f"⚠️  Erro no modelo {nome_modelo}: {e}")
                continue
        
        # 2. Criar uma lista de tuplas (probabilidade, numero)
        probabilidades_por_numero = list(zip(probabilidades_combinadas, range(1, 50)))
        
        # 3. Ordenar e selecionar os números com maior probabilidade
        probabilidades_por_numero.sort(key=lambda x: x[0], reverse=True)
        
        previsao_final = [numero for prob, numero in probabilidades_por_numero[:n_resultados]]
        
        # NOVO: Informações de debug
        top5_probs = [f"{prob:.3f}" for prob, _ in probabilidades_por_numero[:5]]
        print(f"📊 Top 5 probabilidades: {', '.join(top5_probs)}")
        print(f"🎯 Previsão final: {previsao_final}")
        
        return previsao_final

    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        NOVO: Retorna estatísticas do decisor
        """
        return {
            'modelos_carregados': len(self.pipelines),
            'heuristicas_ativas': len(self.heuristicas_ordenadas),
            'performance_media': np.mean([d['score_treino'] for d in self.performance_data.values()]),
            'melhor_modelo': max(self.performance_data.items(), key=lambda x: x[1]['score_treino'])[0],
            'ultima_atualizacao': list(self.performance_data.values())[0]['ultima_atualizacao'] if self.performance_data else 'N/A',
            'configuracao': self.metadados_completos.get('configuracao', {})
        }


# NOVO: Função de conveniência para uso rápido
def criar_decisor_otimizado() -> HeuristicDecisor:
    """
    Cria um decisor pré-configurado e carregado
    """
    try:
        decisor = HeuristicDecisor()
        stats = decisor.obter_estatisticas()
        print(f"🚀 Decisor otimizado criado: {stats['modelos_carregados']} modelos, "
              f"{stats['heuristicas_ativas']} heurísticas")
        return decisor
    except Exception as e:
        print(f"❌ Erro ao criar decisor: {e}")
        raise


# NOVO: Exemplo de uso atualizado
def exemplo_uso():
    """
    Exemplo de como usar o decisor com o novo sistema
    """
    try:
        from lib.despachante import criar_despachante_otimizado
        from lib.dados import Dados
        
        # 1. Carregar dados e estatísticas
        dados = Dados()
        estatisticas, _ = dados.obter_estatisticas({'frequencia_total', 'frequencia_recente'})
        
        # 2. Obter previsões das heurísticas
        despachante = criar_despachante_otimizado()
        previsoes = despachante.get_previsoes(estatisticas, n=5)
        
        # 3. Usar decisor para previsão final
        decisor = criar_decisor_otimizado()
        previsao_final = decisor.predict(previsoes, n_resultados=5)
        
        print(f"🎯 Previsão do sistema: {previsao_final}")
        
        return previsao_final
        
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")
        return []


if __name__ == "__main__":
    # Teste do decisor
    try:
        decisor = criar_decisor_otimizado()
        stats = decisor.obter_estatisticas()
        print("\n" + "="*50)
        print("✅ DECISOR CONFIGURADO COM SUCESSO")
        print(f"   Modelos: {stats['modelos_carregados']}")
        print(f"   Heurísticas: {stats['heuristicas_ativas']}")
        print(f"   Performance média: {stats['performance_media']:.4f}")
        print(f"   Melhor modelo: {stats['melhor_modelo']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
