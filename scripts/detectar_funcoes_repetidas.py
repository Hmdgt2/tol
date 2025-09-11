import os
import ast
import hashlib
from collections import defaultdict
from difflib import SequenceMatcher

BASE_DIR = "lib/funcoes_analiticas"
RELATORIO_DIR = "relatorios"
os.makedirs(RELATORIO_DIR, exist_ok=True)

# Caminhos dos relatórios
RELATORIO_DUPLICADAS = os.path.join(RELATORIO_DIR, "funcoes_duplicadas.txt")
RELATORIO_EQUIVALENTES = os.path.join(RELATORIO_DIR, "funcoes_equivalentes.txt")
RELATORIO_SEMELHANTES = os.path.join(RELATORIO_DIR, "funcoes_semelhantes.txt")
RELATORIO_REORGANIZACAO = os.path.join(RELATORIO_DIR, "sugestoes_reorganizacao.txt")

# Armazenamento
por_nome = defaultdict(list)
por_hash = defaultdict(list)
todas_funcoes = []

def normalizar_corpo(node):
    """Normaliza o corpo da função para comparação."""
    corpo = node.body
    corpo_ast = ast.Module(body=corpo, type_ignores=[])
    try:
        texto = ast.unparse(corpo_ast)
    except Exception:
        texto = ast.dump(corpo_ast)
    return ''.join(texto.split())

def gerar_hash(texto):
    return hashlib.md5(texto.encode("utf-8")).hexdigest()

def tema_ficheiro(caminho):
    return os.path.basename(caminho).replace(".py", "").lower()

# Extrair funções
for root, _, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".py"):
            caminho = os.path.join(root, file)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=caminho)
                    for node in tree.body:
                        if isinstance(node, ast.FunctionDef):
                            nome = node.name
                            texto = normalizar_corpo(node)
                            h = gerar_hash(texto)
                            por_nome[nome].append(caminho)
                            por_hash[h].append((nome, caminho))
                            todas_funcoes.append((nome, caminho, texto))
            except Exception as e:
                print(f"Erro ao processar {caminho}: {e}")

# Relatório 1: Funções duplicadas
with open(RELATORIO_DUPLICADAS, "w", encoding="utf-8") as f:
    f.write("🔍 Funções com o mesmo nome em múltiplos ficheiros:\n\n")
    for nome, locais in sorted(por_nome.items()):
        if len(locais) > 1:
            f.write(f"⚠️ Função `{nome}` aparece em:\n")
            for caminho in locais:
                f.write(f"  - {caminho}\n")
            f.write("\n")

# Relatório 2: Funções equivalentes
with open(RELATORIO_EQUIVALENTES, "w", encoding="utf-8") as f:
    f.write("🔍 Funções com lógica equivalente (mesmo com nomes diferentes):\n\n")
    for h, entradas in sorted(por_hash.items()):
        if len(entradas) > 1:
            f.write("⚠️ Implementações idênticas encontradas:\n")
            for nome, caminho in entradas:
                f.write(f"  - `{nome}` em {caminho}\n")
            f.write("  ✅ Lógica funcional idêntica\n\n")

# Relatório 3: Funções semelhantes
semelhantes = []
for i in range(len(todas_funcoes)):
    nome1, caminho1, texto1 = todas_funcoes[i]
    for j in range(i + 1, len(todas_funcoes)):
        nome2, caminho2, texto2 = todas_funcoes[j]
        if caminho1 != caminho2:
            ratio = SequenceMatcher(None, texto1, texto2).ratio()
            if 0.85 < ratio < 1.0:
                semelhantes.append((nome1, caminho1, nome2, caminho2, ratio))

with open(RELATORIO_SEMELHANTES, "w", encoding="utf-8") as f:
    f.write("🔍 Funções com lógica semelhante (estrutura parecida):\n\n")
    for nome1, caminho1, nome2, caminho2, ratio in semelhantes:
        f.write(f"⚠️ `{nome1}` em {caminho1}\n")
        f.write(f"   ≈ `{nome2}` em {caminho2}\n")
        f.write(f"   🔁 Similaridade: {round(ratio * 100, 2)}%\n\n")

# Relatório 4: Sugestões de reorganização
sugestoes = []

# Duplicadas
for nome, locais in por_nome.items():
    if len(locais) > 1:
        temas = [tema_ficheiro(c) for c in locais]
        sugestao = f"🔧 Função `{nome}` aparece em múltiplos módulos: {', '.join(temas)}\n"
        sugestao += f"   ➤ Sugestão: manter em `{temas[0]}.py`, remover duplicados\n"
        sugestoes.append(sugestao)

# Equivalentes
for h, entradas in por_hash.items():
    if len(entradas) > 1:
        nomes = set([n for n, _ in entradas])
        caminhos = [c for _, c in entradas]
        temas = [tema_ficheiro(c) for c in caminhos]
        sugestao = f"🔁 Funções equivalentes: {', '.join(nomes)}\n"
        sugestao += f"   ➤ Sugestão: fundir em `{temas[0]}.py` com nome padronizado\n"
        sugestoes.append(sugestao)

# Semelhantes
for nome1, caminho1, nome2, caminho2, ratio in semelhantes:
    tema1 = tema_ficheiro(caminho1)
    tema2 = tema_ficheiro(caminho2)
    if tema1 != tema2:
        sugestao = f"🔍 Funções semelhantes `{nome1}` ({tema1}) ≈ `{nome2}` ({tema2})\n"
        sugestao += f"   🔁 Similaridade: {round(ratio * 100, 2)}%\n"
        sugestao += f"   ➤ Sugestão: avaliar fusão ou renomeação para consistência\n"
        sugestoes.append(sugestao)

with open(RELATORIO_REORGANIZACAO, "w", encoding="utf-8") as f:
    f.write("🧠 Sugestões de Reorganização Funcional:\n\n")
    for linha in sugestoes:
        f.write(linha + "\n")

# Conclusão
print("✅ Relatórios gerados:")
print(f"- {RELATORIO_DUPLICADAS}")
print(f"- {RELATORIO_EQUIVALENTES}")
print(f"- {RELATORIO_SEMELHANTES}")
print(f"- {RELATORIO_REORGANIZACAO}")
