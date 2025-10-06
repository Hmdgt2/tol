import os
import ast

BASE_DIR = "lib/funcoes_analiticas"
LISTA_FUNCOES_PATH = "relatorios/lista_funcoes.txt"
os.makedirs(os.path.dirname(LISTA_FUNCOES_PATH), exist_ok=True)

def extrair_funcoes(base_dir):
    resultados = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=caminho)
                        for node in tree.body:
                            if isinstance(node, ast.FunctionDef):
                                nome = node.name
                                assinatura = ast.get_docstring(node)
                                resultados.append({
                                    "nome": nome,
                                    "caminho": caminho,
                                    "args": [a.arg for a in node.args.args],
                                    "docstring": ast.get_docstring(node)
                                })
                except Exception as e:
                    print(f"Erro ao processar {caminho}: {e}")
    return resultados

funcoes = extrair_funcoes(BASE_DIR)

with open(LISTA_FUNCOES_PATH, "w", encoding="utf-8") as f:
    for func in funcoes:
        f.write(f"- Função: {func['nome']}\n")
        f.write(f"  Caminho: {func['caminho']}\n")
        f.write(f"  Args: {func['args']}\n")
        if func['docstring']:
            f.write(f"  Docstring: {func['docstring']}\n")
        f.write("\n")

print(f"✅ Lista de funções gerada em: {LISTA_FUNCOES_PATH}")
