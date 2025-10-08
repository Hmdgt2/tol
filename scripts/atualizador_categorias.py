import os
import re
import ast
from collections import defaultdict

# Configurações
BASE_DIR = "lib/funcoes_analiticas"
WRAPPER_SCRIPT = "scripts/gerar_wrappers_funcoes.py"
RELATORIO_PATH = "relatorios/atualizacao_categorias.txt"

os.makedirs(os.path.dirname(RELATORIO_PATH), exist_ok=True)

def extrair_funcoes_com_estatisticas(base_dir):
    """Extrai funções com estatísticas detalhadas por categoria."""
    resultados = []
    categorias = defaultdict(list)
    funcoes_unicas = set()
    duplicados = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                caminho = os.path.join(root, file)
                categoria = os.path.basename(os.path.dirname(caminho))
                
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=caminho)
                        for node in tree.body:
                            if isinstance(node, ast.FunctionDef):
                                nome = node.name
                                if not nome.startswith('_'):  # Ignorar funções privadas
                                    # Verificar duplicados
                                    if nome in funcoes_unicas:
                                        duplicados.append({"nome": nome, "caminho": caminho})
                                    else:
                                        funcoes_unicas.add(nome)
                                    
                                    func_data = {
                                        "nome": nome,
                                        "caminho": caminho,
                                        "categoria": categoria,
                                        "args": [a.arg for a in node.args.args],
                                        "docstring": ast.get_docstring(node) or ""
                                    }
                                    
                                    resultados.append(func_data)
                                    categorias[categoria].append(func_data)
                                
                except Exception as e:
                    print(f"❌ Erro ao processar {caminho}: {e}")
    
    return resultados, categorias, duplicados

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
        
    except Exception as e:
        print(f"❌ Erro ao carregar mapa atual: {e}")
        return {}

def gerar_sugestoes_categoria(categoria, funcoes):
    """Gera sugestões inteligentes para nova categoria."""
    # Analisar funções para gerar sugestões contextualizadas
    nomes_funcoes = [f["nome"] for f in funcoes]
    descricoes = [f["docstring"] for f in funcoes if f["docstring"]]
    
    # Keywords para inferir objetivo
    keywords = {
        'primo': 'Análise de números primos',
        'fft': 'Processamento de sinal e análise espectral', 
        'correl': 'Análise de correlações e dependências',
        'stat': 'Análise estatística',
        'dist': 'Cálculo de distâncias e métricas',
        'graph': 'Análise de grafos e redes',
        'crypto': 'Criptografia e segurança',
        'series': 'Análise de séries temporais',
        'prob': 'Probabilidade e distribuições',
        'math': 'Operações matemáticas avançadas'
    }
    
    # Inferir objetivo baseado nas funções
    objetivo = f"Processar funções de {categoria}"
    finalidade = "Feature extraction para pipeline de IA"
    
    for key, desc in keywords.items():
        if any(key in nome.lower() or any(key in doc.lower() for doc in descricoes if doc) for nome in nomes_funcoes):
            objetivo = desc
            break
    
    # Gerar nome do wrapper
    wrapper_name = f"{categoria.title().replace('_', '')}Wrapper"
    
    return wrapper_name, objetivo, finalidade

def atualizar_script_wrappers(script_path, novas_categorias, categorias_removidas, categorias_detectadas):
    """Atualiza o script de wrappers com novas categorias."""
    
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
    novo_content = re.sub(pattern, novo_mapa_str, content, flags=re.DOTALL)
    
    # Escrever arquivo atualizado
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(novo_content)
    
    return len(novas_categorias), len(categorias_removidas)

def gerar_relatorio(novas_categorias, categorias_removidas, duplicados, categorias_detectadas):
    """Gera relatório detalhado da atualização."""
    
    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("# RELATÓRIO DE ATUALIZAÇÃO DE CATEGORIAS\n")
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
                for func in categorias_detectadas[cat]:
                    f.write(f"  - {func['nome']}: {func['args']}\n")
                f.write("\n")
        
        if categorias_removidas:
            f.write("## 🗑️ CATEGORIAS REMOVIDAS\n")
            for cat in categorias_removidas:
                f.write(f"- {cat}\n")
        
        if duplicados:
            f.write("## ⚠️ FUNÇÕES DUPLICADAS (REVISAR)\n")
            for dup in duplicados:
                f.write(f"- {dup['nome']} em {dup['caminho']}\n")

def main():
    """Executa o pipeline completo de atualização."""
    
    print("🔄 INICIANDO ATUALIZAÇÃO AUTOMÁTICA DE CATEGORIAS...")
    
    # 1. Extrair funções atuais
    print("📁 Analisando biblioteca de funções...")
    funcoes, categorias_detectadas, duplicados = extrair_funcoes_com_estatisticas(BASE_DIR)
    
    # 2. Carregar categorias atuais
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
    
    # 4. Atualizar se necessário
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
        
        # 6. Sugerir próximo passo
        if novas_categorias:
            print(f"\n🎯 PRÓXIMO PASSO: Executar 'gerar_wrappers_funcoes.py' para gerar novos wrappers")
        
    else:
        print("✅ Nenhuma atualização necessária - todas as categorias estão sincronizadas")
    
    if duplicados:
        print(f"\n⚠️  ATENÇÃO: {len(duplicados)} funções duplicadas encontradas")
        print("   Revise o relatório para corrigir duplicações")

if __name__ == "__main__":
    main()
