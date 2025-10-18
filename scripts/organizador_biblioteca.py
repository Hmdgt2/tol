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
    
    # 🆕 SISTEMAS DINÂMICOS AVANÇADOS → sistemas_dinamicos_avancados.py
    ("lyapunov_exponent", "analise_numerica_avancada"): ("sistemas_dinamicos_avancados", None),
    ("takens_embedding", "analise_numerica_avancada"): ("sistemas_dinamicos_avancados", None),
    ("permutation_entropy", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    ("recurrence_plot", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    ("rossler_attractor", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    ("lyapunov_spectrum", "sistemas_dinamicos"): ("sistemas_dinamicos_avancados", None),
    
    # 🆕 COMPUTAÇÃO AVANÇADA → computacao_avancada.py
    ("numba_optimized_operations", "computacao_jit"): ("computacao_avancada", None),
    ("numba_vectorized_transform", "computacao_jit"): ("computacao_avancada", None),
    ("jit_compiled_analysis", "computacao_jit"): ("computacao_avancada", None),
    ("cupy_gpu_analysis", "gpu_computing"): ("computacao_avancada", None),
    ("jax_autodiff_analysis", "diferenciação_automatica"): ("computacao_avancada", None),
    ("jax_hamiltonian_dynamics", "diferenciação_automatica"): ("computacao_avancada", None),
    ("dask_parallel_analysis", "processamento_distribuido"): ("computacao_avancada", None),
    ("mpi_distributed_analysis", "computacao_cluster"): ("computacao_avancada", None),
    ("cython_analysis_wrapper", "cython_extensions"): ("computacao_avancada", None),
    ("numexpr_vector_operations", "computacao_high_performance"): ("computacao_avancada", None),
    
    # 🆕 MATEMÁTICA SIMBÓLICA → matematica_simbolica.py
    ("symbolic_sequence_analysis", "analise_simbolica"): ("matematica_simbolica", None),
    ("closed_form_expression_finder", "analise_simbolica"): ("matematica_simbolica", None),
    ("symengine_fast_symbolic", "simbolica_rapida"): ("matematica_simbolica", None),
    ("sym_derivative", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_integral", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_series_expansion", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_limit", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_roots", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_simplify", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_expand", "algebra_simbolica"): ("matematica_simbolica", None),
    ("sym_factor", "algebra_simbolica"): ("matematica_simbolica", None),
    
    # 🆕 ANÁLISE QUÂNTICA → analise_quantica.py
    ("quantum_wavefunction_analysis", "analise_quantica"): ("analise_quantica", None),
    ("stochastic_process_classification", "analise_quantica"): ("analise_quantica", None),
    ("density_matrix_purity", "informacao_quantica"): ("analise_quantica", None),
    ("von_neumann_entropy", "informacao_quantica"): ("analise_quantica", None),
    ("quantum_fidelity", "informacao_quantica"): ("analise_quantica", None),
    ("concurrence_entanglement", "informacao_quantica"): ("analise_quantica", None),
    
    # 🆕 TEORIA DO CAOS → teoria_caos.py
    ("chaotic_system_identification", "teoria_caos"): ("teoria_caos", None),
    ("correlation_dimension_estimate", "teoria_caos"): ("teoria_caos", None),
    
    # 🆕 PADRÕES EVOLUTIVOS → padroes_evolutivos.py
    ("evolutionary_fractal_dimension", "padroes_evolutivos_temporais"): ("padroes_evolutivos", None),
    ("temporal_pattern_entropy", "padroes_evolutivos_temporais"): ("padroes_evolutivos", None),
    ("phase_transition_detector", "transicoes_fase"): ("padroes_evolutivos", None),
    ("critical_slowdown_analysis", "transicoes_fase"): ("padroes_evolutivos", None),
    ("sequence_autocorrelation_pattern", "analise_sequencias_avancada"): ("padroes_evolutivos", None),
    ("number_theory_pattern_detector", "analise_sequencias_avancada"): ("padroes_evolutivos", None),
    ("recursive_sequence_analyzer", "analise_sequencias_avancada"): ("padroes_evolutivos", None),
    
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
    ("monoid_operation_check", "algebra_categorias"): ("redes_complexas_avancadas", None),
    ("functor_application", "algebra_categorias"): ("redes_complexas_avancadas", None),
    ("natural_transformation", "algebra_categorias"): ("redes_complexas_avancadas", None),
    ("yoneda_embedding", "algebra_categorias"): ("redes_complexas_avancadas", None),
    
    # 🆕 OTIMIZAÇÃO AVANÇADA → otimizacao_avancada.py
    ("simulated_annealing", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("particle_swarm_optimization", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("genetic_algorithm", "otimizacao_metaheuristicas"): ("otimizacao_avancada", None),
    ("convex_function_test", "otimizacao_convexa"): ("otimizacao_avancada", None),
    ("subgradient_method", "otimizacao_convexa"): ("otimizacao_avancada", None),
    ("lagrange_duality", "otimizacao_convexa"): ("otimizacao_avancada", None),
    ("barrier_method", "otimizacao_convexa"): ("otimizacao_avancada", None),
    ("polynomial_pattern_fitter", "analise_algebrica"): ("otimizacao_avancada", None),
    ("exponential_pattern_detector", "analise_algebrica"): ("otimizacao_avancada", None),
    
    # 🆕 ANÁLISE MULTIVARIADA AVANÇADA → analise_multivariada_avancada.py
    ("mahalanobis_distance", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    ("hotelling_t2_test", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    ("canonical_correlation", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    ("linear_discriminant_analysis", "estatistica_multivariada_2"): ("analise_multivariada_avancada", None),
    
    # 🆕 BIG DATA E SCALE-OUT → big_data_scaleout.py
    ("spark_big_data_analysis", "big_data_analysis"): ("big_data_scaleout", None),
    ("vaex_lazy_dataframe_analysis", "big_dataframes"): ("big_data_scaleout", None),
    ("modin_parallel_dataframe", "pandas_acelerado"): ("big_data_scaleout", None),
    ("dask_ml_distributed_learning", "ml_distribuido"): ("big_data_scaleout", None),
    
    # 🆕 ANÁLISE FUNCIONAL → analise_funcional.py
    ("sobolev_norm", "analise_funcional"): ("analise_funcional", None),
    ("operator_norm_approx", "analise_funcional"): ("analise_funcional", None),
    ("spectral_radius_approx", "analise_funcional"): ("analise_funcional", None),
    
    # 🆕 GEOMETRIA FRACTAL → geometria_fractal.py
    ("multifractal_spectrum", "geometria_fractal"): ("geometria_fractal", None),
    ("lacunarity_analysis", "geometria_fractal"): ("geometria_fractal", None),
    ("hausdorff_dimension_approx", "teoria_medida"): ("geometria_fractal", None),
    
    # 🆕 SIMULAÇÃO E MÉTODOS ESTOCÁSTICOS → simulacao_estocastica.py
    ("metropolis_hastings", "simulacao"): ("simulacao_estocastica", None),
    ("monte_carlo_multistep", "simulacao"): ("simulacao_estocastica", None),
    ("simulate_multinomial_prob", "probabilidade_distribuicoes"): ("simulacao_estocastica", None),
    ("simulate_dirichlet", "probabilidade_distribuicoes"): ("simulacao_estocastica", None),
    ("simulate_multivariate_wishart", "probabilidade_distribuicoes"): ("simulacao_estocastica", None),
    
    # 🆕 PRECISÃO ARBITRÁRIA → precisao_arbitraria.py
    ("arb_arbitrary_precision_analysis", "precisao_arbitraria"): ("precisao_arbitraria", None),
    ("gmpy2_multiprecision_analysis", "multiprecisao_gmp"): ("precisao_arbitraria", None),
    ("mpmath_sqrt", "precisao"): ("precisao_arbitraria", None),
    ("mpmath_log", "precisao"): ("precisao_arbitraria", None),
    ("mpmath_sin", "precisao"): ("precisao_arbitraria", None),
    ("mpmath_prod_list", "precisao"): ("precisao_arbitraria", None),
    ("mpmath_sum_list", "precisao"): ("precisao_arbitraria", None),
    
    # 🆕 ANÁLISE NUMÉRICA AVANÇADA → analise_numerica_avancada.py
    ("mellin_transform", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("hankel_transform", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("fourier_bessel_transform", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("hypergeometric_1f1", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("hypergeometric_2f1", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("meijer_g_transform", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("fresnel_integral", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("exponential_integral_e1", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("sine_integral", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("cosine_integral", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("mathieu_characteristic", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    ("mathieu_function_even", "analise_numerica_avancada"): ("analise_numerica_avancada", None),
    
    # 🆕 MODELAGEM PROBABILÍSTICA → modelagem_probabilistica.py
    ("pymc3_probabilistic_modeling", "modelagem_probabilistica"): ("modelagem_probabilistica", None),
    ("pymc3_gaussian_process", "modelagem_probabilistica"): ("modelagem_probabilistica", None),
    ("stan_bayesian_inference", "inferencia_bayesiana_stan"): ("modelagem_probabilistica", None),
    ("tfp_bayesian_analysis", "estatistica_bayesiana"): ("modelagem_probabilistica", None),
    
    # 🆕 GEOMETRIA COMPUTACIONAL → geometria_computacional.py
    ("convex_hull_area", "funcoes_diversas"): ("geometria_computacional", None),
    ("smallest_enclosing_circle", "funcoes_diversas"): ("geometria_computacional", None),
    ("gaussian_curvature", "geometria_diferencial"): ("geometria_computacional", None),
    ("geodesic_distance", "geometria_diferencial"): ("geometria_computacional", None),
    ("riemann_metric_tensor", "geometria_diferencial"): ("geometria_computacional", None),
    
    # 🆕 ANÁLISE TEMPORAL MULTI-ESCALA → analise_temporal_multiescala.py
    ("multi_scale_entropy_analysis", "analise_temporal_multiescala"): ("analise_temporal_multiescala", None),
    ("wavelet_multiresolution_analysis", "analise_temporal_multiescala"): ("analise_temporal_multiescala", None),
    
    # 🆕 ANÁLISE DE SIMILARIDADE AVANÇADA → analise_similaridade_avancada.py
    ("dynamic_time_warping_distance", "analise_similaridade_avancada"): ("analise_similaridade_avancada", None),
    ("sequence_kernel_similarity", "analise_similaridade_avancada"): ("analise_similaridade_avancada", None),
    ("pattern_cross_correlation", "analise_similaridade_avancada"): ("analise_similaridade_avancada", None),
    
    # 🆕 EVOLUÇÃO DARWINIANA → evolucao_darwiniana.py
    ("evolutionary_fitness_landscape", "evolucao_darwiniana"): ("evolucao_darwiniana", None),
    ("evolutionary_algorithm_simulation", "evolucao_darwiniana"): ("evolucao_darwiniana", None),
    
    # 🆕 ANÁLISE COMBINATÓRIA AVANÇADA → analise_combinatoria_avancada.py
    ("combinatorial_pattern_density", "analise_combinatoria_avancada"): ("analise_combinatoria_avancada", None),
    ("sequence_complexity_measure", "analise_combinatoria_avancada"): ("analise_combinatoria_avancada", None),
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
    "cython_analysis_wrapper",     # Requer compilação Cython
    "pymc3_probabilistic_modeling", # Requer PyMC3 com Theano
    "tfp_bayesian_analysis",       # Requer TensorFlow Probability
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
        print("✅ astunparse: Disponível")
    except ImportError:
        print("❌ ERRO: 'astunparse' não instalado. Execute: pip install astunparse")
        return False
    
    # 🆕 VERIFICAR DEPENDÊNCIAS AVANÇADAS
    dependencias_avancadas = {
        'cupy': 'GPU Computing (NVIDIA)',
        'mpi4py': 'Processamento Distribuído (MPI)',
        'pyspark': 'Big Data (Apache Spark)',
        'cmdstanpy': 'Inferência Bayesiana (Stan)',
        'flint': 'Precisão Arbitrária (Arb)',
        'gmpy2': 'Múltipla Precisão (GMP/MPFR)',
        'jax': 'Diferenciação Automática',
        'symengine': 'Matemática Simbólica Rápida',
        'pymc3': 'Modelagem Probabilística',
        'tensorflow_probability': 'Estatística Bayesiana',
        'vaex': 'DataFrames Lazy',
        'modin': 'Pandas Paralelizado',
        'dask_ml': 'Machine Learning Distribuído',
        'networkit': 'Grafos em Larga Escala',
        'astropy': 'Análise Astronômica',
        'biopython': 'Análise de Sequências Biológicas',
    }
    
    print("\n🔍 VERIFICANDO DEPENDÊNCIAS AVANÇADAS:")
    print("=" * 50)
    
    for dep, desc in dependencias_avancadas.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {desc} - DISPONÍVEL")
        except ImportError:
            print(f"⚠️  {dep}: {desc} - NÃO INSTALADO")
    
    return True

def mostrar_relatorio_categorias_novas():
    """Mostra as novas categorias criadas."""
    categorias_novas = {
        'sistemas_dinamicos_avancados': 'Análise de sistemas não-lineares e caóticos',
        'computacao_avancada': 'GPU, paralelismo, JIT e computação distribuída',
        'matematica_simbolica': 'Álgebra computacional e análise simbólica',
        'analise_quantica': 'Métodos inspirados em mecânica quântica',
        'teoria_caos': 'Sistemas caóticos e expoentes de Lyapunov',
        'padroes_evolutivos': 'Análise temporal em múltiplas escalas',
        'teoria_catastrofe': 'Detecção de pontos de virada',
        'padroes_cosmicos': 'Padrões em escalas temporais longas',
        'redes_complexas_avancadas': 'Análise de grafos temporais e espectrais',
        'otimizacao_avancada': 'Metaheurísticas e otimização convexa',
        'analise_multivariada_avancada': 'Métodos estatísticos multivariados',
        'big_data_scaleout': 'Processamento de dados em grande escala',
        'analise_funcional': 'Análise em espaços de função',
        'geometria_fractal': 'Análise de dimensões fractais',
        'simulacao_estocastica': 'Métodos de Monte Carlo e MCMC',
        'precisao_arbitraria': 'Cálculos com precisão arbitrária',
        'analise_numerica_avancada': 'Transformadas especiais e funções matemáticas',
        'modelagem_probabilistica': 'Modelos bayesianos e inferência',
        'geometria_computacional': 'Algoritmos geométricos avançados',
        'analise_temporal_multiescala': 'Análise em múltiplas resoluções temporais',
        'analise_similaridade_avancada': 'Métodos avançados de similaridade',
        'evolucao_darwiniana': 'Algoritmos evolutivos e landscapes',
        'analise_combinatoria_avancada': 'Análise de padrões combinatórios complexos',
    }
    
    print("\n🆕 NOVAS CATEGORIAS CRIADAS:")
    print("=" * 60)
    for cat, desc in categorias_novas.items():
        print(f"   📁 {cat}.py: {desc}")

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
    
    # 🆕 MOSTRAR CATEGORIAS NOVAS
    mostrar_relatorio_categorias_novas()
    
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
    
    # 🆕 AVISOS SOBRE DEPENDÊNCIAS
    print(f"\n🔔 AVISOS IMPORTANTES:")
    print(f"   • Funções GPU requerem hardware NVIDIA")
    print(f"   • MPI requer configuração de cluster") 
    print(f"   • Spark requer Apache Spark instalado")
    print(f"   • Stan requer compilação C++")
    print(f"   • Cython requer compilação manual")
    print(f"   • PyMC3 pode requerer Theano/PyTensor")
    
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
    print(f"\n⚡ FUNÇÕES COM DEPENDÊNCIAS ESPECIAIS:")
    print(f"   • GPU: cupy_gpu_analysis")
    print(f"   • Cluster: mpi_distributed_analysis") 
    print(f"   • Big Data: spark_big_data_analysis")
    print(f"   • Bayesiana: stan_bayesian_inference, pymc3_probabilistic_modeling")
    print(f"   • Precisão: arb_arbitrary_precision_analysis, gmpy2_multiprecision_analysis")

# =================================================================
# EXECUÇÃO
# =================================================================
if __name__ == "__main__":
    executar_consolidacao_automatica()
