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
    "estatistica_nao_parametrica": ("NonParametricStatsWrapper", "Aplicar testes estatísticos não paramétricos", "Análise robusta sem suposições distribucionais"),
    "probabilidade_distribuicoes": ("ProbabilityWrapper", "Modelar distribuições e simular probabilidades", "Análise probabilística e geração sintética"),
    "precisao": ("PrecisionWrapper", "Executar cálculos com alta precisão numérica", "Cálculos críticos onde precisão é essencial"),
    "analise_padroes": ("PatternAnalysisWrapper", "Detectar e analisar padrões complexos em dados", "Feature extraction para reconhecimento de padrões"),
    "estatisticas": ("BasicStatsWrapper", "Calcular estatísticas descritivas básicas", "Features fundamentais para análise exploratória"),
    "sequencias": ("SequenceAnalysisWrapper", "Analisar propriedades e transformações de sequências", "Feature extraction temporal e sequencial"),
    "algebra_simbolica": ("SymbolicMathWrapper", "Realizar operações de álgebra simbólica", "Manipulação matemática avançada e simbólica"),
    "manipulacao_dados": ("DataManipulationWrapper", "Preprocessar e transformar dados", "Preparação de dados para ML e análise"),
    "numeros_especiais": ("SpecialNumbersWrapper", "Trabalhar com sequências numéricas especiais", "Features matemáticas baseadas em sequências conhecidas"),
    "transformacoes": ("TransformationWrapper", "Aplicar transformações matemáticas a dados", "Feature engineering via transformações"),
    "deteccao_anomalias": ("AnomalyDetectionWrapper", "Identificar outliers e anomalias em dados", "Detecção de valores atípicos para limpeza e análise"),
    "series_temporais": ("TimeSeriesAnalysisWrapper", "Analisar e modelar séries temporais", "Feature extraction e previsão temporal"),
    "probabilidade": ("ProbabilityTheoryWrapper", "Calcular distribuições e medidas probabilísticas", "Análise estatística baseada em probabilidade"),
    "funcoes_especiais": ("SpecialFunctionsWrapper", "Utilizar funções matemáticas especiais", "Cálculos avançados com funções especializadas"),
    "wavelets": ("WaveletAnalysisWrapper", "Aplicar análise wavelet a sinais", "Decomposição multirresolução de sinais"),
    "teoria_informacao": ("InformationTheoryWrapper", "Calcular medidas de teoria da informação", "Análise de entropia, informação mútua e complexidade"),
}

BASE_DIR = "lib/funcoes_analiticas"
WRAPPER_MODULE_PATH = "lib/funcoes_wrappers_auto.py"

def categoria_objetivo_finalidade(caminho):
    """Determina a categoria, objetivo e finalidade com base no caminho do arquivo."""
    partes = caminho.split("/")
    if len(partes) >= 2:
        modulo = partes[-2]  # Pasta contendo o arquivo
    else:
        modulo = "generic"
    return FUNCAO_CATEGORIA_MAP.get(modulo, ("GenericFeatureWrapper", "Transformação genérica", "Integração universal para pipeline de IA"))

def extrair_funcoes(base_dir):
    """Extrai todas as funções dos arquivos Python no diretório base."""
    resultados = []
    total_arquivos = 0
    total_funcoes = 0
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                caminho = os.path.join(root, file)
                modulo = os.path.basename(caminho).replace(".py", "")
                total_arquivos += 1
                
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=caminho)
                        for node in tree.body:
                            if isinstance(node, ast.FunctionDef):
                                nome = node.name
                                if not nome.startswith('_'):  # Ignorar funções privadas
                                    args = [a.arg for a in node.args.args]
                                    docstring = ast.get_docstring(node) or ""
                                    resultados.append({
                                        "nome": nome,
                                        "caminho": caminho,
                                        "modulo": modulo,
                                        "args": args,
                                        "docstring": docstring
                                    })
                                    total_funcoes += 1
                except Exception as e:
                    print(f"❌ Erro ao processar {caminho}: {e}")
    
    print(f"📊 Processados {total_arquivos} arquivos, encontradas {total_funcoes} funções")
    return resultados

