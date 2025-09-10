import os
import sys
import json
from typing import Dict, Any, List

# Adiciona o diretório raiz para resolver as importações
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.despachante import Despachante # Importa o nome da classe 'Despachante'
from lib.dados import Dados

# Caminho de saída para o ficheiro de análise
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'relatorios')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'relatorio_analise.json')

def main():
    """
    Gera um relatório detalhado para análise, incluindo:
    - Metadados das heurísticas e suas dependências.
    - Metadados das funções de cálculo.
    - Funções de cálculo que não estão a ser utilizadas.
    - Funções de cálculo duplicadas (baseado em palavras-chave).
    """
    print("Iniciando a geração do relatório de análise do projeto...")

    try:
        # 1. Carrega o despachante e os metadados das heurísticas
        despachante = Despachante()
        resumo_heuristicas = despachante.obter_metadados()
        
        # 2. Carrega as funções de cálculo e os metadados
        dados_manager = Dados()
        resumo_funcoes_de_calculo = dados_manager.obter_resumo_calculos_com_metadados()
        
        # 3. Identifica as dependências que não estão a ser usadas por nenhuma heurística
        todas_dependencias_usadas = despachante.obter_todas_dependencias()
        todas_funcoes_calculo = set(resumo_funcoes_de_calculo.keys())
        dependencias_nao_usadas = sorted(list(todas_funcoes_calculo - todas_dependencias_usadas))

        # 4. Identifica possíveis funções duplicadas (baseado em palavras-chave)
        funcoes_por_logica = {}
        for nome_funcao, meta in resumo_funcoes_de_calculo.items():
            for palavra_chave in meta.get('logica_principais', []):
                if palavra_chave not in funcoes_por_logica:
                    funcoes_por_logica[palavra_chave] = []
                funcoes_por_logica[palavra_chave].append(nome_funcao)
        
        funcoes_duplicadas = {
            palavra_chave: nomes for palavra_chave, nomes in funcoes_por_logica.items()
            if len(nomes) > 1
        }
        
        # 5. Combina todos os dados em um relatório final
        relatorio_analise = {
            "resumo_heuristicas": resumo_heuristicas,
            "resumo_funcoes_de_calculo": resumo_funcoes_de_calculo,
            "dependencias_nao_usadas": dependencias_nao_usadas,
            "potenciais_funcoes_duplicadas": funcoes_duplicadas
        }

        # 6. Salva o relatório num ficheiro JSON
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(relatorio_analise, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Relatório de análise gerado com sucesso em '{OUTPUT_FILE}'.")
        print("\nPara a análise completa, verifique o campo 'potenciais_funcoes_duplicadas'.")
        print(f"As funções que não estão a ser utilizadas são: {dependencias_nao_usadas}")

    except Exception as e:
        print(f"❌ Erro ao gerar o relatório de análise: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
