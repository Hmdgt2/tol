# tol/avaliador/avaliador.py
import os
import sys
import json
import numpy as np
import joblib
import datetime
import importlib
from typing import Dict, Any, List
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Adiciona o diretório raiz do projeto ao caminho do sistema.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa as classes e funções corretas para a nova estrutura do projeto
from lib.despachante import Despachante, criar_despachante_otimizado
from lib.dados import Dados

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# --- Caminhos dos Ficheiros ---
# O caminho para o ficheiro de estado, que deve estar na pasta 'decisor'
ULTIMO_SORTEIO_PROCESSADO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'sorteio_processado.json')
# O caminho para os dados do sorteio atual
DADOS_ATUAL_PATH = os.path.join(PROJECT_ROOT, 'dados', 'sorteio_atual.json')
# Novos caminhos para os ficheiros
MODELOS_DIR = os.path.join(PROJECT_ROOT, 'decisor', 'modelos_salvos')
PERFORMANCE_PATH = os.path.join(MODELOS_DIR, 'performance_modelos.json')
METADADOS_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'metadados_modelo.json')
MODELOS_ML_DIR = os.path.join(PROJECT_ROOT, 'modelos_ml')

# NOVO: Caminho para histórico de otimização
HISTORICO_OTIMIZACAO_PATH = os.path.join(PROJECT_ROOT, 'decisor', 'historico_otimizacao.json')

if not os.path.exists(MODELOS_DIR):
    os.makedirs(MODELOS_DIR)

def carregar_sorteio_processado(path: str) -> Dict[str, str]:
    """Carrega o identificador do último sorteio processado."""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError):
            print(f"Aviso: Erro ao carregar o estado do processamento em '{path}'. Começando do zero.")
            return {"ultimo_concurso_processado": ""}
    return {"ultimo_concurso_processado": ""}

