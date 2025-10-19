# scripts/corrigir_sintaxe_final.py
import ast
import os
import re
from pathlib import Path

def diagnosticar_e_corrigir_erros():
    """Diagnostica e corrige todos os erros de sintaxe reportados"""
    
    problemas = {
        'sistemas_dinamicos_avancados.py': 18,
        'estatistica_multivariada_2.py': 34,
        'modelagem_probabilistica.py': 20,
        'geometria_computacional.py': 40
    }
    
    staging_dir = Path('lib/funcoes_limpas')
    correcoes_aplicadas = {}
    
    print("🔧 CORRETOR DE SINTAXE AUTOMÁTICO")
    print("=" * 50)
    
    for arquivo, linha_problema in problemas.items():
        caminho = staging_dir / arquivo
        if not caminho.exists():
            print(f"❌ {arquivo}: Arquivo não encontrado")
            continue
            
        print(f"\n📝 Corrigindo {arquivo}...")
        
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            # CORREÇÕES ESPECÍFICAS BASEADAS NOS PADRÕES IDENTIFICADOS
            conteudo_corrigido = aplicar_correcoes_gerais(conteudo)
            
            # Validar se a correção funcionou
            try:
                ast.parse(conteudo_corrigido)
                with open(caminho, 'w', encoding='utf-8') as f:
                    f.write(conteudo_corrigido)
                print(f"   ✅ {arquivo}: Sintaxe corrigida com sucesso")
                correcoes_aplicadas[arquivo] = True
            except SyntaxError as e:
                print(f"   ❌ {arquivo}: Ainda com erro - {e}")
                correcoes_aplicadas[arquivo] = False
                
        except Exception as e:
            print(f"   💥 {arquivo}: Erro inesperado - {e}")
            correcoes_aplicadas[arquivo] = False
    
    return correcoes_aplicadas

def aplicar_correcoes_gerais(conteudo):
    """Aplica correções gerais para problemas comuns do ASTConsolidator"""
    
    correcoes = [
        # Problema: Imports relativos mal formatados
        (r'from\s+\.\.\s*import', 'from .. import'),
        (r'import\s+\.\.', '# import .. removido'),
        
        # Problema: Parênteses desbalanceados
        (r'\(\s*,\s*', '('),
        (r',\s*\)', ')'),
        
        # Problema: Strings quebradas incorretamente
        (r"'\s*\+\s*'", ''),
        
        # Problema: Decoradores mal formatados
        (r'@\s+', '@'),
        
        # Problema: Imports duplicados
        (r'import\s+(\w+)\s*\n\s*import\s+\1', r'import \1'),
        
        # Problema: Type hints mal formatados
        (r':\s*:\s*', ': '),
        (r'->\s*->', '->'),
        
        # Problema: Chamadas de função vazias
        (r'\(\s*\)\s*\.', '().'),
        
        # Problema: Matrizes/vetores mal formatados
        (r'\[\s*,\s*', '['),
        (r',\s*\]', ']'),
    ]
    
    for padrao, substituicao in correcoes:
        conteudo = re.sub(padrao, substituicao, conteudo)
    
    return conteudo

def validar_todas_correcoes():
    """Valida se todos os arquivos têm sintaxe correta"""
    
    staging_dir = Path('lib/funcoes_limpas')
    arquivos_problematicos = [
        'sistemas_dinamicos_avancados.py',
        'estatistica_multivariada_2.py',
        'modelagem_probabilistica.py',
        'geometria_computacional.py'
    ]
    
    print("\n✅ VALIDAÇÃO FINAL DA SINTAXE")
    print("=" * 50)
    
    todos_validos = True
    for arquivo in arquivos_problematicos:
        caminho = staging_dir / arquivo
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                codigo = f.read()
            ast.parse(codigo)
            print(f"   ✅ {arquivo}: VÁLIDO")
        except SyntaxError as e:
            print(f"   ❌ {arquivo}: INVÁLIDO - {e}")
            todos_validos = False
    
    return todos_validos

def main():
    """Executa o processo completo de correção"""
    print("🛠️  EXECUTANDO CORREÇÃO DE SINTAXE DEFINITIVA")
    print("=" * 60)
    
    # 1. Aplicar correções
    resultados = diagnosticar_e_corrigir_erros()
    
    # 2. Validar resultados
    todos_validos = validar_todas_correcoes()
    
    # 3. Relatório final
    print("\n📊 RELATÓRIO FINAL")
    print("=" * 50)
    
    sucessos = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    
    print(f"✅ Arquivos corrigidos: {sucessos}/{total}")
    
    if todos_validos:
        print("🎉 TODOS OS ARQUIVOS ESTÃO COM SINTAXE VÁLIDA!")
        print("🚀 A biblioteca está pronta para uso!")
    else:
        print("⚠️  Alguns arquivos ainda precisam de atenção manual")

if __name__ == "__main__":
    main()
