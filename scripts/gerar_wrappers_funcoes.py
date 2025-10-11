import os
import ast
import sys

# Mapear tipo de módulo para classe de wrapper, objetivo e finalidade
FUNCAO_CATEGORIA_MAP = {
    "algebra_linear": ("AlgebraLinearWrapper", "Processar funções de algebra_linear", "Feature extraction para pipeline de IA"),
    "algebra_simbolica": ("SymbolicMathWrapper", "Manipulação algébrica simbólica", "Cálculos simbólicos e algebra avançada"),
    "algoritmos_grafos": ("GraphAlgorithmWrapper", "Executar algoritmos sobre grafos (caminhos, conectividade, ciclos)", "Heurísticas baseadas em conectividade e estrutura"),
    "analise_numerica": ("NumericalAnalysisWrapper", "Transformações e análises numéricas especializadas", "Features de análise numérica e filtragem robusta"),
    "analise_padroes": ("PatternAnalysisWrapper", "Análise e detecção de padrões", "Identificação de padrões complexos em dados"),
    "analise_primos": ("PrimeAnalysisWrapper", "Explorar propriedades e padrões de números primos", "Features matemáticas e filtragem por primos"),
    "aritmetica": ("ArithmeticWrapper", "Realizar operações aritméticas básicas e avançadas", "Composição de features simples ou pré-processamento"),
    "combinatoria": ("CombinatoricsWrapper", "Avaliar agrupamentos, combinações e permutações", "Features de grupos e filtragem combinatória"),
    "combinatoria_avancada": ("AdvancedCombinatoricsWrapper", "Explorar relações avançadas entre combinações e permutações", "Features avançadas para ML ou heurísticas complexas"),
    "conjuntos": ("SetFeatureWrapper", "Processar relações entre conjuntos (interseção, união, espelho, contagem)", "Feature extraction e filtragem lógica"),
    "criptografia": ("CryptoWrapper", "Segurança, aleatoriedade, geração de chaves", "Heurísticas de randomização ou proteção"),
    "deteccao_anomalias": ("AnomalyDetectionWrapper", "Detecção de outliers e anomalias", "Identificação de valores atípicos"),
    "estatistica_multivariada": ("MultivariateStatsWrapper", "Avaliar dependências, variância, clustering e desigualdade", "Feature extraction e validação de heurísticas"),
    "estatistica_nao_parametrica": ("NonParametricStatsWrapper", "Testes estatísticos não paramétricos", "Análise robusta sem suposições distribucionais"),
    "estatisticas": ("BasicStatsWrapper", "Estatísticas descritivas básicas", "Cálculos estatísticos fundamentais"),
    "exploracao": ("ExplorationWrapper", "Explorar tendências, diferenças e padrões de listas", "Features exploratórias para detecção de padrões"),
    "funcoes_especiais": ("SpecialFunctionsWrapper", "Funções matemáticas especiais", "Cálculos com funções matemáticas avançadas"),
    "geometria": ("DistanceWrapper", "Calcular distâncias e medidas geométricas", "Features espaciais e agrupamentos"),
    "grafos": ("GraphStatsWrapper", "Extrair métricas de grafos (centralidade, densidade, triângulos, etc)", "Feature extraction e avaliação de padrões estruturais"),
    "ia_heuristica": ("HeuristicMLWrapper", "Compor heurísticas, testar, evoluir e ranquear heurísticas", "Avaliação, recombinação e evolução automática via ML/genético"),
    "machine_learning": ("MLMetricWrapper", "Avaliar desempenho de heurísticas/modelos (MSE, RMSE, accuracy, etc)", "Seleção e evolução automática de heurísticas/modelos"),
    "manipulacao_dados": ("DataManipulationWrapper", "Transformação e preparação de dados", "Pré-processamento e manipulação de datasets"),
    "matematica_especial": ("SpecialMathWrapper", "Explorar padrões avançados com funções especiais (Gamma, Beta, Bessel, Airy, etc)", "Extração de features matemáticas não triviais"),
    "modelagem_preditiva": ("PredictiveModelWrapper", "Modelar e prever usando regressão (linear, polinomial, etc)", "Predição direta e extração de coeficientes/score"),
    "numeros_especiais": ("SpecialNumbersWrapper", "Sequências numéricas especiais", "Cálculos com sequências matemáticas especiais"),
    "plots": ("VisualizationWrapper", "Gerar gráficos e visualizações para diagnóstico e debug", "Suporte visual ao pipeline e análise de heurísticas"),
    "precisao": ("PrecisionWrapper", "Cálculos com alta precisão numérica", "Operações matemáticas de alta precisão"),
    "probabilidade": ("ProbabilityTheoryWrapper", "Teoria da probabilidade", "Cálculos probabilísticos e distribuições"),
    "probabilidade_distribuicoes": ("ProbabilityWrapper", "Simulação de distribuições probabilísticas", "Geração de dados sintéticos e modelagem"),
    "processamento_sinal": ("SignalProcessingWrapper", "Extrair padrões espectrais e cíclicos (FFT, wavelet, filtros)", "Pré-processamento, compressão de dados e extração de features"),
    "sequencias": ("SequenceAnalysisWrapper", "Análise de sequências e séries", "Processamento e análise de dados sequenciais"),
    "series_temporais": ("TimeSeriesWrapper", "Análise de séries temporais", "Processamento e modelagem temporal"),
    "simulacao": ("SimulationWrapper", "Gerar dados sintéticos ou probabilísticos via Monte Carlo, MCMC", "Validação sob cenários de incerteza"),
    "temporais": ("TimeSeriesWrapper", "Detectar padrões temporais, tendências e dependências", "Feature extraction para previsões temporais ou heurísticas evolutivas"),
    "teoria_informacao": ("InformationTheoryWrapper", "Teoria da informação", "Cálculos de entropia e informação mútua"),
    "teoria_numeros": ("NumberTheoryWrapper", "Gerar features sobre propriedades numéricas (primos, fatores, totiente, etc)", "Feature extraction para ML/heurísticas matemáticas"),
    "transformacoes": ("TransformationWrapper", "Transformações matemáticas de dados", "Aplicação de transformações a conjuntos de dados"),
    "wavelets": ("WaveletAnalysisWrapper", "Análise wavelet", "Decomposição multirresolução de sinais"),
}

