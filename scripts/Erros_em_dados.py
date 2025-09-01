# tool/scripts/Erros_em_dados.py

import os
import sys

# Adiciona o diretório raiz ao caminho do sistema
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import MAP_ESTATISTICAS
from lib.despachante import Despachante

def gerar_relatorio_dependencias():
    """
    Gera um relatório que verifica se as dependências das heurísticas
    têm uma função de cálculo correspondente em dados.py.
    """
    despachante = Despachante()
    todas_dependencias = despachante.get_todas_dependencias()
    
    erros_encontrados = []
    
    print("--- Verificação de Dependências ---")
    
    for dep in todas_dependencias:
        if dep in MAP_ESTATISTICAS:
            print(f"✅ Dependência '{dep}' encontrada e mapeada para uma função de cálculo.")
        else:
            erros_encontrados.append(f"❌ Erro: Função de cálculo para a dependência '{dep}' não encontrada.")

    print("\n--- Resumo ---")
    if not erros_encontrados:
        print("🎉 Perfeito! Todas as dependências têm uma função de cálculo correspondente.")
    else:
        print("⚠️ Foram encontrados erros. Por favor, corrija o seguinte:")
        for erro in erros_encontrados:
            print(f"  {erro}")

if __name__ == "__main__":
    gerar_relatorio_dependencias()
