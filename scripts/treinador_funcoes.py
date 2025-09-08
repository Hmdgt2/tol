# tol/scripts/treinador_funcoes.py
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List, Any

# Adiciona o diretório-pai ao caminho para importar as classes
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa a classe Dados do diretório 'lib'
from lib.dados import Dados
# Importa as funções do gerador no mesmo diretório
from gerador_logicas import gerar_logicas, calcular_variaveis

def treinar_e_encontrar_logica(ano_alvo: int):
    print(f"Iniciando o treino para o ano: {ano_alvo}...")
    
    # 1. Carrega todos os dados
    dados_manager = Dados()
    sorteios_do_ano = [s for s in dados_manager.sorteios if s and s.get('concurso') and int(s['concurso'].split('/')[1]) == ano_alvo]
    
    if not sorteios_do_ano:
        print(f"Nenhum sorteio encontrado para o ano {ano_alvo}. Abortando.")
        return

    logicas_encontradas = defaultdict(dict)
    
    # Simulação incremental do histórico
    for i in range(1, len(sorteios_do_ano)):
        historico_incremental = sorteios_do_ano[:i]
        sorteio_alvo = sorteios_do_ano[i]
        
        numeros_alvo = set(sorteio_alvo.get('numeros', []))
        concurso_alvo = sorteio_alvo.get('concurso')

        print(f"\nAnalisando o sorteio {concurso_alvo}...")

        if not historico_incremental:
            continue
        variaveis_anteriores = calcular_variaveis(historico_incremental[-1]['numeros'])
        if not variaveis_anteriores:
            print("  ❌ Não há variáveis suficientes para gerar lógicas.")
            continue

        logicas_candidatas = gerar_logicas(variaveis_anteriores)
        
        acertos_da_logica = defaultdict(list)

        for logica in logicas_candidatas:
            try:
                previsao = logica['func'](variaveis_anteriores)
                
                if previsao in numeros_alvo:
                    acertos_da_logica[logica['nome']].append(previsao)
            except Exception as e:
                continue
        
        numeros_acertados = set()
        for acertos in acertos_da_logica.values():
            numeros_acertados.update(acertos)

        if acertos_da_logica:
            logicas_encontradas[concurso_alvo]['acertos'] = {
                l: a for l, a in acertos_da_logica.items()
            }
            logicas_encontradas[concurso_alvo]['numeros_previstos'] = sorted(list(numeros_acertados))
            logicas_encontradas[concurso_alvo]['numeros_em_falta'] = sorted(list(numeros_alvo - numeros_acertados))
            
            print(f"  ✅ Acertos encontrados: {len(numeros_acertados)} de 5. Números: {logicas_encontradas[concurso_alvo]['numeros_previstos']}")
            if logicas_encontradas[concurso_alvo]['numeros_em_falta']:
                print(f"  ⚠️ Números em falta: {logicas_encontradas[concurso_alvo]['numeros_em_falta']}")
        else:
            logicas_encontradas[concurso_alvo]['acertos'] = {}
            logicas_encontradas[concurso_alvo]['numeros_previstos'] = []
            logicas_encontradas[concurso_alvo]['numeros_em_falta'] = sorted(list(numeros_alvo))
            print("  ❌ Nenhuma lógica gerada encontrou acertos.")
    
    # NOVO: Define a pasta onde o ficheiro será gravado
    pasta_resultados = os.path.join(PROJECT_ROOT, 'dados')
    
    # NOVO: Constrói o caminho completo do ficheiro
    nome_arquivo = f'engenharia_reversa_{ano_alvo}.json'
    caminho_completo_arquivo = os.path.join(pasta_resultados, nome_arquivo)
    
    with open(caminho_completo_arquivo, 'w', encoding='utf-8') as f:
        json.dump(logicas_encontradas, f, indent=4)
        
    print(f"\nEngenharia reversa para o ano {ano_alvo} concluída. Análise salva em '{caminho_completo_arquivo}'.")

if __name__ == '__main__':
    treinar_e_encontrar_logica(2011)
