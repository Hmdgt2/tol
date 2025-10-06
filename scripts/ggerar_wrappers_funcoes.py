import os
import ast

# Mapear tipo de módulo para classe de wrapper, objetivo e finalidade
FUNCAO_CATEGORIA_MAP = {
    "teoria_numeros": ("NumberTheoryWrapper", "Gerar features sobre propriedades numéricas (primos, fatores, totiente, etc)", "Feature extraction para ML/heurísticas matemáticas"),
    "matematica_especial": ("SpecialMathWrapper", "Explorar padrões avançados com funções especiais (Gamma, Beta, Bessel, Airy, etc)", "Extração de features matemáticas não triviais"),
    "conjuntos": ("SetFeatureWrapper", "Processar relações entre conjuntos (interseção, união, espelho, contagem)", "Feature extraction e filtragem lógica"),
    "temporais": ("TimeSeriesWrapper", "Detectar padrões temporais, tendências e dependências", "Feature extraction para previsões temporais ou heurísticas evolutivas"),
    "processamento_sinal": ("SignalProcessingWrapper", "Extrair padrões espectrais e cíclicos (FFT, wavelet, filtros)", "Pré-processamento, compressão de dados e extração de features"),
    "algoritmos_grafos": ("GraphAlgorithmWrapper", "Executar algoritmos sobre grafos (caminhos, conectividade, ciclos)", "Heurísticas baseadas em conectividade e estrutura"),
    "grafos": ("GraphStatsWrapper", "Extrair métricas de grafos (centralidade, densidade, triângulos, etc)", "Feature extraction e avaliação de padrões estruturais"),
    "estatistica_multivariada": ("MultivariateStatsWrapper", "Avaliar dependências, variância, clustering e desigualdade", "Feature extraction e validação de heurísticas"),
    "ia_heuristica": ("HeuristicMLWrapper", "Compor heurísticas, testar, evoluir e ranquear heurísticas", "Avaliação, recombinação e evolução automática via ML/genético"),
    "machine_learning": ("MLMetricWrapper", "Avaliar desempenho de heurísticas/modelos (MSE, RMSE, accuracy, etc)", "Seleção e evolução automática de heurísticas/modelos"),
    "simulacao": ("SimulationWrapper", "Gerar dados sintéticos ou probabilísticos via Monte Carlo, MCMC", "Validação sob cenários de incerteza"),
    "combinatoria": ("CombinatoricsWrapper", "Avaliar agrupamentos, combinações e permutações", "Features de grupos e filtragem combinatória"),
    "combinatoria_avancada": ("AdvancedCombinatoricsWrapper", "Explorar relações avançadas entre combinações e permutações", "Features avançadas para ML ou heurísticas complexas"),
    "aritmetica": ("ArithmeticWrapper", "Realizar operações aritméticas básicas e avançadas", "Composição de features simples ou pré-processamento"),
    "analise_numerica": ("NumericalAnalysisWrapper", "Transformações e análises numéricas especializadas", "Features de análise numérica e filtragem robusta"),
    "exploracao": ("ExplorationWrapper", "Explorar tendências, diferenças e padrões de listas", "Features exploratórias para detecção de padrões"),
    "plots": ("VisualizationWrapper", "Gerar gráficos e visualizações para diagnóstico e debug", "Suporte visual ao pipeline e análise de heurísticas"),
    "modelagem_preditiva": ("PredictiveModelWrapper", "Modelar e prever usando regressão (linear, polinomial, etc)", "Predição direta e extração de coeficientes/score"),
    "geometria": ("DistanceWrapper", "Calcular distâncias e medidas geométricas", "Features espaciais e agrupamentos"),
    "criptografia": ("CryptoWrapper", "Segurança, aleatoriedade, geração de chaves", "Heurísticas de randomização ou proteção"),
    "analise_primos": ("PrimeAnalysisWrapper", "Explorar propriedades e padrões de números primos", "Features matemáticas e filtragem por primos"),
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

if __name__ == "__main__":
    funcoes = extrair_funcoes(BASE_DIR)
    gerar_wrappers(funcoes, WRAPPER_MODULE_PATH)
