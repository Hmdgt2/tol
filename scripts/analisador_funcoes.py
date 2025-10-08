import os
import ast
from collections import defaultdict

BASE_DIR = "lib/funcoes_analiticas"
LISTA_FUNCOES_PATH = "relatorios/lista_funcoes.txt"
ESTATISTICAS_PATH = "relatorios/estatisticas_funcoes.json"

os.makedirs(os.path.dirname(LISTA_FUNCOES_PATH), exist_ok=True)

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

# Executar análise
funcoes, categorias, duplicados = extrair_funcoes_com_estatisticas(BASE_DIR)

# Gerar lista limpa
with open(LISTA_FUNCOES_PATH, "w", encoding="utf-8") as f:
    f.write("# LISTA LIMPA DE FUNÇÕES - SEM DUPLICADOS\n")
    f.write("=" * 50 + "\n\n")
    
    for categoria, funcs in categorias.items():
        f.write(f"## CATEGORIA: {categoria.upper()} ({len(funcs)} funções)\n")
        for func in funcs:
            f.write(f"- {func['nome']}: {func['args']}\n")
            if func['docstring']:
                f.write(f"  # {func['docstring'].split('.')[0]}\n")
        f.write("\n")
    
    if duplicados:
        f.write("\n## ⚠️ FUNÇÕES DUPLICADAS (REMOVER)\n")
        for dup in duplicados:
            f.write(f"- {dup['nome']} em {dup['caminho']}\n")

print(f"✅ Lista limpa gerada: {LISTA_FUNCOES_PATH}")
print(f"📊 Estatísticas: {len(funcoes)} funções únicas, {len(categorias)} categorias")
if duplicados:
    print(f"⚠️  {len(duplicados)} funções duplicadas encontradas")
