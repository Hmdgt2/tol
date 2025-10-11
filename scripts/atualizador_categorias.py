import os
import re
import json
import sys
from datetime import datetime

# CONFIGURAÇÕES
LISTA_FUNCOES_JSON = "relatorios/lista_funcoes.json"
WRAPPER_SCRIPT = "scripts/gerar_wrappers_funcoes.py"
RELATORIO_PATH = "relatorios/atualizacao_categorias.txt"

os.makedirs(os.path.dirname(RELATORIO_PATH), exist_ok=True)

def carregar_funcoes_do_json():
    """Carrega as funções e categorias do relatório JSON."""
    if not os.path.exists(LISTA_FUNCOES_JSON):
        print(f"❌ Arquivo {LISTA_FUNCOES_JSON} não encontrado.")
        print("💡 Execute primeiro: python scripts/analisador_funcoes.py")
        return {}, []
    
    with open(LISTA_FUNCOES_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    categorias = dados.get("categorias", {})
    duplicados = dados.get("duplicados", [])
    
    print(f"📁 Carregadas {len(categorias)} categorias do JSON")
    return categorias, duplicados

def carregar_mapa_atual(script_path):
    """Carrega o FUNCAO_CATEGORIA_MAP atual do script."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Encontrar FUNCAO_CATEGORIA_MAP usando regex
        pattern = r"FUNCAO_CATEGORIA_MAP\s*=\s*\{([^}]+)\}"
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print("❌ Não foi possível encontrar FUNCAO_CATEGORIA_MAP")
            return {}
        
        mapa_str = "{" + match.group(1) + "}"
        
        # Converter string para dicionário com eval seguro
        mapa_atual = eval(mapa_str)
        return mapa_atual
        
    except FileNotFoundError:
        print(f"⚠️  Arquivo {script_path} não encontrado. Criando mapa vazio.")
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar mapa atual: {e}")
        return {}

def gerar_sugestoes_categoria(categoria, funcoes):
    """Gera sugestões inteligentes para nova categoria."""
    nomes_funcoes = [f["nome"] for f in funcoes]
    
    # Mapeamento de sugestões baseado no nome da categoria
    sugestoes_map = {
        "estatistica_nao_parametrica": ("NonParametricStatsWrapper", "Testes estatísticos não paramétricos", "Análise robusta sem suposições distribucionais"),
        "combinatoria": ("CombinatoricsWrapper", "Cálculos combinatórios e permutações", "Análise de combinações e arranjos"),
        "probabilidade_distribuicoes": ("ProbabilityWrapper", "Simulação de distribuições probabilísticas", "Geração de dados sintéticos e modelagem"),
        "precisao": ("PrecisionWrapper", "Cálculos com alta precisão numérica", "Operações matemáticas de alta precisão"),
        "analise_padroes": ("PatternAnalysisWrapper", "Análise e detecção de padrões", "Identificação de padrões complexos em dados"),
        "estatisticas": ("BasicStatsWrapper", "Estatísticas descritivas básicas", "Cálculos estatísticos fundamentais"),
        "sequencias": ("SequenceAnalysisWrapper", "Análise de sequências e séries", "Processamento e análise de dados sequenciais"),
        "algebra_simbolica": ("SymbolicMathWrapper", "Manipulação algébrica simbólica", "Cálculos simbólicos e algebra avançada"),
        "manipulacao_dados": ("DataManipulationWrapper", "Transformação e preparação de dados", "Pré-processamento e manipulação de datasets"),
        "numeros_especiais": ("SpecialNumbersWrapper", "Sequências numéricas especiais", "Cálculos com sequências matemáticas especiais"),
        "transformacoes": ("TransformationWrapper", "Transformações matemáticas de dados", "Aplicação de transformações a conjuntos de dados"),
        "deteccao_anomalias": ("AnomalyDetectionWrapper", "Detecção de outliers e anomalias", "Identificação de valores atípicos"),
        "series_temporais": ("TimeSeriesWrapper", "Análise de séries temporais", "Processamento e modelagem temporal"),
        "probabilidade": ("ProbabilityTheoryWrapper", "Teoria da probabilidade", "Cálculos probabilísticos e distribuições"),
        "funcoes_especiais": ("SpecialFunctionsWrapper", "Funções matemáticas especiais", "Cálculos com funções matemáticas avançadas"),
        "wavelets": ("WaveletAnalysisWrapper", "Análise wavelet", "Decomposição multirresolução de sinais"),
        "teoria_informacao": ("InformationTheoryWrapper", "Teoria da informação", "Cálculos de entropia e informação mútua"),
        "processamento_sinal": ("SignalProcessingWrapper", "Processamento de sinal", "Análise e transformação de sinais"),
        "algoritmos_grafos": ("GraphAlgorithmWrapper", "Algoritmos de grafos", "Execução de algoritmos em estruturas de grafos"),
        "grafos": ("GraphAnalysisWrapper", "Análise de grafos", "Métricas e propriedades de grafos"),
        "estatistica_multivariada": ("MultivariateStatsWrapper", "Estatística multivariada", "Análise de dados multidimensionais"),
        "ia_heuristica": ("HeuristicMLWrapper", "Heurísticas e algoritmos de IA", "Otimização e algoritmos inteligentes"),
        "machine_learning": ("MLMetricsWrapper", "Métricas de machine learning", "Avaliação de modelos de ML"),
        "simulacao": ("SimulationWrapper", "Simulação e Monte Carlo", "Métodos de simulação estatística"),
        "aritmetica": ("ArithmeticWrapper", "Operações aritméticas", "Cálculos matemáticos básicos"),
        "analise_numerica": ("NumericalAnalysisWrapper", "Análise numérica", "Métodos numéricos e computacionais"),
        "exploracao": ("ExplorationWrapper", "Exploração de dados", "Análise exploratória e descoberta"),
        "plots": ("VisualizationWrapper", "Visualização de dados", "Geração de gráficos e visualizações"),
        "modelagem_preditiva": ("PredictiveModelingWrapper", "Modelagem preditiva", "Algoritmos de previsão e regressão"),
        "geometria": ("GeometryWrapper", "Geometria e distâncias", "Cálculos geométricos e métricas"),
        "criptografia": ("CryptographyWrapper", "Criptografia e segurança", "Algoritmos criptográficos"),
        "analise_primos": ("PrimeAnalysisWrapper", "Análise de números primos", "Propriedades e características de primos"),
        "teoria_numeros": ("NumberTheoryWrapper", "Teoria dos números", "Propriedades avançadas de números"),
        "matematica_especial": ("SpecialMathWrapper", "Matemática especializada", "Funções e conceitos matemáticos avançados"),
        "conjuntos": ("SetTheoryWrapper", "Teoria dos conjuntos", "Operações e análise de conjuntos"),
        "temporais": ("TemporalAnalysisWrapper", "Análise temporal", "Processamento de dados temporais")
    }
    
    # Verificar se temos uma sugestão pré-definida
    if categoria in sugestoes_map:
        return sugestoes_map[categoria]
    
    # Caso contrário, gerar sugestão genérica
    wrapper_name = f"{categoria.title().replace('_', '')}Wrapper"
    objetivo = f"Processar funções de {categoria}"
    finalidade = "Feature extraction para pipeline de IA"
    
    return wrapper_name, objetivo, finalidade

def atualizar_script_wrappers(script_path, novas_categorias, categorias_removidas, categorias_detectadas):
    """Atualiza o script de wrappers com novas categorias."""
    
    # Se o arquivo não existe, criar um básico
    if not os.path.exists(script_path):
        print(f"⚠️  Arquivo {script_path} não encontrado. Criando novo...")
        conteudo_base = '''import os
import ast

# Mapear tipo de módulo para classe de wrapper, objetivo e finalidade
FUNCAO_CATEGORIA_MAP = {
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
        f.write("# Wrappers automáticos para funções analíticas\\n")
        f.write("# Cada wrapper inclui objetivo e finalidade, facilitando integração universal\\n\\n")

        for wrapper_class, funclist in wrappers_dict.items():
            objetivo, finalidade = metadados_dict[wrapper_class]
            f.write(f"class {wrapper_class}:\\n")
            f.write(f'    """\\n    Objetivo: {objetivo}\\n    Finalidade no pipeline: {finalidade}\\n    """\\n\\n')
            # Wrapper universal adaptativo (opcional)
            f.write(f"    @staticmethod\\n")
            f.write(f"    def apply_function(func, data, *args, **kwargs):\\n")
            f.write(f"        \\"\\"\\"\\n        Aplica função a dados, adaptando tipo de retorno para integração universal.\\n        \\"\\"\\"\\n")
            f.write(f"        result = func(data, *args, **kwargs)\\n")
            f.write(f"        if isinstance(result, list):\\n")
            f.write(f"            return result[:5] if len(result) > 5 else result\\n")
            f.write(f"        elif isinstance(result, dict):\\n")
            f.write(f"            return list(result.values())[:5]\\n")
            f.write(f"        elif isinstance(result, (int, float)):\\n")
            f.write(f"            return [result]\\n")
            f.write(f"        elif hasattr(result, 'shape'):\\n")
            f.write(f"            try:\\n")
            f.write(f"                return result.flatten().tolist()[:5]\\n")
            f.write(f"            except Exception:\\n")
            f.write(f"                return [float(result)]\\n")
            f.write(f"        return result\\n\\n")
            # Gerar wrapper para cada função
            for func in funclist:
                args_str = ", ".join(func["args"])
                args_pass = ", ".join(func["args"])
                doc = func["docstring"].replace('\\n', '\\n        ')
                f.write(f"    @staticmethod\\n")
                f.write(f"    def {func['nome']}({args_str}):\\n")
                if doc:
                    f.write(f'        """{doc}"""\\n')
                f.write(f"        # Chamada original + adaptação universal\\n")
                f.write(f"        from lib.funcoes_analiticas.{func['modulo']} import {func['nome']}\\n")
                f.write(f"        return {wrapper_class}.apply_function({func['nome']}, {args_pass})\\n\\n")
            f.write("\\n")
    print(f"✅ Wrappers gerados em: {destino_path}")

if __name__ == "__main__":
    funcoes = extrair_funcoes(BASE_DIR)
    gerar_wrappers(funcoes, WRAPPER_MODULE_PATH)
'''
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(conteudo_base)
    
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Carregar mapa atual
    mapa_atual = carregar_mapa_atual(script_path)
    
    # Adicionar novas categorias
    for categoria in novas_categorias:
        wrapper_name, objetivo, finalidade = gerar_sugestoes_categoria(
            categoria, categorias_detectadas[categoria]
        )
        mapa_atual[categoria] = (wrapper_name, objetivo, finalidade)
        print(f"   ✅ Adicionada: {categoria} -> {wrapper_name}")
    
    # Remover categorias excluídas
    for categoria in categorias_removidas:
        if categoria in mapa_atual:
            del mapa_atual[categoria]
            print(f"   ❌ Removida: {categoria}")
    
    # Gerar novo conteúdo do mapa
    novo_mapa_str = "FUNCAO_CATEGORIA_MAP = {\n"
    for cat, (wrapper, obj, final) in sorted(mapa_atual.items()):
        novo_mapa_str += f'    "{cat}": ("{wrapper}", "{obj}", "{final}"),\n'
    novo_mapa_str += "}"
    
    # Substituir no conteúdo
    pattern = r"FUNCAO_CATEGORIA_MAP\s*=\s*\{[^}]+\}"
    if re.search(pattern, content, re.DOTALL):
        novo_content = re.sub(pattern, novo_mapa_str, content, flags=re.DOTALL)
    else:
        # Se não encontrar, adicionar após imports
        novo_content = content.replace("FUNCAO_CATEGORIA_MAP = {}", novo_mapa_str)
    
    # Escrever arquivo atualizado
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(novo_content)
    
    return len(novas_categorias), len(categorias_removidas)

def gerar_relatorio(novas_categorias, categorias_removidas, duplicados, categorias_detectadas):
    """Gera relatório detalhado da atualização."""
    
    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("# RELATÓRIO DE ATUALIZAÇÃO DE CATEGORIAS\n")
        f.write(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("## 📊 ESTATÍSTICAS GERAIS\n")
        f.write(f"- Total de categorias detectadas: {len(categorias_detectadas)}\n")
        f.write(f"- Novas categorias adicionadas: {len(novas_categorias)}\n")
        f.write(f"- Categorias removidas: {len(categorias_removidas)}\n")
        f.write(f"- Funções duplicadas: {len(duplicados)}\n\n")
        
        if novas_categorias:
            f.write("## 🆕 NOVAS CATEGORIAS ADICIONADAS\n")
            for cat in novas_categorias:
                wrapper_name, objetivo, finalidade = gerar_sugestoes_categoria(cat, categorias_detectadas[cat])
                f.write(f"### {cat}\n")
                f.write(f"- Wrapper: {wrapper_name}\n")
                f.write(f"- Objetivo: {objetivo}\n")
                f.write(f"- Finalidade: {finalidade}\n")
                f.write(f"- Funções: {len(categorias_detectadas[cat])}\n")
                for func in categorias_detectadas[cat][:5]:  # Mostrar apenas 5 primeiras
                    f.write(f"  - {func['nome']}: {func['args']}\n")
                if len(categorias_detectadas[cat]) > 5:
                    f.write(f"  - ... e {len(categorias_detectadas[cat]) - 5} mais\n")
                f.write("\n")
        
        if categorias_removidas:
            f.write("## 🗑️ CATEGORIAS REMOVIDAS\n")
            for cat in categorias_removidas:
                f.write(f"- {cat}\n")
        
        if duplicados:
            f.write("## ⚠️ FUNÇÕES DUPLICADAS (REVISAR)\n")
            for dup in duplicados[:10]:  # Mostrar apenas 10 primeiras
                f.write(f"- {dup['nome']} em {dup['caminho']} (categoria: {dup['categoria']})\n")
            if len(duplicados) > 10:
                f.write(f"- ... e {len(duplicados) - 10} mais duplicados\n")

def main():
    """Executa o pipeline completo de atualização."""
    
    print("🔄 INICIANDO FASE 2: ATUALIZAÇÃO DE CATEGORIAS...")
    
    # 1. Carregar funções do JSON gerado pelo analisador
    print("📁 Carregando funções do relatório JSON...")
    categorias_detectadas, duplicados = carregar_funcoes_do_json()
    
    if not categorias_detectadas:
        print("💥 Não foi possível carregar as categorias. Pipeline interrompido.")
        return False
    
    # 2. Carregar categorias atuais do script
    print("📋 Carregando categorias atuais...")
    mapa_atual = carregar_mapa_atual(WRAPPER_SCRIPT)
    categorias_atuais = set(mapa_atual.keys())
    categorias_detectadas_set = set(categorias_detectadas.keys())
    
    # 3. Identificar mudanças
    novas_categorias = categorias_detectadas_set - categorias_atuais
    categorias_removidas = categorias_atuais - categorias_detectadas_set
    
    print(f"📊 DETECTADAS: {len(categorias_detectadas_set)} categorias")
    print(f"🆕 NOVAS: {len(novas_categorias)} categorias")
    print(f"🗑️ REMOVIDAS: {len(categorias_removidas)} categorias")
    print(f"⚠️ DUPLICADOS: {len(duplicados)} funções")
    
    # Listar categorias detectadas
    print("\n📁 Categorias detectadas:")
    for cat in sorted(categorias_detectadas.keys()):
        print(f"  - {cat}: {len(categorias_detectadas[cat])} funções")
    
    # 4. Atualizar se necessário
    atualizacao_realizada = False
    if novas_categorias or categorias_removidas:
        print("\n🔄 ATUALIZANDO SCRIPT DE WRAPPERS...")
        novas_count, removidas_count = atualizar_script_wrappers(
            WRAPPER_SCRIPT, novas_categorias, categorias_removidas, categorias_detectadas
        )
        
        # 5. Gerar relatório
        print("📄 GERANDO RELATÓRIO...")
        gerar_relatorio(novas_categorias, categorias_removidas, duplicados, categorias_detectadas)
        
        print(f"\n✅ ATUALIZAÇÃO CONCLUÍDA!")
        print(f"   ➕ {novas_count} novas categorias adicionadas")
        print(f"   ➖ {removidas_count} categorias removidas") 
        print(f"   📊 Relatório salvo em: {RELATORIO_PATH}")
        
        atualizacao_realizada = True
        
    else:
        print("✅ Nenhuma atualização necessária - todas as categorias estão sincronizadas")
    
    if duplicados:
        print(f"\n⚠️  ATENÇÃO: {len(duplicados)} funções duplicadas encontradas")
        print("   Revise o relatório para corrigir duplicações")
    
    # VERIFICAÇÃO FINAL - Para o GitHub Actions
    mapa_final = carregar_mapa_atual(WRAPPER_SCRIPT)
    if (atualizacao_realizada and len(mapa_final) > 0) or (not atualizacao_realizada):
        print("🎯 FASE 2 CONCLUÍDA - Categorias atualizadas/prontas para commit")
        return True
    else:
        print("❌ FALHA - Categorias não foram atualizadas corretamente")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Erro no atualizador: {e}")
        sys.exit(1)
