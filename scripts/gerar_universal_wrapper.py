#!/usr/bin/env python3
"""
GERADOR DE UNIVERSAL WRAPPER
Gera wrapper único a partir dos wrappers por categoria gerados anteriormente
"""

import os
import re
import ast
import sys
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
    
    # DEBUG: Ver o conteúdo do arquivo
    print(f"📄 Tamanho do arquivo de wrappers: {len(wrappers_content)} bytes")
    
    # Extrair todas as classes - método mais robusto
    classes = re.findall(r'class (\w+Wrapper):.*?(?=class|\Z)', wrappers_content, re.DOTALL)
    
    print(f"🔍 Encontradas {len(classes)} classes de wrapper")
    
    universal_methods = []
    imports_set = set()
    total_funcoes = 0
    
    for class_block in classes:
        class_match = re.match(r'class (\w+Wrapper)', class_block)
        if not class_match:
            continue
            
        class_name = class_match.group(1)
        imports_set.add(class_name)
        print(f"📦 Processando classe: {class_name}")
        
        # Extrair métodos - método mais simples e direto
        method_matches = re.findall(r'@staticmethod\s+def (\w+)\([^)]*\):', class_block)
        
        for method_name in method_matches:
            if not method_name.startswith('_'):
                # Criar método no UniversalWrapper
                method_template = f'''
    @staticmethod
    def {method_name}(*args, **kwargs):
        """Método universal para {method_name}"""
        from lib.funcoes_wrappers_auto import {class_name}
        return {class_name}.{method_name}(*args, **kwargs)
'''
                universal_methods.append(method_template)
                total_funcoes += 1
                print(f"   ✅ Adicionado método: {method_name}")
    
    if total_funcoes == 0:
        print("❌ Nenhuma função encontrada nos wrappers")
        print("🔍 Tentando método alternativo de extração...")
        
        # Método alternativo: procurar diretamente por métodos
        all_methods = re.findall(r'def (\w+)\([^)]*\):', wrappers_content)
        unique_methods = set([m for m in all_methods if not m.startswith('_')])
        
        print(f"🔍 Métodos encontrados (alternativo): {len(unique_methods)}")
        for method in sorted(unique_methods)[:10]:  # Mostrar primeiros 10
            print(f"   - {method}")
        
        if unique_methods:
            # Se encontrou métodos, criar UniversalWrapper básico
            class_name = "FuncoesAnaliticasWrapper"  # Assumir nome padrão
            imports_set.add(class_name)
            
            for method_name in sorted(unique_methods):
                method_template = f'''
    @staticmethod
    def {method_name}(*args, **kwargs):
        """Método universal para {method_name}"""
        from lib.funcoes_wrappers_auto import {class_name}
        return {class_name}.{method_name}(*args, **kwargs)
'''
                universal_methods.append(method_template)
                total_funcoes += 1
            
            print(f"🔄 Criado UniversalWrapper com {total_funcoes} métodos (método alternativo)")
    
    if total_funcoes == 0:
        print("❌ FALHA CRÍTICA - Não foi possível extrair nenhuma função")
        return False
    
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

def main():
    """Executa a geração do UniversalWrapper."""
    print("🔄 INICIANDO FASE 4: GERAÇÃO DO UNIVERSAL WRAPPER...")
    
    try:
        success = gerar_universal_wrapper()
        
        # VERIFICAÇÃO FINAL - Para o GitHub Actions
        if success and os.path.exists("lib/universal_wrapper.py"):
            file_size = os.path.getsize("lib/universal_wrapper.py")
            print(f"🎯 FASE 4 CONCLUÍDA - UniversalWrapper gerado ({file_size} bytes) pronto para commit")
            return True
        else:
            print("❌ FALHA - UniversalWrapper não foi gerado")
            return False
            
    except Exception as e:
        print(f"💥 Erro no gerador de UniversalWrapper: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