BASE_DIR = "lib/funcoes_analiticas"
WRAPPER_MODULE_PATH = "lib/funcoes_wrappers_auto.py"

def categoria_objetivo_finalidade(caminho):
    modulo = caminho.split("/")[-2]
    return FUNCAO_CATEGORIA_MAP.get(modulo, ("GenericFeatureWrapper", "Genérico", "Transformação genérica para integração universal"))

def extrair_funcoes(base_dir):
    resultados = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                modulo = os.path.basename(caminho).replace(".py", "")
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=caminho)
                        for node in tree.body:
                            if isinstance(node, ast.FunctionDef):
                                nome = node.name
                                args = [a.arg for a in node.args.args]
                                docstring = ast.get_docstring(node) or ""
                                resultados.append({
                                    "nome": nome,
                                    "caminho": caminho,
                                    "modulo": modulo,
                                    "args": args,
                                    "docstring": docstring
                                })
                except Exception as e:
                    print(f"Erro ao processar {caminho}: {e}")
    return resultados

def gerar_wrappers(funcoes, destino_path):
    # Primeiro, agrupar por classe de wrapper
    wrappers_dict = {}
    metadados_dict = {}
    for func in funcoes:
        wrapper_class, objetivo, finalidade = categoria_objetivo_finalidade(func["caminho"])
        if wrapper_class not in wrappers_dict:
            wrappers_dict[wrapper_class] = []
            metadados_dict[wrapper_class] = (objetivo, finalidade)
        wrappers_dict[wrapper_class].append(func)

    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(destino_path), exist_ok=True)

    # Gerar arquivo de wrappers
    with open(destino_path, "w", encoding="utf-8") as f:
        f.write("# Wrappers automáticos para funções analíticas\n")
        f.write("# Cada wrapper inclui objetivo e finalidade, facilitando integração universal\n\n")

        for wrapper_class, funclist in wrappers_dict.items():
            objetivo, finalidade = metadados_dict[wrapper_class]
            f.write(f"class {wrapper_class}:\n")
            f.write(f'    """\n    Objetivo: {objetivo}\n    Finalidade no pipeline: {finalidade}\n    """\n\n')
            # Wrapper universal adaptativo (opcional)
            f.write(f"    @staticmethod\n")
            f.write(f"    def apply_function(func, data, *args, **kwargs):\n")
            f.write(f"        \"\"\"\n        Aplica função a dados, adaptando tipo de retorno para integração universal.\n        \"\"\"\n")
            f.write(f"        result = func(data, *args, **kwargs)\n")
            f.write(f"        if isinstance(result, list):\n")
            f.write(f"            return result[:5] if len(result) > 5 else result\n")
            f.write(f"        elif isinstance(result, dict):\n")
            f.write(f"            return list(result.values())[:5]\n")
            f.write(f"        elif isinstance(result, (int, float)):\n")
            f.write(f"            return [result]\n")
            f.write(f"        elif hasattr(result, 'shape'):\n")
            f.write(f"            try:\n")
            f.write(f"                return result.flatten().tolist()[:5]\n")
            f.write(f"            except Exception:\n")
            f.write(f"                return [float(result)]\n")
            f.write(f"        return result\n\n")
            # Gerar wrapper para cada função
            for func in funclist:
                args_str = ", ".join(func["args"])
                args_pass = ", ".join(func["args"])
                doc = func["docstring"].replace('\n', '\n        ')
                f.write(f"    @staticmethod\n")
                f.write(f"    def {func['nome']}({args_str}):\n")
                if doc:
                    f.write(f'        """{doc}"""\n')
                f.write(f"        # Chamada original + adaptação universal\n")
                f.write(f"        from lib.funcoes_analiticas.{func['modulo']} import {func['nome']}\n")
                f.write(f"        return {wrapper_class}.apply_function({func['nome']}, {args_pass})\n\n")
            f.write("\n")
    print(f"✅ Wrappers gerados em: {destino_path}")

def main():
    """Função principal do gerador de wrappers."""
    print("🔄 INICIANDO FASE 3: GERAÇÃO DE WRAPPERS POR CATEGORIA...")
    
    try:
        print("📁 Extraindo funções da biblioteca...")
        funcoes = extrair_funcoes(BASE_DIR)
        
        if not funcoes:
            print("❌ Nenhuma função encontrada para processar")
            return False
            
        print(f"📊 Processando {len(funcoes)} funções...")
        gerar_wrappers(funcoes, WRAPPER_MODULE_PATH)
        
        # VERIFICAÇÃO FINAL - Para o GitHub Actions
        if os.path.exists(WRAPPER_MODULE_PATH):
            file_size = os.path.getsize(WRAPPER_MODULE_PATH)
            print(f"🎯 FASE 3 CONCLUÍDA - Wrappers gerados ({file_size} bytes) prontos para commit")
            return True
        else:
            print("❌ FALHA - Wrappers não foram gerados")
            return False
            
    except Exception as e:
        print(f"💥 Erro no gerador de wrappers: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
