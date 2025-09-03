import os
import sys
import json

# Adiciona o diretório raiz para resolver as importações
# O script agora está em 'scripts/', então precisamos de subir um nível ('..')
# para chegar à raiz do projeto ('tol').
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante

# Caminho de saída do arquivo de resumo
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'dados')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'resumo_heuristicas.json')

def main():
    """
    Gera um resumo de todas as heurísticas e suas dependências
    e salva o resultado num arquivo JSON.
    """
    print("Iniciando a geração do resumo das heurísticas...")

    # 1. Carrega o Despachante, que se encarrega de encontrar e carregar as heurísticas
    despachante = Despachante()
    
    if not despachante.heuristicas:
        print("❌ Não foi possível carregar nenhuma heurística. O resumo não pode ser gerado.")
        return

    # 2. Usa o método do Despachante para obter os metadados de forma confiável
    resumo_metadados = despachante.obter_metadados()

    if not resumo_metadados:
        print("Nenhum metadado de heurística válido encontrado.")
        return

    # 3. Garante que a pasta de saída existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 4. Salva o resumo num arquivo JSON formatado
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resumo_metadados, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Resumo das heurísticas salvo com sucesso em '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
