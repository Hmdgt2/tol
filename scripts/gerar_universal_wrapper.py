#!/usr/bin/env python3
"""
GERADOR DE UNIVERSAL WRAPPER
Gera wrapper único a partir dos wrappers por categoria gerados anteriormente
"""

import os
import re
import ast
from datetime import datetime

def gerar_universal_wrapper():
    """Gera UniversalWrapper único baseado nos wrappers por categoria."""
    
    print("🌐 Iniciando geração do UniversalWrapper...")
    
    # Caminhos dos arquivos
    wrappers_file = "lib/funcoes_wrappers_auto.py"
    output_file = "lib/universal_wrapper.py"
    
    if not os.path.exists(wrappers_file):
        print(f"❌ Arquivo de wrappers não encontrado: {wrappers_file}")
        print("💡 Execute primeiro: python scripts/gerar_wrappers_funcoes.py")
        return False
    
    # Ler wrappers gerados
    with open(wrappers_file, "r", encoding="utf-8") as f:
        wrappers_content = f.read()
    
    # Extrair todas as classes e métodos
    classes = re.findall(r'class (\w+Wrapper):.*?(?=class|\Z)', wrappers_content, re.DOTALL)
    
    universal_methods = []
    imports_set = set()
    total_funcoes = 0
    
    for class_block in classes:
        class_match = re.match(r'class (\w+Wrapper)', class_block)
        if not class_match:
            continue
            
        class_name = class_match.group(1)
        imports_set.add(class_name)
        
        # Extrair métodos usando AST para maior precisão
        try:
            tree = ast.parse(class_block)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                            # Encontrar a linha de return no código original
                            method_code = None
                            lines = class_block.split('\n')
                            for i, line in enumerate(lines):
                                if f"def {item.name}(" in line:
                                    # Encontrar o bloco do método
                                    j = i
                                    while j < len(lines) and (lines[j].strip() or j == i):
                                        if "return" in lines[j] and class_name in lines[j]:
                                            method_code = lines[j]
                                            break
                                        j += 1
                                    break
                            
                            if method_code:
                                # Criar método no UniversalWrapper
                                method_template = f'''
    @staticmethod
    def {item.name}(*args, **kwargs):
        """Método universal para {item.name}"""
        from lib.funcoes_wrappers_auto import {class_name}
        return {class_name}.{item.name}(*args, **kwargs)
'''
                                universal_methods.append(method_template)
                                total_funcoes += 1
        except Exception as e:
            print(f"⚠️ Erro ao processar {class_name}: {e}")
            continue
    
    # Gerar conteúdo do UniversalWrapper
    template = f'''"""
UNIVERSAL WRAPPER - Interface Única para Todas as Funções
================================================================
Gerado automaticamente em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total de funções: {total_funcoes}

⚠️ NÃO EDITAR MANUALMENTE - Este arquivo é gerado automaticamente
   Qualquer alteração será sobrescrita na próxima execução do pipeline.

Fornece acesso unificado a todas as funções através de uma interface consistente.
Ideal para algoritmos genéticos e sistemas de ML que precisam compor heurísticas.
"""

import numpy as np
from typing import List, Any

class UniversalWrapper:
    """
    Wrapper único com acesso a todas as funções analíticas.
    
    Objetivo: Interface padronizada para composição de heurísticas
    Finalidade: Permitir combinação livre de funções em algoritmos genéticos/ML
    
    Características:
    - Todas as funções retornam List[float] padronizada
    - Tratamento automático de erros
    - Interface consistente para pipeline de IA
    - {total_funcoes} funções disponíveis
    """
    
    # Importações dinâmicas de todos os wrappers
'''
    
    # Adicionar imports
    imports_code = "\n".join([f"from lib.funcoes_wrappers_auto import {cls}" for cls in sorted(imports_set)])
    
    # Adicionar métodos
    methods_code = "\n".join(universal_methods)
    
    # Adicionar métodos utilitários
    util_methods = f'''
    
    @staticmethod
    def get_available_functions():
        """Retorna lista de todas as funções disponíveis."""
        return [method for method in dir(UniversalWrapper) 
                if not method.startswith('_') and callable(getattr(UniversalWrapper, method))]
    
    @staticmethod
    def get_function_count():
        """Retorna o número total de funções disponíveis."""
        return {total_funcoes}
    
    @staticmethod
    def get_function_info(func_name):
        """Retorna informações sobre uma função específica."""
        if hasattr(UniversalWrapper, func_name) and callable(getattr(UniversalWrapper, func_name)):
            return f"Função {{func_name}} disponível no UniversalWrapper"
        else:
            return f"Função {{func_name}} não encontrada"

if __name__ == "__main__":
    # Teste básico
    print(f"🔧 UniversalWrapper carregado com {{UniversalWrapper.get_function_count()}} funções")
    print("✅ UniversalWrapper pronto para uso no pipeline!")
'''
    
    # Conteúdo final
    final_content = template + imports_code + "\n" + methods_code + util_methods
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Escrever arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ UniversalWrapper gerado: {output_file}")
    print(f"📊 Total de funções incluídas: {total_funcoes}")
    print(f"📦 Wrappers importados: {len(imports_set)}")
    
    return True

if __name__ == "__main__":
    success = gerar_universal_wrapper()
    if success:
        print("🎯 Próximo passo: Implementar gerador_logicas.py")
    else:
        print("💥 Falha na geração do UniversalWrapper")
        sys.exit(1)
