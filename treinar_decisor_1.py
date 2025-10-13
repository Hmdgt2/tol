# treinar_decisor.py
import os
import sys
import json
import numpy as np
import joblib
from collections import defaultdict
from typing import Dict, Any, List
import importlib
import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# CORREÇÃO 1: Adiciona o diretório raiz para resolver importações
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# IMPORTANTE: Agora importamos a classe 'Dados' em vez das funções
from lib.dados import Dados 
from lib.despachante_new import Despachante

# Adicionamos os imports para os modelos e o scaler
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Novos caminhos para os ficheiros
MODELOS_DIR = os.path.join(PROJECT_ROOT, 'decisor', 'modelos_salvos')
PERFORMANCE_PATH = os.path.join(MODELOS_DIR, 'performance_modelos.json')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
MODELOS_ML_DIR = os.path.join(PROJECT_ROOT, 'modelos_ml')

if not os.path.exists(MODELOS_DIR):
    os.makedirs(MODELOS_DIR)

def carregar_modelos_ml():
    """
    Carrega dinamicamente os modelos de machine learning da pasta 'modelos_ml'.
    """
    modelos_disponiveis = {}
    sys.path.insert(0, MODELOS_ML_DIR)
    for filename in os.listdir(MODELOS_ML_DIR):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'get_model'):
                    modelos_disponiveis[module_name] = module.get_model()
            except ImportError as e:
                print(f"Aviso: Não foi possível importar o modelo '{module_name}'. Erro: {e}")
    sys.path.pop(0)
    return modelos_disponiveis

