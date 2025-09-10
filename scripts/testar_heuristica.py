# /scripts/testar_heuristica.py

import os
import sys
import traceback
import json
from collections import Counter, defaultdict

# Adiciona o diretório raiz para resolver as importações
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import Dados
from lib.despachante import Despachante

def testar_heuristica():
    """
    Testa cada heurística para verificar se está a funcionar corretamente.
    Retorna um dicionário com os resultados dos testes.
    """
    resultados = {}
    print("Iniciando teste de todas as heurísticas...")

    try:
        # Carrega o despachante para obter a lista de heurísticas
        despachante = Despachante()
        todas_dependencias = despachante.obter_todas_dependencias()
        
        # Carrega os dados históricos, pois algumas heurísticas precisam deles
        dados_manager = Dados()
        estatisticas, erros_dados = dados_manager.obter_estatisticas(todas_dependencias)

        if erros_dados:
            print("\nAVISO: Erros foram encontrados ao carregar as estatísticas base:")
            for erro in erros_dados:
                print(f" - {erro}")
            print("-" * 50)

        for nome_heuristica, heuristica_instance in despachante.heuristicas.items():
            print(f"Testando a heurística '{nome_heuristica}'...")
            
            try:
                # Prepara os dados de entrada
                dependencias_necessarias = getattr(heuristica_instance, 'DEPENDENCIAS', [])
                dados_de_entrada = {dep: estatisticas.get(dep) for dep in dependencias_necessarias}
                
                # Executa a função 'prever' diretamente na instância
                previsao = heuristica_instance.prever(dados_de_entrada)
                
                # Verifica a validade do resultado
                if not isinstance(previsao, list):
                    status = "FALHOU"
                    detalhes = f"A função não retornou uma lista. Tipo retornado: {type(previsao).__name__}"
                elif not previsao:
                    status = "FALHOU"
                    detalhes = "A lista de previsão está vazia."
                else:
                    status = "SUCESSO"
                    detalhes = f"Previsão gerada com sucesso: {previsao}"
            
            except Exception as e:
                status = "ERRO FATAL"
                detalhes = f"Ocorreu um erro ao executar a heurística: {e}\n{traceback.format_exc()}"
                
            resultados[nome_heuristica] = {
                'status': status,
                'detalhes': detalhes
            }
            
            print(f" -> Status: {status}\n")
    
    except Exception as e:
        print(f"❌ ERRO GRAVE: Falha ao iniciar o teste. Detalhes: {e}")
        return {}

    return resultados

def imprimir_relatorio(resultados):
    """Imprime um relatório formatado dos resultados dos testes."""
    
    print("\n" + "="*50)
    print(" " * 15 + "RELATÓRIO DE TESTE")
    print("="*50)

    sucessos = {h: r for h, r in resultados.items() if r['status'] == 'SUCESSO'}
    falhas = {h: r for h, r in resultados.items() if r['status'] == 'FALHOU'}
    erros_fatais = {h: r for h, r in resultados.items() if r['status'] == 'ERRO FATAL'}
    
    print(f"\n✅ Heurísticas com SUCESSO: {len(sucessos)}")
    for nome, resultado in sucessos.items():
        print(f" - {nome}")

    print(f"\n⚠️ Heurísticas com FALHA (lista vazia): {len(falhas)}")
    for nome, resultado in falhas.items():
        print(f" - {nome}: {resultado['detalhes']}")

    print(f"\n❌ Heurísticas com ERRO FATAL: {len(erros_fatais)}")
    for nome, resultado in erros_fatais.items():
        print(f" - {nome}: {resultado['detalhes']}")
        
    print("\n" + "="*50)

    # Salva os resultados em um arquivo JSON na pasta 'relatorios'
    pasta_relatorios = os.path.join(PROJECT_ROOT, 'relatorios')
    os.makedirs(pasta_relatorios, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_relatorios, 'resultado_testes_heuristicas.json')

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print(f"\n📄 Relatório salvo em: {caminho_arquivo}")

    
if __name__ == "__main__":
    resultados_teste = testar_heuristica()
    if resultados_teste:
        imprimir_relatorio(resultados_teste)