def gerar_wrappers(funcoes, destino_path):
    """Gera os wrappers automáticos organizados por categoria."""
    # Agrupar por classe de wrapper
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
        f.write('''"""
Wrappers Automáticos para Funções Analíticas
============================================

Gerado automaticamente por scripts/gerar_wrappers_funcoes.py

Cada wrapper inclui:
- Objetivo específico da categoria
- Finalidade no pipeline de IA/heurísticas
- Adaptação universal de tipos de retorno
- Metadados para documentação automática

⚠️ NÃO EDITAR MANUALMENTE - Este arquivo será sobrescrito na próxima geração.
"""

import numpy as np
import pandas as pd
from typing import Union, List, Any, Optional

''')

        f.write("# ========== WRAPPERS POR CATEGORIA ==========\n\n")
        
        for wrapper_class, funclist in wrappers_dict.items():
            objetivo, finalidade = metadados_dict[wrapper_class]
            
            # Header da classe
            f.write(f"class {wrapper_class}:\n")
            f.write(f'    """\n')
            f.write(f'    {wrapper_class}\n')
            f.write(f'    {"=" * len(wrapper_class)}\n')
            f.write(f'    \n')
            f.write(f'    Objetivo: {objetivo}\n')
            f.write(f'    Finalidade no pipeline: {finalidade}\n')
            f.write(f'    \n')
            f.write(f'    Funções disponíveis: {len(funclist)}\n')
            f.write(f'    """\n\n')
            
            # Wrapper universal adaptativo
            f.write('    @staticmethod\n')
            f.write('    def apply_function(func, data, *args, **kwargs):\n')
            f.write('        """\n')
            f.write('        Aplica função a dados, adaptando tipo de retorno para integração universal.\n')
            f.write('        \n')
            f.write('        Args:\n')
            f.write('            func: Função a ser aplicada\n')
            f.write('            data: Dados de entrada\n')
            f.write('            *args: Argumentos posicionais adicionais\n')
            f.write('            **kwargs: Argumentos nomeados adicionais\n')
            f.write('            \n')
            f.write('        Returns:\n')
            f.write('            List[Any]: Resultado padronizado para integração no pipeline\n')
            f.write('        """\n')
            f.write('        try:\n')
            f.write('            result = func(data, *args, **kwargs)\n')
            f.write('            \n')
            f.write('            # Caso especial: funções que já retornam lista padronizada\n')
            f.write('            if hasattr(result, "__is_wrapped__"):\n')
            f.write('                return result\n')
            f.write('                \n')
            f.write('            if isinstance(result, (list, tuple)):\n')
            f.write('                return list(result)[:10]  # Limite razoável para contexto\n')
            f.write('                \n')
            f.write('            elif isinstance(result, dict):\n')
            f.write('                return list(result.values())[:10]\n')
            f.write('                \n')
            f.write('            elif isinstance(result, (int, float)):\n')
            f.write('                return [float(result)]\n')
            f.write('                \n')
            f.write('            elif isinstance(result, complex):\n')
            f.write('                return [result.real, result.imag]\n')
            f.write('                \n')
            f.write('            elif hasattr(result, "shape"):  # numpy arrays, pandas Series\n')
            f.write('                flattened = result.flatten() if hasattr(result, "flatten") else result\n')
            f.write('                return flattened.tolist()[:10]\n')
            f.write('                \n')
            f.write('            elif result is None:\n')
            f.write('                return []\n')
            f.write('                \n')
            f.write('            elif isinstance(result, (str, bool)):\n')
            f.write('                return [str(result)]\n')
            f.write('                \n')
            f.write('            else:\n')
            f.write('                # Fallback: converter para string e limitar\n')
            f.write('                return [str(result)[:100]]\n')
            f.write('                \n')
            f.write('        except Exception as e:\n')
            f.write('            # Retorna erro de forma padronizada\n')
            f.write('            return [f"ERROR: {type(e).__name__}: {str(e)[:50]}"]\n')
            f.write('\n')
            
            # Gerar wrapper para cada função
            for func in funclist:
                args_str = ", ".join(func["args"])
                args_pass = ", ".join(func["args"])
                doc = func["docstring"]
                
                f.write(f"    @staticmethod\n")
                f.write(f"    def {func['nome']}({args_str}):\n")
                f.write(f'        """\n')
                if doc:
                    # Preservar formatação original do docstring
                    for line in doc.split('\n'):
                        f.write(f'        {line}\n')
                f.write(f'        \n')
                f.write(f'        Categoria: {wrapper_class}\n')
                f.write(f'        Módulo: {func["modulo"]}\n')
                f.write(f'        """\n')
                f.write(f"        from lib.funcoes_analiticas.{func['modulo']} import {func['nome']}\n")
                f.write(f"        return {wrapper_class}.apply_function({func['nome']}, {args_pass})\n")
                f.write("\n")
            
            f.write("\n" + "#" * 80 + "\n\n")
    
    # Estatísticas finais
    total_wrappers = sum(len(funclist) for funclist in wrappers_dict.values())
    print(f"✅ Wrappers gerados em: {destino_path}")
    print(f"📈 Estatísticas:")
    print(f"   └── Categorias: {len(wrappers_dict)}")
    print(f"   └── Wrappers criados: {total_wrappers}")
    
    # Listar categorias com contagem
    for wrapper_class, funclist in wrappers_dict.items():
        print(f"   └── {wrapper_class}: {len(funclist)} funções")

def main():
    """Função principal com tratamento robusto de erros."""
    try:
        print("🚀 Iniciando geração de wrappers automáticos...")
        
        if not os.path.exists(BASE_DIR):
            print(f"❌ Diretório base não encontrado: {BASE_DIR}")
            return
        
        funcoes = extrair_funcoes(BASE_DIR)
        
        if not funcoes:
            print("❌ Nenhuma função encontrada para processar")
            return
            
        # Criar diretório de destino se não existir
        os.makedirs(os.path.dirname(WRAPPER_MODULE_PATH), exist_ok=True)
        
        gerar_wrappers(funcoes, WRAPPER_MODULE_PATH)
        
        print("🎉 Geração concluída com sucesso!")
        
    except Exception as e:
        print(f"💥 Erro crítico durante a geração: {e}")
        raise

if __name__ == "__main__":
    main()
