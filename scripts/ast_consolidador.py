# ast_consolidador.py
import ast
import os
import astunparse
import re
from typing import Dict, List, Set, Optional

class ASTConsolidator:
    def __init__(self, target_module, source_module, base_staging_dir):
        self.base_staging_dir = base_staging_dir
        self.target_module_path = os.path.join(base_staging_dir, f"{target_module}.py")
        self.source_module_path = os.path.join(base_staging_dir, f"{source_module}.py")
        
        # 🆕 REGISTRO DE DEPENDÊNCIAS ESPECIAIS
        self.dependencias_especiais = {
            'cupy': ['cupy_gpu_analysis', 'cupy_matrix_operations', 'cupy_linear_algebra'],
            'jax': ['jax_autodiff_analysis', 'jax_hamiltonian_dynamics'],
            'mpi4py': ['mpi_distributed_analysis'],
            'pyspark': ['spark_big_data_analysis'],
            'cmdstanpy': ['stan_bayesian_inference'],
            'flint': ['arb_arbitrary_precision_analysis'],
            'gmpy2': ['gmpy2_multiprecision_analysis'],
            'symengine': ['symengine_fast_symbolic'],
            'pymc3': ['pymc3_probabilistic_modeling', 'pymc3_gaussian_process'],
            'tensorflow_probability': ['tfp_bayesian_analysis'],
            'vaex': ['vaex_lazy_dataframe_analysis'],
            'modin': ['modin_parallel_dataframe'],
            'dask_ml': ['dask_ml_distributed_learning'],
            'networkit': ['networkit_large_scale_graphs'],
            'astropy': ['astropy_astronomical_analysis'],
            'biopython': ['biopython_sequence_analysis'],
        }
        
        # 🆕 CATEGORIAS DE IMPORTS
        self.categorias_imports = {
            'computacao_gpu': ['cupy', 'cupyx'],
            'computacao_distribuida': ['mpi4py', 'pyspark', 'dask'],
            'matematica_simbolica': ['sympy', 'symengine'],
            'aprendizado_maquina': ['sklearn', 'tensorflow', 'torch'],
            'estatistica_avancada': ['pymc3', 'cmdstanpy', 'tensorflow_probability'],
            'big_data': ['vaex', 'modin', 'dask'],
            'analise_numerica': ['scipy', 'numpy', 'mpmath'],
            'visualizacao': ['matplotlib', 'seaborn', 'plotly'],
        }

    def _carregar_ast(self, filepath):
        """Carrega e retorna o AST de um ficheiro."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source_code = f.read()
                return ast.parse(source_code)
        except FileNotFoundError:
            return ast.Module(body=[], type_ignores=[])
        except Exception as e:
            print(f"❌ Erro ao carregar {filepath}: {e}")
            return None

    def _escrever_ast(self, filepath, tree):
        """Escreve o AST de volta para o ficheiro."""
        try:
            code = astunparse.unparse(tree)
            
            # 🆕 FORMATAÇÃO AUTOMÁTICA DO CÓDIGO
            code = self._formatar_codigo(code)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            return True
        except Exception as e:
            print(f"❌ Erro ao escrever {filepath}: {e}")
            return False

    def _formatar_codigo(self, code):
        """Aplica formatação básica ao código."""
        # Remove múltiplas linhas em branco
        code = re.sub(r'\n\s*\n\s*\n', '\n\n', code)
        
        # Garante 2 linhas em branco entre funções
        code = re.sub(r'(\n)(def )', r'\1\n\2', code)
        
        # Remove espaços em branco desnecessários no final das linhas
        code = '\n'.join(line.rstrip() for line in code.split('\n'))
        
        return code + '\n'  # Garante nova linha no final

    def _encontrar_e_extrair_funcao(self, tree, func_name):
        """Encontra e extrai uma função do AST, removendo-a da árvore original."""
        funcao_a_mover = None
        novos_nodes = []
        
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                funcao_a_mover = node
            else:
                novos_nodes.append(node)
        
        if funcao_a_mover:
            tree.body = novos_nodes
        
        return funcao_a_mover

    def _funcao_existe_no_destino(self, tree, func_name):
        """Verifica se a função já existe no módulo de destino."""
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                return True
        return False

    def _extrair_imports_da_funcao(self, func_node):
        """Extrai imports necessários da função."""
        imports_encontrados = set()
        
        # 🆕 Analisa o corpo da função para encontrar imports implícitos
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                # Verifica chamadas de funções de bibliotecas específicas
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        module_name = node.func.value.id
                        if module_name in self.dependencias_especiais:
                            imports_encontrados.add(module_name)
        
        return list(imports_encontrados)

    def _analisar_dependencias_funcao(self, func_node, func_name):
        """Analisa dependências específicas da função."""
        dependencias = set()
        
        # 🆕 Verifica dependências baseadas no nome da função
        for lib, funcoes in self.dependencias_especiais.items():
            if func_name in funcoes:
                dependencias.add(lib)
                print(f"    📦 Dependência detectada: {lib} para {func_name}")
        
        # 🆕 Analisa o código da função
        code = astunparse.unparse(func_node)
        
        # Padrões de detecção de bibliotecas
        padroes_dependencias = {
            'cupy': [r'cupy\.', r'cupyx\.'],
            'jax': [r'jax\.', r'jnp\.'],
            'mpi4py': [r'mpi4py', r'MPI\.'],
            'pyspark': [r'pyspark', r'SparkContext'],
            'pymc3': [r'pymc3', r'pm\.'],
            'tensorflow': [r'tensorflow', r'tf\.'],
            'torch': [r'torch', r'nn\.'],
            'dask': [r'dask\.'],
            'vaex': [r'vaex\.'],
            'modin': [r'modin\.'],
        }
        
        for lib, padroes in padroes_dependencias.items():
            for padrao in padroes:
                if re.search(padrao, code):
                    dependencias.add(lib)
        
        return list(dependencias)

    def _gerar_header_categoria(self, categoria):
        """Gera header apropriado para cada categoria de funções."""
        headers = {
            'sistemas_dinamicos_avancados': '''
# ============================================================
# SISTEMAS DINÂMICOS AVANÇADOS
# ============================================================
# Análise de sistemas não-lineares, caos e atratores
''',
            'computacao_avancada': '''
# ============================================================
# COMPUTAÇÃO AVANÇADA
# ============================================================
# GPU, paralelismo, JIT e computação distribuída
''',
            'matematica_simbolica': '''
# ============================================================
# MATEMÁTICA SIMBÓLICA
# ============================================================
# Álgebra computacional e análise simbólica
''',
            'analise_quantica': '''
# ============================================================
# ANÁLISE QUÂNTICA
# ============================================================
# Métodos inspirados em mecânica quântica
''',
            'teoria_caos': '''
# ============================================================
# TEORIA DO CAOS
# ============================================================
# Sistemas caóticos e expoentes de Lyapunov
''',
            'big_data_scaleout': '''
# ============================================================
# BIG DATA & SCALE-OUT
# ============================================================
# Processamento de dados em grande escala
''',
            'precisao_arbitraria': '''
# ============================================================
# PRECISÃO ARBITRÁRIA
# ============================================================
# Cálculos com precisão extrema (GMP/MPFR/Arb)
''',
        }
        
        return headers.get(categoria, '')

    def _adicionar_docstring_automatica(self, func_node, categoria):
        """Adiciona/atualiza docstring baseada na categoria."""
        docstring_template = self._obter_template_docstring(categoria)
        
        # Verifica se já existe docstring
        if (func_node.body and 
            isinstance(func_node.body[0], ast.Expr) and 
            isinstance(func_node.body[0].value, ast.Str)):
            # Docstring existe, adiciona categoria se não estiver presente
            docstring_atual = func_node.body[0].value.s
            if '🔬' not in docstring_atual and '🎯' not in docstring_atual:
                nova_docstring = f'{docstring_atual}\n\n{docstring_template}'
                func_node.body[0].value.s = nova_docstring
        else:
            # Adiciona nova docstring
            nova_docstring = ast.Expr(value=ast.Str(s=docstring_template))
            func_node.body.insert(0, nova_docstring)

    def _obter_template_docstring(self, categoria):
        """Retorna template de docstring baseado na categoria."""
        templates = {
            'computacao_avancada': '''
🔬 **Categoria**: Computação Avançada
🎯 **Performance**: Otimizada para GPU/Paralelismo
⚡ **Complexidade**: Alta

⚠️ **Requisitos**: Dependências especiais podem ser necessárias
''',
            'sistemas_dinamicos_avancados': '''
🔬 **Categoria**: Sistemas Dinâmicos
🎯 **Aplicação**: Análise de sistemas não-lineares
📈 **Método**: Baseado em teoria do caos

🌪️ **Sistema**: Não-linear/Dinâmico
''',
            'precisao_arbitraria': '''
🔬 **Categoria**: Precisão Arbitrária  
🎯 **Precisão**: Múltipla precisão/Arbitrária
📊 **Método**: Cálculos exatos

💎 **Garantia**: Precisão numérica rigorosa
''',
            'big_data_scaleout': '''
🔬 **Categoria**: Big Data
🎯 **Escala**: Processamento distribuído
📈 **Performance**: Otimizada para grandes volumes

🏗️ **Arquitetura**: Scale-out/Distribuída
''',
        }
        
        return templates.get(categoria, '''
🔬 **Categoria**: Função Analítica
🎯 **Propósito**: Análise de padrões matemáticos
''')

    def _organizar_imports(self, tree):
        """Organiza e categoriza imports no módulo."""
        imports = []
        outros_nodes = []
        
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(node)
            else:
                outros_nodes.append(node)
        
        if not imports:
            return tree
        
        # 🆕 Categoriza imports
        imports_categorizados = self._categorizar_imports(imports)
        
        # Reconstrói o AST com imports organizados
        tree.body = imports_categorizados + outros_nodes
        return tree

    def _categorizar_imports(self, imports):
        """Categoriza imports por tipo de biblioteca."""
        categorias = {}
        
        for imp in imports:
            categoria = self._classificar_import(imp)
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(imp)
        
        # 🆕 Adiciona headers entre categorias
        resultado = []
        ordem_categorias = [
            'bibliotecas_padrao',
            'computacao_cientifica', 
            'aprendizado_maquina',
            'computacao_avancada',
            'visualizacao',
            'outros'
        ]
        
        for cat in ordem_categorias:
            if cat in categorias and categorias[cat]:
                # Adiciona comentário de categoria
                if cat != 'bibliotecas_padrao':
                    comentario = ast.Expr(value=ast.Str(s=f'# {cat.replace("_", " ").title()}'))
                    resultado.append(comentario)
                resultado.extend(categorias[cat])
                resultado.append(ast.Pass())  # Linha em branco
        
        return resultado

    def _classificar_import(self, imp_node):
        """Classifica um import em categoria."""
        bibliotecas_cientificas = {'numpy', 'scipy', 'pandas', 'sympy', 'mpmath'}
        bibliotecas_ml = {'sklearn', 'tensorflow', 'torch', 'keras'}
        bibliotecas_avancadas = {'cupy', 'jax', 'mpi4py', 'dask', 'pyspark'}
        bibliotecas_viz = {'matplotlib', 'seaborn', 'plotly', 'bokeh'}
        
        if isinstance(imp_node, ast.Import):
            for alias in imp_node.names:
                if alias.name in bibliotecas_avancadas:
                    return 'computacao_avancada'
                elif alias.name in bibliotecas_cientificas:
                    return 'computacao_cientifica'
                elif alias.name in bibliotecas_ml:
                    return 'aprendizado_maquina'
                elif alias.name in bibliotecas_viz:
                    return 'visualizacao'
                elif '.' not in alias.name and alias.name not in {'os', 'sys', 'math'}:
                    return 'bibliotecas_padrao'
        
        return 'outros'

    def mover_funcao(self, func_name, nome_padrao=None):
        """
        Move a função func_name do módulo de origem para o módulo de destino
        dentro da área de staging.
        """
        nome_final = nome_padrao or func_name
        
        print(f"  🔧 Processando: '{func_name}' → '{nome_final}'")
        
        source_tree = self._carregar_ast(self.source_module_path)
        target_tree = self._carregar_ast(self.target_module_path)
        
        if source_tree is None or target_tree is None:
            return False

        # Extrair função da origem
        funcao_a_mover = self._encontrar_e_extrair_funcao(source_tree, func_name)
        if not funcao_a_mover:
            print(f"    ⚠️ Função '{func_name}' não encontrada em {os.path.basename(self.source_module_path)}")
            return False

        # 🆕 ANALISAR DEPENDÊNCIAS DA FUNÇÃO
        dependencias = self._analisar_dependencias_funcao(funcao_a_mover, func_name)
        if dependencias:
            print(f"    📦 Dependências detectadas: {', '.join(dependencias)}")

        # Verificar se já existe no destino
        if self._funcao_existe_no_destino(target_tree, nome_final):
            print(f"    ⚠️ '{nome_final}' já existe no destino. Eliminando duplicado da origem.")
            return self._escrever_ast(self.source_module_path, source_tree)
        
        # 🆕 ADICIONAR METADADOS À FUNÇÃO
        categoria = os.path.basename(self.target_module_path).replace('.py', '')
        self._adicionar_docstring_automatica(funcao_a_mover, categoria)
        
        # Renomear e adicionar ao destino
        funcao_a_mover.name = nome_final
        target_tree.body.append(funcao_a_mover)

        # 🆕 ORGANIZAR IMPORTS NO DESTINO
        target_tree = self._organizar_imports(target_tree)

        # Escrever ficheiros atualizados
        sucesso_origem = self._escrever_ast(self.source_module_path, source_tree)
        sucesso_destino = self._escrever_ast(self.target_module_path, target_tree)

        if sucesso_origem and sucesso_destino:
            print(f"    ✅ Sucesso: Movida para {os.path.basename(self.target_module_path)}")
            if dependencias:
                print(f"    📋 Dependências: {', '.join(dependencias)}")
            return True
        else:
            print(f"    ❌ Falha ao escrever ficheiros")
            return False

    # 🆕 MÉTODO PARA VALIDAÇÃO DE DEPENDÊNCIAS
    def validar_dependencias_modulo(self, modulo_path):
        """Valida se todas as dependências do módulo estão disponíveis."""
        tree = self._carregar_ast(modulo_path)
        if not tree:
            return False
        
        dependencias_encontradas = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        dependencias_encontradas.add(alias.name.split('.')[0])
                else:
                    dependencias_encontradas.add(node.module.split('.')[0])
        
        # Verifica disponibilidade
        dependencias_faltantes = []
        for dep in dependencias_encontradas:
            try:
                __import__(dep)
            except ImportError:
                if dep in self.dependencias_especiais:
                    dependencias_faltantes.append(dep)
        
        return dependencias_faltantes
