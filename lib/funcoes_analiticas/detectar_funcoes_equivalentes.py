import os
import ast
import hashlib
from collections import defaultdict

BASE_DIR = "lib/funcoes_analiticas"
RELATORIO_DIR = "relatorios"
RELATORIO_PATH = os.path.join(RELATORIO_DIR, "funcoes_equivalentes.txt")

os.makedirs(RELATORIO_DIR, exist_ok=True)

# Funções agrupadas por hash do corpo
funcoes_por_hash = defaultdict(list)

def normalizar_corpo(node):
    """Remove nome da função e normaliza o corpo para comparação."""
    # Remove o nome e argumentos, foca só no corpo
    corpo = node.body
    corpo_ast = ast.Module(body=corpo, type_ignores=[])
    try:
        texto = ast.unparse(corpo_ast)
    except Exception:
        texto = ast.dump(corpo_ast)
    # Remove espaços e comentários
    texto = ''.join(texto.split())
    return hashlib.md5(texto.encode("utf-8")).hexdigest()

# Percorrer todos os ficheiros
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".py"):
            caminho = os.path.join(root, file)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=caminho)
                    for node in tree.body:
                        if isinstance(node, ast.FunctionDef):
                            h = normalizar_corpo(node)
                            funcoes_por_hash[h].append((node.name, caminho))
            except Exception as e:
                print(f"Erro ao processar {caminho}: {e}")

# Escrever relatório
with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
    f.write("🔍 Funções com lógica equivalente (mesmo com nomes diferentes):\n\n")
    for h, entradas in funcoes_por_hash.items():
        if len(entradas) > 1:
            f.write("⚠️ Implementações idênticas encontradas:\n")
            for nome, caminho in entradas:
                f.write(f"  - `{nome}` em {caminho}\n")
            f.write("  ✅ Lógica funcional idêntica\n\n")

print(f"✅ Relatório gerado em: {RELATORIO_PATH}")
