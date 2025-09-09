# tol/scripts/treinador_funcoes.py
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List, Any
import numpy as np

# Adiciona o diretório-pai ao caminho para importar as classes
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Importa as classes necessárias
from lib.dados import Dados
from lib.despachante import Despachante
from gerador_logicas import gerar_logicas, calcular_variaveis

def treinar_e_encontrar_logica(ano_alvo: int):
    print(f"Iniciando o treino para o ano: {ano_alvo}...")
    
    # 1. Carrega todos os dados e o despachante
    dados_manager = Dados()
    despachante = Despachante()
    todas_dependencias = despachante.obter_todas_dependencias()
    
    sorteios_do_ano = [s for s in dados_manager.sorteios if s and s.get('concurso') and int(s['concurso'].split('/')[1]) == ano_alvo]
    
    if not sorteios_do_ano:
        print(f"Nenhum sorteio encontrado para o ano {ano_alvo}. Abortando.")
        return

    # Estruturas para acumular dados para o relatório final
    totais_acertos_por_logica = defaultdict(int)
    total_numeros_previstos = 0
    total_sorteios_analisados = len(sorteios_do_ano) - 1
    dados_numeros_em_falta = defaultdict(list)
    
    # Simulação incremental do histórico
    for i in range(1, len(sorteios_do_ano)):
        historico_incremental = sorteios_do_ano[:i]
        sorteio_alvo = sorteios_do_ano[i]
        
        numeros_alvo = set(sorteio_alvo.get('numeros', []))
        concurso_alvo = sorteio_alvo.get('concurso')

        if not historico_incremental:
            continue

        variaveis_anteriores = calcular_variaveis(historico_incremental[-1]['numeros'])
        if not variaveis_anteriores:
            print("  ❌ Não há variáveis suficientes para gerar lógicas.")
            continue

        logicas_candidatas = gerar_logicas(variaveis_anteriores)
        
        previsoes_do_sorteio = {}
        for logica in logicas_candidatas:
            try:
                previsao = logica['func'](variaveis_anteriores)
                if isinstance(previsao, (int, float)) and (1 <= int(previsao) <= 49):
                    previsoes_do_sorteio[logica['nome']] = int(previsao)
            except Exception as e:
                continue
        
        # Processa acertos e acumula
        numeros_previstos_unicos = set(previsoes_do_sorteio.values())
        for logica_nome, previsao in previsoes_do_sorteio.items():
            if previsao in numeros_alvo:
                totais_acertos_por_logica[logica_nome] += 1
        
        total_numeros_previstos += len(numeros_previstos_unicos.intersection(numeros_alvo))

        # Analisa e acumula dados sobre os números em falta
        numeros_em_falta = sorted(list(numeros_alvo - numeros_previstos_unicos))
        if numeros_em_falta:
            dados_parciais = Dados()
            dados_parciais.sorteios = historico_incremental
            
            estatisticas_completas, _ = dados_parciais.obter_estatisticas(todas_dependencias)
            
            for num_falta in numeros_em_falta:
                for estat_nome, estat_dict in estatisticas_completas.items():
                    # ATUALIZADO: Filtra apenas os valores que podem ser somados
                    if isinstance(estat_dict, dict):
                        valor = estat_dict.get(num_falta)
                        if isinstance(valor, (int, float)):
                            dados_numeros_em_falta[estat_nome].append(valor)

    # 2. Gera o relatório simplificado
    
    # Calcula as melhores lógicas
    melhores_logicas = sorted(totais_acertos_por_logica.items(), key=lambda item: item[1], reverse=True)[:5]
    melhores_logicas_formatadas = []
    for nome, acertos in melhores_logicas:
        taxa_acerto = (acertos / total_sorteios_analisados) if total_sorteios_analisados > 0 else 0
        melhores_logicas_formatadas.append({
            "nome": nome,
            "acertos_totais": acertos,
            "taxa_acerto_percentual": f"{taxa_acerto:.2f}%"
        })

    # ATUALIZADO: Calcula as médias gerais das estatísticas
    dados_manager_completo = Dados()
    estatisticas_completas_finais, _ = dados_manager_completo.obter_estatisticas(todas_dependencias)
    estatisticas_medias_dict = {}

    for estat_nome, estat_dict in estatisticas_completas_finais.items():
        if isinstance(estat_dict, dict):
            # ATUALIZADO: Filtra valores não-numéricos ao calcular a média geral
            valores = [v for v in estat_dict.values() if isinstance(v, (int, float))]
            if valores:
                estatisticas_medias_dict[estat_nome] = np.mean(valores)

    # Calcula o diagnóstico de lacunas
    diagnostico_lacunas = {}
    for estat_nome, valores in dados_numeros_em_falta.items():
        if valores:
            media_em_falta = sum(valores) / len(valores)
            media_geral = estatisticas_medias_dict.get(estat_nome, 'N/A')
            
            if isinstance(media_geral, (int, float)):
                conclusao = "acima" if media_em_falta > media_geral else "abaixo"
                diagnostico_lacunas[estat_nome] = {
                    "media_em_falta": round(media_em_falta, 2),
                    "media_geral": round(media_geral, 2),
                    "conclusao": f"Os números em falta tinham consistentemente um valor {conclusao} da média geral."
                }
    
    # Se houver estatísticas que não geraram dados de lacunas, mas têm uma média geral
    # Podes querer lidar com elas aqui, mas por agora, a abordagem é focada
    # nas que apareceram nos "números em falta".

    relatorio_final = {
        "ano": ano_alvo,
        "resumo_geral": {
            "total_sorteios_analisados": total_sorteios_analisados,
            "total_acertos_unicos": total_numeros_previstos,
            "melhores_logicas_do_ano": melhores_logicas_formatadas
        },
        "diagnostico_lacunas": diagnostico_lacunas
    }

    # 3. Salva o relatório
    pasta_resultados = os.path.join(PROJECT_ROOT, 'dados')
    os.makedirs(pasta_resultados, exist_ok=True)
    nome_arquivo = f'sumario_anual_engenharia_reversa_{ano_alvo}.json'
    caminho_completo_arquivo = os.path.join(pasta_resultados, nome_arquivo)
    
    with open(caminho_completo_arquivo, 'w', encoding='utf-8') as f:
        json.dump(relatorio_final, f, indent=4, ensure_ascii=False)
        
    print(f"\nEngenharia reversa para o ano {ano_alvo} concluída. Relatório simplificado salvo em '{caminho_completo_arquivo}'.")

if __name__ == '__main__':
    treinar_e_encontrar_logica(2011)