def guardar_sorteio_processado(concurso: str, path: str):
    """Guarda o identificador do sorteio que acabou de ser processado."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"ultimo_concurso_processado": concurso}, f, indent=2, ensure_ascii=False)

def carregar_modelos_ml():
    """Carrega dinamicamente todos os modelos de ML disponíveis."""
    modelos = {}
    if not os.path.exists(MODELOS_ML_DIR):
        print(f"Diretório de modelos de ML não encontrado: {MODELOS_ML_DIR}")
        return modelos
    
    for ficheiro in os.listdir(MODELOS_ML_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            try:
                # Usa importlib para carregar o módulo
                spec = importlib.util.spec_from_file_location(nome_modulo, os.path.join(MODELOS_ML_DIR, ficheiro))
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                
                # Procura por uma função get_model() no módulo
                if hasattr(modulo, 'get_model') and callable(modulo.get_model):
                    instance = modulo.get_model()
                    if hasattr(instance, 'fit') and hasattr(instance, 'predict'):
                        modelos[nome_modulo] = instance
                        print(f"✅ Modelo ML '{nome_modulo}' carregado")
            except ImportError as e:
                print(f"Aviso: Não foi possível importar o modelo {nome_modulo}. Erro: {e}")
    return modelos

def avaliar_e_incrementar(usar_heuristicas_dinamicas: bool = True, forcar_reatreinamento: bool = False):
    """
    Verifica se há um novo sorteio para processar e, se houver,
    re-treina o modelo com o histórico completo.
    
    Args:
        usar_heuristicas_dinamicas: Ativa heurísticas dinâmicas
        forcar_reatreinamento: Força re-treino mesmo sem novo sorteio
    """
    print("🎯 Iniciando avaliação e atualização do sistema...")

    # 1. Carrega os dados do sorteio mais recente e verifica se já foi processado
    try:
        with open(DADOS_ATUAL_PATH, 'r', encoding='utf-8') as f:
            novo_sorteio = json.load(f)
        concurso_atual = novo_sorteio.get("concurso", "")
        data_sorteio = novo_sorteio.get("data", "")
        print(f"📅 Sorteio atual: {concurso_atual} ({data_sorteio})")
    except FileNotFoundError:
        print(f"⚠️ Ficheiro de dados mais recente não encontrado em: {DADOS_ATUAL_PATH}.")
        if not forcar_reatreinamento:
            return
        print("🔄 Continuando com re-treino forçado...")
        concurso_atual = "FORCADO_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    except json.JSONDecodeError:
        print(f"❌ Erro ao ler o ficheiro {DADOS_ATUAL_PATH}. Verifique se o JSON está formatado corretamente.")
        return

    estado_processamento = carregar_sorteio_processado(ULTIMO_SORTEIO_PROCESSADO_PATH)
    ultimo_processado = estado_processamento.get("ultimo_concurso_processado", "")

    if not forcar_reatreinamento and concurso_atual == ultimo_processado:
        print(f"✅ Sorteio '{concurso_atual}' já foi processado. Nenhuma ação necessária.")
        return

    if forcar_reatreinamento:
        print("🔄 Re-treino forçado ativado...")
    else:
        print(f"🆕 Novo sorteio '{concurso_atual}' detectado. Re-treinando modelos...")

    try:
        # 2. Carrega todas as heurísticas (FIXAS + DINÂMICAS) e o histórico de sorteios
        dados = Dados()
        sorteios_historico = dados.sorteios
        
        print(f"📊 Carregando {len(sorteios_historico)} sorteios históricos...")
        
        # NOVO: Usar despachante otimizado com heurísticas dinâmicas
        despachante = criar_despachante_otimizado() if usar_heuristicas_dinamicas else Despachante(usar_dinamicas=False)
        
        # NOVO: Reavaliar heurísticas dinâmicas se ativadas
        if usar_heuristicas_dinamicas:
            print("🔄 Reavaliando heurísticas dinâmicas...")
            despachante.reavaliar_heuristicas_dinamicas(dados, forcar_reatreinamento=True)
        
        # Obter estatísticas do sistema
        stats = despachante.obter_estatisticas_heuristicas()
        print(f"🔧 Sistema com {stats['total_heuristicas']} heurísticas "
              f"({stats['heuristicas_fixas']} fixas + {stats['heuristicas_dinamicas']} dinâmicas)")

        todas_dependencias = despachante.obter_todas_dependencias()

        # Obtém a lista de heurísticas disponíveis a partir dos metadados.
        metadados_heuristicas = despachante.obter_metadados()
        
        # NOVO: Ordenar heurísticas por tipo (fixas primeiro)
        heuristicas_ordenadas = sorted(
            list(metadados_heuristicas.keys()),
            key=lambda h: (0 if metadados_heuristicas[h].get('tipo') == 'fixa' else 1, h)
        )

        if not heuristicas_ordenadas or not sorteios_historico or len(sorteios_historico) < 2:
            print("❌ Dados ou heurísticas insuficientes para treino.")
            return

        print(f"🔄 Simulando previsões de {len(heuristicas_ordenadas)} heurísticas para dados históricos...")
        X_treino = []
        y_treino = []
        
        total_sorteios = len(sorteios_historico)
        print(f"📈 Processando {total_sorteios - 1} pontos de treino...")
        
        for i in range(len(sorteios_historico) - 1):
            if (i + 1) % 50 == 0:
                print(f"   📊 Processados {i + 1}/{total_sorteios - 1} sorteios...")
                
            historico_parcial = sorteios_historico[:i+1]
            sorteio_alvo = sorteios_historico[i+1]
            
            # CORREÇÃO CRUCIAL:
            # O método 'get_previsoes' do despachante espera um dicionário de estatísticas,
            # não uma lista de sorteios. Criamos uma instância temporária de Dados
            # para calcular as estatísticas com base no histórico parcial.
            dados_parciais = Dados()
            dados_parciais.sorteios = historico_parcial
            estatisticas_parciais, _ = dados_parciais.obter_estatisticas(todas_dependencias)

            # Passa as estatísticas calculadas corretamente para o despachante.
            previsoes_sorteio_atual = despachante.get_previsoes(estatisticas_parciais)

            for num in range(1, 50):
                feature_vector = [1 if num in previsoes_sorteio_atual.get(h, []) else 0 for h in heuristicas_ordenadas]
                X_treino.append(feature_vector)
                y_treino.append(1 if num in sorteio_alvo.get("numeros", []) else 0)

        X_treino_np = np.array(X_treino)
        y_treino_np = np.array(y_treino)

        print(f"✅ Conjunto de treino criado: {X_treino_np.shape[0]} amostras, {X_treino_np.shape[1]} características")

        # 3. Carrega os modelos dinamicamente
        modelos_disponiveis = carregar_modelos_ml()
        if not modelos_disponiveis:
            print("❌ Nenhum modelo de ML encontrado. O treino será encerrado.")
            return

        resultados_treino = {}
        data_atualizacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 4. Treina e salva cada modelo
        print("\n🧠 Iniciando o treino dos modelos de ML...")
        for nome_modelo, modelo in modelos_disponiveis.items():
            print(f"   Treinando: {nome_modelo}...")
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
                print(f"   ✅ {nome_modelo} salvo com score: {score_treino:.4f}")

            except Exception as e:
                print(f"   ❌ Erro ao treinar {nome_modelo}: {e}")
                continue

        # 5. Salva o ficheiro de performance
        with open(PERFORMANCE_PATH, 'w', encoding='utf-8') as f:
            json.dump(resultados_treino, f, indent=2, ensure_ascii=False)

        # 6. NOVO: Salva os metadados completos das heurísticas
        json_data_metadados = {
            'heuristicas_ordenadas': heuristicas_ordenadas,
            'metadados_completos': metadados_heuristicas,
            'estatisticas_sistema': stats,
            'data_treino': data_atualizacao,
            'usou_heuristicas_dinamicas': usar_heuristicas_dinamicas,
            'configuracao': {
                'total_heuristicas': len(heuristicas_ordenadas),
                'dimensoes_dataset': X_treino_np.shape,
                'sorteios_processados': total_sorteios
            }
        }
        with open(METADADOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_data_metadados, f, indent=2, ensure_ascii=False)

        # 7. NOVO: Exporta configuração do despachante
        despachante.exportar_configuracao()

        print("\n🎉 ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print(f"📊 RESUMO DA ATUALIZAÇÃO:")
        print(f"   • Heurísticas: {stats['total_heuristicas']} ({stats['heuristicas_fixas']}F + {stats['heuristicas_dinamicas']}D)")
        print(f"   • Modelos treinados: {len(resultados_treino)}")
        print(f"   • Dataset: {X_treino_np.shape[0]} amostras × {X_treino_np.shape[1]} características")
        print(f"   • Sorteios processados: {total_sorteios}")
        
        if resultados_treino:
            melhor_modelo = max(resultados_treino.items(), key=lambda x: x[1]['score_treino'])
            print(f"🏆 Melhor modelo: {melhor_modelo[0]} (score: {melhor_modelo[1]['score_treino']:.4f})")
        
        if stats.get('melhores_dinamicas'):
            print(f"⭐ Melhores dinâmicas: {', '.join(stats['melhores_dinamicas'][:3])}")

        guardar_sorteio_processado(concurso_atual, ULTIMO_SORTEIO_PROCESSADO_PATH)
        print(f"✅ Sistema atualizado com sorteio '{concurso_atual}'")

    except Exception as e:
        print(f"\n❌ ERRO durante a atualização:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Detalhes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def executar_manutencao_sistema():
    """
    FUNÇÃO NOVA: Executa manutenção completa do sistema
    """
    print("🛠️  INICIANDO MANUTENÇÃO DO SISTEMA...")
    
    try:
        # 1. Recarregar heurísticas
        print("🔄 Recarregando heurísticas...")
        despachante = criar_despachante_otimizado()
        dados = Dados()
        
        # 2. Reavaliar heurísticas dinâmicas
        print("📈 Reavaliando heurísticas dinâmicas...")
        despachante.reavaliar_heuristicas_dinamicas(dados, forcar_reatreinamento=True)
        
        # 3. Forçar re-treino completo
        print("🧠 Forçando re-treino completo...")
        avaliar_e_incrementar(usar_heuristicas_dinamicas=True, forcar_reatreinamento=True)
        
        print("✅ MANUTENÇÃO CONCLUÍDA!")
        
    except Exception as e:
        print(f"❌ Erro na manutenção: {e}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Sistema de Avaliação e Atualização')
    parser.add_argument('--sem-dinamicas', action='store_true', 
                       help='Desativar heurísticas dinâmicas')
    parser.add_argument('--forcar', action='store_true',
                       help='Forçar re-treino mesmo sem novo sorteio')
    parser.add_argument('--manutencao', action='store_true',
                       help='Executar manutenção completa do sistema')
    
    args = parser.parse_args()
    
    if args.manutencao:
        executar_manutencao_sistema()
    else:
        avaliar_e_incrementar(
            usar_heuristicas_dinamicas=not args.sem_dinamicas,
            forcar_reatreinamento=args.forcar
        )
