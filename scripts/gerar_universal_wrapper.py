import os
import re

def gerar_universal_wrapper():
    """Gera UniversalWrapper único importando todos os wrappers por categoria."""
    
    # Template do UniversalWrapper
    template = '''"""
UNIVERSAL WRAPPER - Interface única para todas as funções analíticas
============================================================

Gerado automaticamente por gerar_universal_wrapper.py
NÃO EDITAR MANUALMENTE - Este arquivo será sobrescrito.

Fornece acesso unificado a todas as 154+ funções através de uma única interface.
Ideal para uso em algoritmos genéticos e ML que precisam compor funções livremente.
"""

class UniversalWrapper:
    """
    Wrapper único com acesso a todas as funções analíticas.
    
    Objetivo: Fornecer interface padronizada para composição de heurísticas
    Finalidade: Permitir que algoritmos genéticos/ML combinem funções livremente
    
    Características:
    - Todas as funções retornam List[float] padronizada
    - Tratamento automático de erros
    - Interface consistente para o pipeline de IA
    """
    
    # Métodos serão adicionados dinamicamente abaixo
    pass

# ========== IMPORTAÇÃO DINÂMICA DE TODOS OS WRAPPERS ==========

'''
    
    # Ler o arquivo de wrappers gerado para extrair todas as funções
    wrappers_file = "lib/funcoes_wrappers_auto.py"
    
    if not os.path.exists(wrappers_file):
        print("❌ Arquivo de wrappers não encontrado. Execute gerar_wrappers_funcoes.py primeiro.")
        return
    
    with open(wrappers_file, "r", encoding="utf-8") as f:
        wrappers_content = f.read()
    
    # Extrair todas as classes de wrapper e seus métodos
    classes = re.findall(r'class (\w+Wrapper):.*?(?=class|\Z)', wrappers_content, re.DOTALL)
    
    universal_methods = []
    imports_set = set()
    
    for class_block in classes:
        # Extrair nome da classe
        class_match = re.match(r'class (\w+Wrapper)', class_block)
        if not class_match:
            continue
            
        class_name = class_match.group(1)
        
        # Extrair métodos estáticos desta classe
        methods = re.findall(r'@staticmethod\s+def (\w+)\([^)]*\):\s*""".*?""".*?return (\w+)\.apply_function\((\w+),', class_block, re.DOTALL)
        
        for method_name, wrapper_class, original_func in methods:
            # Criar método no UniversalWrapper
            method_code = f'''
    @staticmethod
    def {method_name}(*args, **kwargs):
        """Wrapper para {method_name} - via {wrapper_class}"""
        from lib.funcoes_wrappers_auto import {wrapper_class}
        return {wrapper_class}.{method_name}(*args, **kwargs)
'''
            universal_methods.append(method_code)
            imports_set.add(wrapper_class)
    
    # Gerar imports
    imports_code = "\n".join([f"from lib.funcoes_wrappers_auto import {cls}" for cls in sorted(imports_set)])
    
    # Arquivo final
    final_content = template + imports_code + "\n\n" + "\n".join(universal_methods)
    
    # Adicionar método de utilidade
    final_content += '''
    
    @staticmethod
    def get_available_functions():
        """Retorna lista de todas as funções disponíveis no wrapper."""
        return [method for method in dir(UniversalWrapper) 
                if not method.startswith('_') and callable(getattr(UniversalWrapper, method))]
    
    @staticmethod
    def get_function_count():
        """Retorna o número total de funções disponíveis."""
        return len([method for method in dir(UniversalWrapper) 
                   if not method.startswith('_') and callable(getattr(UniversalWrapper, method))])

# ========== EXEMPLO DE USO ==========

if __name__ == "__main__":
    # Teste básico do UniversalWrapper
    print(f"🔧 UniversalWrapper carregado com {UniversalWrapper.get_function_count()} funções")
    
    # Exemplo de uso
    dados = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Usando diferentes funções através da mesma interface
    resultado_fft = UniversalWrapper.fft_magnitude(dados)
    resultado_primes = UniversalWrapper.count_primes(dados)
    resultado_mean = UniversalWrapper.rolling_mean(dados, 3)
    
    print(f"📊 FFT: {resultado_fft}")
    print(f"🔢 Primos: {resultado_primes}") 
    print(f"📈 Média móvel: {resultado_mean}")
    
    print("✅ UniversalWrapper pronto para uso no pipeline!")
'''
    
    # Escrever arquivo
    output_path = "lib/universal_wrapper.py"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ UniversalWrapper gerado em: {output_path}")
    print(f"📊 Total de funções incluídas: {len(universal_methods)}")

def main():
    """Executa a geração do UniversalWrapper."""
    print("🚀 Gerando UniversalWrapper único...")
    gerar_universal_wrapper()
    print("🎯 Próximo passo: Implementar gerador_logicas.py")

if __name__ == "__main__":
    main()
