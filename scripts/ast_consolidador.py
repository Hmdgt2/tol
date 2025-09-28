# ast_consolidador.py
import ast
import os
import astunparse

class ASTConsolidator:
    def __init__(self, target_module, source_module, base_staging_dir):
        self.base_staging_dir = base_staging_dir
        self.target_module_path = os.path.join(base_staging_dir, f"{target_module}.py")
        self.source_module_path = os.path.join(base_staging_dir, f"{source_module}.py")
        
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
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            return True
        except Exception as e:
            print(f"❌ Erro ao escrever {filepath}: {e}")
            return False

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

        # Verificar se já existe no destino
        if self._funcao_existe_no_destino(target_tree, nome_final):
            print(f"    ⚠️ '{nome_final}' já existe no destino. Eliminando duplicado da origem.")
            return self._escrever_ast(self.source_module_path, source_tree)
        
        # Renomear e adicionar ao destino
        funcao_a_mover.name = nome_final
        target_tree.body.append(funcao_a_mover)

        # Escrever ficheiros atualizados
        sucesso_origem = self._escrever_ast(self.source_module_path, source_tree)
        sucesso_destino = self._escrever_ast(self.target_module_path, target_tree)

        if sucesso_origem and sucesso_destino:
            print(f"    ✅ Sucesso: Movida para {os.path.basename(self.target_module_path)}")
            return True
        else:
            print(f"    ❌ Falha ao escrever ficheiros")
            return False
