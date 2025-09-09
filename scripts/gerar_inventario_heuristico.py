#/scripts/gerar_inventario_heuristico.py
import os
import sys
import json
import inspect

# Adiciona o diretório-pai (raiz do projeto) ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante

def gerar_inventario_heuristico():
    """
    Gera um relatório JSON com o inventário completo das heurísticas.
    """
    print("A gerar inventário de heurísticas...")
    
    # Instancia o despachante para carregar e obter os metadados
    despachante = Despachante()
    metadados = despachante.obter_metadados()
    
    inventario = {}
    for nome_heuristica, dados_metadados in metadados.items():
        # Constrói a entrada no inventário
        inventario[nome_heuristica] = {
            "descricao": dados_metadados.get('descricao', 'Descrição não disponível.'),
            "dependencias": [dep['nome'] for dep in dados_metadados.get('dependencias', [])],
            "funcao_principal": dados_metadados.get('funcao_principal', 'Não disponível')
        }

    # Define o caminho para o ficheiro de relatório
    RELATORIOS_DIR = os.path.join(PROJECT_ROOT, "relatorios")
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    caminho_relatorio = os.path.join(RELATORIOS_DIR, "inventario_heuristico.json")

    # Salva o inventário em formato JSON
    with open(caminho_relatorio, 'w', encoding='utf-8') as f:
        json.dump(inventario, f, indent=4, ensure_ascii=False)
    
    print(f"Inventário de heurísticas gerado com sucesso em: {caminho_relatorio}")


if __name__ == "__main__":
    gerar_inventario_heuristico()
