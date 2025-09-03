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
from lib.dados import Dados

# Caminho de saída do arquivo de resumo
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'dados')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'resumo_projeto.json')

def main():
    """
    Gera um resumo de todas as heurísticas e suas dependências
    e salva o resultado num arquivo JSON.
    """
    print("Iniciando a geração do resumo do projeto...")

    # 1. Carrega o Despachante para obter as informações das heurísticas
    despachante = Despachante()
    
    if not despachante.heuristicas:
        print("❌ Não foi possível carregar nenhuma heurística. O resumo não pode ser gerado.")
        return

    # 2. Usa o método do Despachante para obter os metadados de forma confiável
    resumo_heuristicas = despachante.obter_metadados()

    if not resumo_heuristicas:
        print("Nenhum metadado de heurística válido encontrado.")
    
    # 3. Carrega o Dados para obter as informações das funções de cálculo
    dados_manager = Dados()
    resumo_funcoes_de_calculo = dados_manager.obter_resumo_calculos()

    if not resumo_funcoes_de_calculo:
        print("Nenhuma função de cálculo válida encontrada.")

    # 4. Combina os dois resumos num único dicionário
    resumo_completo = {
        "heuristicas": resumo_heuristicas,
        "funcoes_de_calculo": resumo_funcoes_de_calculo
    }

    # 5. Garante que a pasta de saída existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 6. Salva o resumo num arquivo JSON formatado
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resumo_completo, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Resumo completo do projeto salvo com sucesso em '{OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