def treinar_decisor(usar_heuristicas_dinamicas: bool = True, num_heuristicas_dinamicas: int = 20):
    """
    Treina múltiplos modelos e salva o melhor.
    
    Args:
        usar_heuristicas_dinamicas: Ativa o uso de heurísticas geradas automaticamente
        num_heuristicas_dinamicas: Número de heurísticas dinâmicas a gerar
    """
    try:
        # 1. Carrega o despachante COM HEURÍSTICAS DINÂMICAS
        print("🎯 Iniciando o treino. Carregando heurísticas e dados...")
        despachante = Despachante(usar_dinamicas=usar_heuristicas_dinamicas)
        
        # IMPORTANTE: Instancia a classe Dados para carregar os sorteios
        dados_manager = Dados()
        sorteios_historico = dados_manager.sorteios

        # NOVO: Otimização de heurísticas dinâmicas se ativado
        if usar_heuristicas_dinamicas:
            print("🔄 Otimizando heurísticas dinâmicas...")
            despachante.reavaliar_heuristicas_dinamicas(dados_manager)
        
        # Estatísticas do sistema atualizado
        stats = despachante.obter_estatisticas_heuristicas()
        print(f"📊 Sistema com {stats['total_heuristicas']} heurísticas "
              f"({stats['heuristicas_fixas']} fixas + {stats['heuristicas_dinamicas']} dinâmicas)")
        
        if stats.get('melhores_dinamicas'):
            print(f"🏆 Melhores dinâmicas: {', '.join(stats['melhores_dinamicas'][:3])}")

        todas_dependencias = despachante.obter_todas_dependencias()

        if not todas_dependencias or not sorteios_historico or len(sorteios_historico) < 2:
            print("❌ Dados insuficientes para treino. O processo será encerrado.")
            return

        print("🔄 Simulando previsões de heurísticas (fixas + dinâmicas) para dados históricos...")
        X_treino = []
        y_treino = []
        
        # CORREÇÃO: Altera o nome do método de 'get_metadados' para 'obter_metadados'
        metadados_heuristicas = despachante.obter_metadados()
        
        # NOVO: Ordenar heurísticas por tipo (fixas primeiro, depois dinâmicas)
        heuristicas_ordenadas = sorted(
            list(metadados_heuristicas.keys()),
            key=lambda h: (0 if metadados_heuristicas[h].get('tipo') == 'fixa' else 1, h)
        )

        total_sorteios = len(sorteios_historico)
        print(f"📈 Processando {total_sorteios - 1} pontos de treino...")

        for i in range(len(sorteios_historico) - 1):
            if (i + 1) % 50 == 0:
                print(f"   Processados {i + 1}/{total_sorteios - 1} sorteios...")
                
            # IMPORTANTE: Cria uma nova instância de Dados com um subconjunto do histórico
            # Isso simula o conhecimento do sistema em cada ponto do tempo.
            historico_parcial = sorteios_historico[:i+1]
            dados_parciais = Dados()
            dados_parciais.sorteios = historico_parcial
            
            sorteio_alvo = sorteios_historico[i+1]
            
            # Chama o método da instância para obter as estatísticas
            estatisticas_parciais, _ = dados_parciais.obter_estatisticas(todas_dependencias)
            
            previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)
            
            for num in range(1, 50):
                feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
                X_treino.append(feature_vector)
                y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

        X_treino_np = np.array(X_treino)
        y_treino_np = np.array(y_treino)

        print(f"✅ Conjunto de treino criado: {X_treino_np.shape[0]} amostras, {X_treino_np.shape[1]} características")

        # 2. Carrega os modelos dinamicamente
        modelos_disponiveis = carregar_modelos_ml()
        if not modelos_disponiveis:
            print("❌ Nenhum modelo de ML encontrado na pasta 'modelos_ml'. O treino será encerrado.")
            return
            
        resultados_treino = {}
        data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 3. Treina e salva cada modelo
        print("\n🧠 Conjunto de treino criado. Iniciando o treino dos modelos de ML...")
        for nome_modelo, modelo in modelos_disponiveis.items():
            print(f"   Treinando o modelo: {nome_modelo}...")
            try:
                pipeline = Pipeline([
                    ('scaler', StandardScaler()),
                    ('model', modelo)
                ])
                pipeline.fit(X_treino_np, y_treino_np)
                
                # Avalia o modelo
                score_treino = pipeline.score(X_treino_np, y_treino_np)
                
                # Salva o pipeline
                modelo_path = os.path.join(MODELOS_DIR, f"{nome_modelo}_pipeline.joblib")
                joblib.dump(pipeline, modelo_path)
                
                resultados_treino[nome_modelo] = {
                    'caminho': modelo_path,
                    'score_treino': score_treino,
                    'ultima_atualizacao': data_atualizacao,
                    'num_caracteristicas': X_treino_np.shape[1],
                    'num_amostras': X_treino_np.shape[0]
                }
                print(f"   ✅ Modelo {nome_modelo} salvo com score: {score_treino:.4f}")
                
            except Exception as e:
                print(f"   ❌ Erro ao treinar {nome_modelo}: {e}")
                continue

        # 4. Salva o ficheiro de performance
        with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
            json.dump(resultados_treino, f, indent=2, ensure_ascii=False)
            
        # 5. Salva os metadados das heurísticas (ATUALIZADO)
        json_data_metadados = {
            'heuristicas_ordenadas': heuristicas_ordenadas,
            'metadados_completos': metadados_heuristicas,
            'estatisticas_sistema': stats,
            'data_treino': data_atualizacao,
            'usou_heuristicas_dinamicas': usar_heuristicas_dinamicas
        }
        with open(METADADOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_data_metadados, f, indent=2, ensure_ascii=False)
        
        # 6. NOVO: Salva informações sobre heurísticas dinâmicas
        if usar_heuristicas_dinamicas and hasattr(despachante, 'gerador_dinamicas'):
            info_dinamicas = {
                'melhores_heuristicas': despachante.gerador_dinamicas.historico_desempenho[:10],
                'total_geradas': len(despachante.heuristicas_dinamicas),
                'data_avaliacao': data_atualizacao
            }
            dinamicas_path = os.path.join(MODELOS_DIR, 'heuristicas_dinamicas_info.json')
            with open(dinamicas_path, 'w', encoding='utf-8') as f:
                json.dump(info_dinamicas, f, indent=2, ensure_ascii=False)
            
        # Relatório final
        print("\n🎉 TREINO CONCLUÍDO COM SUCESSO!")
        print("=" * 50)
        print(f"📊 Estatísticas do Sistema:")
        print(f"   • Heurísticas totais: {stats['total_heuristicas']}")
        print(f"   • Heurísticas fixas: {stats['heuristicas_fixas']}")
        print(f"   • Heurísticas dinâmicas: {stats['heuristicas_dinamicas']}")
        print(f"   • Dependências únicas: {stats['dependencias_unicas']}")
        print(f"   • Modelos treinados: {len(resultados_treino)}")
        print(f"   • Dimensões do dataset: {X_treino_np.shape}")
        
        if resultados_treino:
            melhor_modelo = max(resultados_treino.items(), key=lambda x: x[1]['score_treino'])
            print(f"🏆 Melhor modelo: {melhor_modelo[0]} (score: {melhor_modelo[1]['score_treino']:.4f})")

    except Exception as e:
        print(f"\n❌ ERRO FATAL: Ocorreu um erro durante o treino do modelo.")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Detalhes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def analisar_desempenho_heuristicas():
    """
    FUNÇÃO NOVA: Analisa o desempenho individual das heurísticas
    """
    try:
        print("\n📈 ANALISANDO DESEMPENHO DAS HEURÍSTICAS...")
        
        despachante = Despachante(usar_dinamicas=True)
        dados_manager = Dados()
        
        # Reavaliar heurísticas dinâmicas
        despachante.reavaliar_heuristicas_dinamicas(dados_manager)
        
        # Carregar histórico de desempenho
        if hasattr(despachante, 'gerador_dinamicas'):
            desempenho = despachante.gerador_dinamicas.historico_desempenho
            
            print("\n🏆 TOP 10 HEURÍSTICAS DINÂMICAS:")
            for i, heur in enumerate(desempenho[:10]):
                print(f"   {i+1:2d}. {heur['nome']:30} | Acerto: {heur['taxa_acerto']:.3f} | "
                      f"Score: {heur['score']:.3f} | Estabilidade: {heur['estabilidade']:.3f}")
        
        stats = despachante.obter_estatisticas_heuristicas()
        print(f"\n📊 RESUMO DO SISTEMA:")
        print(f"   Total de heurísticas: {stats['total_heuristicas']}")
        print(f"   Heurísticas fixas: {stats['heuristicas_fixas']}")
        print(f"   Heurísticas dinâmicas: {stats['heuristicas_dinamicas']}")
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Treinar modelos de decisão para loteria')
    parser.add_argument('--sem-dinamicas', action='store_true', 
                       help='Desativar heurísticas dinâmicas')
    parser.add_argument('--analisar', action='store_true',
                       help='Apenas analisar desempenho das heurísticas')
    parser.add_argument('--num-dinamicas', type=int, default=20,
                       help='Número de heurísticas dinâmicas a gerar')
    
    args = parser.parse_args()
    
    if args.analisar:
        analisar_desempenho_heuristicas()
    else:
        treinar_decisor(
            usar_heuristicas_dinamicas=not args.sem_dinamicas,
            num_heuristicas_dinamicas=args.num_dinamicas
        )
