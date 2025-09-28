#/scripts/ast_consolidador.py
import ast
import os

# Defina a pasta raiz da sua biblioteca de funções
FUNCOES_DIR = 'lib/funcoes_analiticas'

class ASTConsolidator:
    def __init__(self, target_module, source_module):
        self.target_module = os.path.join(FUNCOES_DIR, f"{target_module}.py")
        self.source_module = os.path.join(FUNCOES_DIR, f"{source_module}.py")
    
    def mover_funcao(self, func_name, nome_padrao=None):
        """
        Move a função func_name do módulo de origem para o módulo de destino.
        """
        
        # 1. Carregar e analisar o módulo de origem
        with open(self.source_module, 'r') as f:
            source_code = f.read()
            source_tree = ast.parse(source_code)
            
        # 2. Carregar e analisar o módulo de destino
        with open(self.target_module, 'r') as f:
            target_code = f.read()
            target_tree = ast.parse(target_code)
        
        # Encontra a função no módulo de origem
        funcao_a_mover = None
        novas_source_nodes = []
        
        for node in source_tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                # Função encontrada! Guarda para mover e não inclui na reescrita.
                funcao_a_mover = node
                if nome_padrao:
                    # Se houver um nome padronizado (ex: fibonacci_num), atualiza
                    funcao_a_mover.name = nome_padrao 
            else:
                # Mantém o resto do código no ficheiro de origem
                novas_source_nodes.append(node)

        if not funcao_a_mover:
            print(f"❌ Erro: Função '{func_name}' não encontrada em {self.source_module}")
            return False

        # 3. Adiciona a função ao módulo de destino
        target_tree.body.append(funcao_a_mover)
        
        # 4. Reescreve os ficheiros (usando um 'unparser' para converter AST de volta a código)
        
        try:
            # Requer uma biblioteca auxiliar para converter AST para código
            # (Exemplo simplificado, na vida real usaria 'astunparse' ou 'gast')
            
            # ATENÇÃO: A conversão de AST para código é complexa e requer uma biblioteca externa.
            # Este código é apenas conceitual para focar na lógica.
            
            # Reescreve o ficheiro de destino com a nova função
            # novo_target_code = ast_unparse(target_tree)
            # with open(self.target_module, 'w') as f: f.write(novo_target_code)
            
            # Reescreve o ficheiro de origem sem a função movida
            # novo_source_code = ast_unparse(ast.Module(body=novas_source_nodes, type_ignores=[]))
            # with open(self.source_module, 'w') as f: f.write(novo_source_code)

            print(f"✅ Movido/Consolidado: '{func_name}' de {self.source_module} para {self.target_module}")
            return True

        except Exception as e:
            print(f"❌ ERRO na reescrita de código: {e}")
            return False


# EXEMPLO DE USO (Conceitual):
# consolidator = ASTConsolidator('estatisticas', 'conjuntos')
# consolidator.mover_funcao('intersection')
# consolidator.mover_funcao('fibonacci', 'fibonacci_num') # Renomeia e move
