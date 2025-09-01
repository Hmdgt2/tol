import os
import sys
import importlib.util
import json

# Adiciona o diretório-pai (raiz do projeto) ao caminho para importação
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Caminhos de entrada e saída
HEURISTICAS_DIR = os.path.join(PROJECT_ROOT, 'heuristicas')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'dados')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'resumo_heuristicas.json')

def analisar_heuristicas():
    """
    Analisa os arquivos de heurística e extrai seus metadados.
    Retorna um dicionário com o resumo de cada heurística.
    """
    resumo_heuristicas = {}
    
    for ficheiro in os.listdir(HEURISTICAS_DIR):
        if ficheiro.endswith('.py') and not ficheiro.startswith('__'):
            nome_modulo = ficheiro[:-3]
            caminho_completo = os.path.join(HEURISTICAS_DIR, ficheiro)
            
            try:
                spec = importlib.util.spec_from_file_location(nome_modulo, caminho_completo)
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)

                if hasattr(modulo, 'NOME') and hasattr(modulo, 'DESCRICAO') and hasattr(modulo, 'DEPENDENCIAS'):
                    resumo_heuristicas[modulo.NOME] = {
                        "descricao": modulo.DESCRICAO,
                        "dependencias": modulo.DEPENDENCIAS
                    }
                else:
                    print(f"⚠️ Aviso: Arquivo {ficheiro} ignorado. Faltam metadados.")

            except Exception as e:
                print(f"❌ Erro ao analisar a heurística {nome_modulo}: {e}")

    return resumo_heuristicas

def main():
    if not os.path.exists(HEURISTICAS_DIR):
        print(f"Erro: Pasta '{HEURISTICAS_DIR}' não encontrada.")
        return

    resumo = analisar_heuristicas()

    if not resumo:
        print("Nenhuma heurística válida encontrada.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resumo, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resumo das heurísticas salvo em '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
