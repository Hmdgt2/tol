# organizador_biblioteca.py
import os
import shutil
import datetime
from ast_consolidador import ASTConsolidator

# =================================================================
# CONFIGURAÇÕES
# =================================================================
DIR_ORIGEM = 'lib/funcoes_analiticas'
DIR_DESTINO = 'lib/funcoes_limpas'

# REGRAS CANÓNICAS - Defina aqui TODAS as suas duplicações
REGRAS_CANONICAS = {
    # Estatísticas Básicas → estatisticas.py
    ("unique_count", "conjuntos"): ("estatisticas", None),
    ("intersection", "conjuntos"): ("estatisticas", None),
    ("union", "conjuntos"): ("estatisticas", None),
    ("mirror_count", "conjuntos"): ("estatisticas", None),
    ("pair_sum_count", "conjuntos"): ("estatisticas", None),
    ("iqr_outliers", "deteccao_anomalias"): ("estatisticas", None),
    
    # Números Especiais → numeros_especiais.py
    ("bell_number", "teoria_numeros"): ("numeros_especiais", "bell_number"),
    ("partition_number", "teoria_numeros"): ("numeros_especiais", "partition_number"),
    ("bernoulli_number", "teoria_numeros"): ("numeros_especiais", "bernoulli_number"),
    ("fibonacci", "teoria_numeros"): ("numeros_especiais", "fibonacci_num"),
    ("lucas", "teoria_numeros"): ("numeros_especiais", "lucas_num"),
    ("catalan_number", "teoria_numeros"): ("numeros_especiais", "catalan_num"),
    
    # Funções Especiais → funcoes_especiais.py
    ("gamma_func", "matematica_especial"): ("funcoes_especiais", None),
    ("beta_func", "matematica_especial"): ("funcoes_especiais", None),
    ("bessel_j", "matematica_especial"): ("funcoes_especiais", None),
    
    # Processamento de Sinal → temporais.py
    ("fft_phase", "processamento_sinal"): ("temporais", None),
    ("ifft_real", "processamento_sinal"): ("temporais", None),
    
    # Teoria da Informação → teoria_informacao.py
    ("mutual_info", "estatistica_multivariada"): ("teoria_informacao", None),
    ("normalized_mutual_info", "estatistica_multivariada"): ("teoria_informacao", None),

    # REGRAS CANONICAS - Defina aqui TODAS as suas duplicações
REGRAS_CANONICAS = {
    # ... regras existentes ...
    
    # 🆕 SISTEMAS DINÂMICOS AVANÇADOS → sistemas_dinamicos_avancados.py
    ("lyapunov_exponent", "analise_numerica_avancada"): ("sistemas_dinamicos_avancados", None),
    ("takens_embedding", "analise_numerica_avancada"): ("sistemas_dinamicos_avancados", None),
    ("permutation_entropy", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    ("recurrence_plot", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    ("rossler_attractor", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    
    # 🆕 COMPUTAÇÃO AVANÇADA → computacao_avancada.py
    ("numba_optimized_operations", "computacao_jit"): ("computacao_avancada", None),
    ("cupy_gpu_analysis", "gpu_computing"): ("computacao_avancada", None),
    ("jax_autodiff_analysis", "diferenciação_automatica"): ("computacao_avancada", None),
    ("dask_parallel_analysis", "processamento_distribuido"): ("computacao_avancada", None),
    ("mpi_distributed_analysis", "computacao_cluster"): ("computacao_avancada", None),
    
    # 🆕 MATEMÁTICA SIMBÓLICA → matematica_simbolica.py
    ("symbolic_sequence_analysis", "analise_simbolica"): ("matematica_simbolica", None),
    ("closed_form_expression_finder", "analise_simbolica"): ("matematica_simbolica", None),
    ("symengine_fast_symbolic", "simbolica_rapida"): ("matematica_simbolica", None),
    
    # 🆕 ANÁLISE QUÂNTICA → analise_quantica.py
    ("quantum_wavefunction_analysis", "analise_quantica"): ("analise_quantica", None),
    ("stochastic_process_classification", "analise_quantica"): ("analise_quantica", None),
    
    # 🆕 TEORIA DO CAOS → teoria_caos.py
    ("chaotic_system_identification", "teoria_caos"): ("teoria_caos", None),
    ("correlation_dimension_estimate", "teoria_caos"): ("teoria_caos", None),
    
    # 🆕 PADRÕES EVOLUTIVOS → padroes_evolutivos.py
    ("evolutionary_fractal_dimension", "padroes_evolutivos_temporais"): ("padroes_evolutivos", None),
    ("temporal_pattern_entropy", "padroes_evolutivos_temporais"): ("padroes_evolutivos", None),
    ("phase_transition_detector", "transicoes_fase"): ("padroes_evolutivos", None),
    ("critical_slowdown_analysis", "transicoes_fase"): ("padroes_evolutivos", None),
    
    # 🆕 TEORIA DAS CATÁSTROFES → teoria_catastrofe.py
    ("catastrophe_theory_analyzer", "teoria_catastrofe"): ("teoria_catastrofe", None),
    ("tipping_point_early_warning", "teoria_catastrofe"): ("teoria_catastrofe", None),
    
    # 🆕 PADRÕES CÓSMICOS → padroes_cosmicos.py
    ("astronomical_cycle_detector", "padroes_cosmicos"): ("padroes_cosmicos", None),
    ("galactic_pattern_analyzer", "padroes_cosmicos"): ("padroes_cosmicos", None),
    
    # 🆕 REDES COMPLEXAS → redes_complexas_avancadas.py
    ("temporal_network_analysis", "redes_complexas_temporais"): ("redes_complexas_avancadas", None),
    ("graph_spectral_gap", "funcoes_diversas"): ("redes_complexas_avancadas", None),
    ("betweenness_centrality_approx", "funcoes_diversas"): ("redes_complexas_avancadas", None),
    
    # 🆕 OTIMIZAÇÃO AVANÇADA → otimizacao_avancada.py
    ("simulated_annealing", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("particle_swarm_optimization", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("genetic_algorithm", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("convex_function_test", "otimizacao_convexa"): ("otimizacao_avancada", None),
    
    # 🆕 ANÁLISE MULTIVARIADA AVANÇADA → analise_multivariada_avancada.py
    ("mahalanobis_distance", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    ("hotelling_t2_test", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    ("canonical_correlation", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    
    # 🆕 BIG DATA E SCALE-OUT → big_data_scaleout.py
    ("spark_big_data_analysis", "big_data_analysis"): ("big_data_scaleout", None),
    ("vaex_lazy_dataframe_analysis", "big_dataframes"): ("big_data_scaleout", None),
    ("modin_parallel_dataframe", "pandas_acelerado"): ("big_data_scaleout", None),
    ("dask_ml_distributed_learning", "ml_distribuido"): ("big_data_scaleout", None),
}
}

# Funções que requerem intervenção manual
ACOES_MANUAIS = [
    "sum_of_pairs",
    "sum_of_triples", 
    "shortest_paths_length",
    "cupy_gpu_analysis",           # Requer GPU NVIDIA
    "mpi_distributed_analysis",    # Requer MPI
    "spark_big_data_analysis",     # Requer Apache Spark
    "stan_bayesian_inference",     # Requer Stan/CmdStan
    "arb_arbitrary_precision_analysis",  # Requer Flint/Arb
    "gmpy2_multiprecision_analysis",     # Requer GMP/MPFR
]

# =================================================================
# FUNÇÕES AUXILIARES
# =================================================================
def criar_backup_original():
    """Cria um backup da biblioteca original."""
    if os.path.exists(DIR_ORIGEM):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = f"backup_biblioteca_original_{timestamp}"
        shutil.copytree(DIR_ORIGEM, backup_dir)
        print(f"📦 Backup criado: {backup_dir}")
        return backup_dir
    else:
        print("⚠️ Diretório original não encontrado.")
        return None

def preparar_area_staging():
    """Prepara a área de staging copiando a biblioteca original."""
    # Limpar staging anterior
    if os.path.exists(DIR_DESTINO):
        shutil.rmtree(DIR_DESTINO)
        print("♻️  Staging anterior removido")
    
    # Criar nova área de staging
    shutil.copytree(DIR_ORIGEM, DIR_DESTINO)
    print(f"✅ Área de staging criada: {DIR_DESTINO}")

def verificar_ambiente():
    """Verifica se o ambiente está pronto para execução."""
    if not os.path.exists(DIR_ORIGEM):
        print(f"❌ ERRO: Diretório original '{DIR_ORIGEM}' não encontrado!")
        return False
    
    try:
        import astunparse
        return True
    except ImportError:
        print("❌ ERRO: 'astunparse' não instalado. Execute: pip install astunparse")
        return False

# =================================================================
# ORQUESTRADOR PRINCIPAL
# =================================================================
def executar_consolidacao_automatica():
    """Executa o processo completo de consolidação."""
    print("🧹 ORGANIZADOR DE BIBLIOTECA - MODO STAGING")
    print("=" * 60)
    
    # Verificar ambiente
    if not verificar_ambiente():
        return
    
    # Preparação
    criar_backup_original()
    preparar_area_staging()
    
    print("\n🚀 INICIANDO LIMPEZA NA ÁREA DE STAGING")
    print("=" * 60)
    
    sucesso_count = 0
    falha_count = 0
    ignoradas_count = 0
    
    # Processar cada regra canónica
    for (func_name, source_mod), (target_mod, novo_nome) in REGRAS_CANONICAS.items():
        source_path = os.path.join(DIR_DESTINO, f"{source_mod}.py")
        
        # Verificar se o módulo de origem existe no staging
        if not os.path.exists(source_path):
            print(f"📋 {func_name}: ❌ Módulo '{source_mod}.py' não encontrado no staging")
            ignoradas_count += 1
            continue
            
        print(f"📋 {func_name}: {source_mod}.py → {target_mod}.py")
        
        try:
            consolidator = ASTConsolidator(target_mod, source_mod, DIR_DESTINO)
            resultado = consolidator.mover_funcao(func_name, novo_nome)
            
            if resultado:
                sucesso_count += 1
            else:
                falha_count += 1
                
        except Exception as e:
            print(f"    ❌ Erro inesperado: {e}")
            falha_count += 1
    
    # Relatório Final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL DA AUTOMAÇÃO")
    print("=" * 60)
    print(f"✅ Consolidações bem sucedidas: {sucesso_count}")
    print(f"❌ Falhas no processamento: {falha_count}")
    print(f"⚠️  Ignoradas (módulo não encontrado): {ignoradas_count}")
    
    # Ações Manuais
    if ACOES_MANUAIS:
        mostrar_relatorio_manual()
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"   1. Biblioteca limpa disponível em: {DIR_DESTINO}")
    print(f"   2. Biblioteca original preservada em: {DIR_ORIGEM}")
    print(f"   3. Resolva as ações manuais listadas acima")
    print(f"   4. Quando satisfeito, substitua {DIR_ORIGEM} por {DIR_DESTINO}")

def mostrar_relatorio_manual():
    """Mostra as ações que precisam de intervenção manual."""
    print("\n🔧 AÇÕES MANUAIS NECESSÁRIAS")
    print("=" * 60)
    print("Estas funções têm conflitos de LÓGICA e precisam de fusão manual:")
    
    for i, acao in enumerate(ACOES_MANUAIS, 1):
        print(f"   {i}. ⚠️  {acao}")
    
    print(f"\n📝 INSTRUÇÕES:")
    print(f"   • Edite APENAS a pasta '{DIR_DESTINO}'")
    print(f"   • Analise o código de cada função em conflito")
    print(f"   • Escolha a implementação mais eficiente")
    print(f"   • Funda manualmente e remova duplicados")

# =================================================================
# EXECUÇÃO
# =================================================================
if __name__ == "__main__":
    executar_consolidacao_automatica()
