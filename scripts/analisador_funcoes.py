import os
import ast
import json
import sys
from collections import defaultdict
from datetime import datetime

BASE_DIR = "lib/funcoes_limpas"
LISTA_FUNCOES_TXT = "relatorios/lista_funcoes.txt"
LISTA_FUNCOES_JSON = "relatorios/lista_funcoes.json"

os.makedirs(os.path.dirname(LISTA_FUNCOES_TXT), exist_ok=True)

def extrair_funcoes_com_estatisticas(base_dir):
    """Extrai funções com estatísticas detalhadas por categoria."""
    resultados = []
    categorias = defaultdict(list)
    funcoes_unicas = set()
    duplicados = []
    
    print(f"🔍 Analisando estrutura do diretório: {base_dir}")
    
    # Primeiro, verificar a estrutura de pastas
    for root, dirs, files in os.walk(base_dir):
        print(f"📁 Pasta: {root}")
        print(f"   Subpastas: {dirs}")
        print(f"   Arquivos: {[f for f in files if f.endswith('.py')]}")
        
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                caminho = os.path.join(root, file)
                
                # CORREÇÃO CRÍTICA: Detetar categoria corretamente
                # Se estiver em subpasta, usar nome da subpasta
                # Se estiver na raiz, usar nome do arquivo como categoria
                if root == base_dir:
                    # Está na pasta raiz - usar nome do arquivo como categoria
                    categoria = file.replace('.py', '')
                else:
                    # Está em subpasta - usar nome da pasta
                    categoria = os.path.basename(root)
                
                print(f"   📄 {file} → Categoria: {categoria}")
                
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=caminho)
                        for node in tree.body:
                            if isinstance(node, ast.FunctionDef):
                                nome = node.name
                                if not nome.startswith('_'):
                                    # Verificar duplicados
                                    if nome in funcoes_unicas:
                                        duplicados.append({
                                            "nome": nome, 
                                            "caminho": caminho, 
                                            "categoria": categoria
                                        })
                                    else:
                                        funcoes_unicas.add(nome)
                                    
                                    func_data = {
                                        "nome": nome,
                                        "caminho": caminho,
                                        "categoria": categoria,
                                        "args": [a.arg for a in node.args.args],
                                        "docstring": ast.get_docstring(node) or "",
                                        "modulo": file.replace('.py', '')
                                    }
                                    
                                    resultados.append(func_data)
                                    categorias[categoria].append(func_data)
                                
                except Exception as e:
                    print(f"❌ Erro ao processar {caminho}: {e}")
    
    return resultados, categorias, duplicados

def main():
    """Função principal do analisador."""
    print("🔄 INICIANDO FASE 1: ANÁLISE DE FUNÇÕES...")
    
    # Verificar se o diretório existe
    if not os.path.exists(BASE_DIR):
        print(f"❌ Diretório não encontrado: {BASE_DIR}")
        return False
    
    # Executar análise
    funcoes, categorias, duplicados = extrair_funcoes_com_estatisticas(BASE_DIR)

    # Gerar relatório TXT (para humanos)
    with open(LISTA_FUNCOES_TXT, "w", encoding="utf-8") as f:
        f.write("# LISTA DE FUNÇÕES DA BIBLIOTECA\n")
        f.write(f"# Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"## ESTATÍSTICAS GERAIS\n")
        f.write(f"- Funções únicas: {len(funcoes)}\n")
        f.write(f"- Categorias: {len(categorias)}\n")
        f.write(f"- Duplicados: {len(duplicados)}\n\n")
        
        for categoria, funcs in sorted(categorias.items()):
            f.write(f"## CATEGORIA: {categoria.upper()} ({len(funcs)} funções)\n")
            for func in funcs:
                f.write(f"- {func['nome']}({', '.join(func['args'])})\n")
                if func['docstring']:
                    f.write(f"  # {func['docstring'].split('.')[0]}\n")
            f.write("\n")
        
        if duplicados:
            f.write("\n## ⚠️ FUNÇÕES DUPLICADAS\n")
            for dup in duplicados:
                f.write(f"- {dup['nome']} em {dup['caminho']}\n")

    # Gerar relatório JSON (para máquinas)
    dados_json = {
        "metadata": {
            "data_geracao": datetime.now().isoformat(),
            "total_funcoes": len(funcoes),
            "total_categorias": len(categorias),
            "total_duplicados": len(duplicados)
        },
        "categorias": {
            cat: [
                {
                    "nome": func["nome"],
                    "args": func["args"],
                    "docstring": func["docstring"],
                    "modulo": func["modulo"],
                    "caminho": func["caminho"]
                } for func in funcs
            ] for cat, funcs in categorias.items()
        },
        "duplicados": duplicados,
        "estatisticas_categorias": {
            cat: len(funcs) for cat, funcs in categorias.items()
        }
    }

    with open(LISTA_FUNCOES_JSON, "w", encoding="utf-8") as f:
        json.dump(dados_json, f, indent=2, ensure_ascii=False)

    print(f"✅ Relatório TXT gerado: {LISTA_FUNCOES_TXT}")
    print(f"✅ Relatório JSON gerado: {LISTA_FUNCOES_JSON}")
    print(f"📊 Estatísticas: {len(funcoes)} funções únicas, {len(categorias)} categorias")
    
    if duplicados:
        print(f"⚠️  {len(duplicados)} funções duplicadas encontradas")

    # Listar categorias detectadas
    print("\n📁 Categorias detectadas:")
    for cat in sorted(categorias.keys()):
        print(f"  - {cat}: {len(categorias[cat])} funções")
    
    # VERIFICAÇÃO FINAL - Para o GitHub Actions
    if os.path.exists(LISTA_FUNCOES_JSON) and os.path.exists(LISTA_FUNCOES_TXT):
        print("🎯 FASE 1 CONCLUÍDA - Relatórios prontos para commit")
        return True
    else:
        print("❌ FALHA - Relatórios não foram gerados")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Erro no analisador: {e}")
        sys.exit(1)
