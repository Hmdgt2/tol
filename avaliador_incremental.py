import os
import json
import importlib
import sys
import inspect
from collections import defaultdict

# Adiciona o diretório raiz ao caminho do sistema para importar as heurísticas e os dados
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from lib.dados import carregar_sorteios, get_all_stats
from gerar_relatorio_analise_completa import carregar_heuristicas, analisar_performance_detalhada

# Caminhos de ficheiro
RELATORIOS_DIR = "estatisticas"
ULTIMO_CONCURSO_ANALISADO_PATH = os.path.join(RELATORIOS_DIR, "ultimo_concurso_analisado.json")

def carregar_checkpoint():
    """Carrega o número do último concurso analisado a partir do ficheiro de controlo."""
    if os.path.exists(ULTIMO_CONCURSO_ANALISADO_PATH):
        with open(ULTIMO_CONCURSO_ANALISADO_PATH, 'r', encoding='utf-8') as f:
            return json.load(f).get("ultimo_concurso_analisado")
    return None

def salvar_checkpoint(concurso):
    """Guarda o número do último concurso analisado no ficheiro de controlo."""
    os.makedirs(RELATORIOS_DIR, exist_ok=True)
    with open(ULTIMO_CONCURSO_ANALISADO_PATH, 'w', encoding='utf-8') as f:
        json.dump({"ultimo_concurso_analisado": concurso}, f, indent=2)

def carregar_relatorios_existentes():
    """Carrega todos os relatórios JSON existentes da pasta de relatórios."""
    relatorios = {}
    if not os.path.exists(RELATORIOS_DIR):
        return relatorios

    for ficheiro in os.listdir(RELATORIOS_DIR):
        caminho_completo = os.path.join(RELATORIOS_DIR, ficheiro)
        if ficheiro.endswith('.json') and ficheiro != "relatorio_combinacoes.json" and ficheiro != "ultimo_concurso_analisado.json":
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                nome_heuristica = os.path.splitext(ficheiro)[0]
                try:
                    relatorios[nome_heuristica] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Erro a ler o ficheiro JSON: {ficheiro}. A ignorar.")
    return relatorios

def salvar_relatorio_individual(nome_heuristica, dados_relatorio):
    """Salva um relatório de heurística individual na pasta de relatórios."""
    caminho_ficheiro = os.path.join(RELATORIOS_DIR, f"{nome_heuristica}.json")
    with open(caminho_ficheiro, 'w', encoding='utf-8') as f:
        json.dump(dados_relatorio, f, indent=2, ensure_ascii=False)

def main():
    print("A iniciar o avaliador incremental de performance das heurísticas...")
    
    # 1. Carregar todos os sorteios e heurísticas
    sorteios_historicos = carregar_sorteios()
    heuristicas_info = carregar_heuristicas()
    descricoes_heuristicas = {h['nome']: h['descricao'] for h in heuristicas_info}
    heuristicas_funcoes = [(h['nome'], h['funcao']) for h in heuristicas_info]

    if not sorteios_historicos or not heuristicas_funcoes:
        print("Dados ou heurísticas insuficientes. A sair.")
        return

    # 2. Determinar o ponto de partida
    ultimo_concurso_processado = carregar_checkpoint()
    indice_ultimo = -1

    if ultimo_concurso_processado:
        try:
            indice_ultimo = next(i for i, s in enumerate(sorteios_historicos) if s.get('concurso') == ultimo_concurso_processado)
        except StopIteration:
            print(f"Aviso: Concurso {ultimo_concurso_processado} do ponto de controlo não encontrado no histórico. A reprocessar desde o início.")
            indice_ultimo = -1

    sorteios_novos = sorteios_historicos[indice_ultimo + 1:]
    
    if not sorteios_novos:
        print("Nenhum novo sorteio para processar. Os relatórios já estão atualizados.")
        return

    print(f"A processar {len(sorteios_novos)} novos sorteios, a partir do concurso {sorteios_novos[0]['concurso']}...")

    # 3. Carregar os relatórios existentes
    relatorios = carregar_relatorios_existentes()

    # 4. Processar cada novo sorteio
    for i in range(len(sorteios_novos)):
        sorteio_atual = sorteios_novos[i]
        concurso_atual = sorteio_atual.get('concurso')
        resultado_real = set(sorteio_atual.get('numeros', []))

        # O histórico parcial para a previsão inclui todos os sorteios até ao atual
        historico_parcial = sorteios_historicos[:indice_ultimo + 1 + i + 1]
        estatisticas = get_all_stats(historico_parcial)

        for nome_heuristica, funcao_prever in heuristicas_funcoes:
            
            # Carregar ou inicializar o relatório para a heurística
            if nome_heuristica not in relatorios:
                relatorios[nome_heuristica] = {
                    "nome_heuristica": nome_heuristica,
                    "descricao": descricoes_heuristicas.get(nome_heuristica, 'Descrição não disponível.'),
                    "total_previsoes": 0,
                    "metricas_acerto": {
                        "acerto_1": {"total": 0, "taxa_sucesso": 0.0},
                        "acerto_2": {"total": 0, "taxa_sucesso": 0.0},
                        "acerto_3": {"total": 0, "taxa_sucesso": 0.0},
                        "acerto_4": {"total": 0, "taxa_sucesso": 0.0},
                        "acerto_5": {"total": 0, "taxa_sucesso": 0.0}
                    },
                    "melhor_previsao": {
                        "concurso": None, "data": None, "numeros_acertados": -1, 
                        "numeros_previstos_pico": [], "numeros_reais_pico": [], "indice_sorteio": -1
                    },
                    "desempenho_pos_pico": {"sorteios_apos": 0, "media_acertos_apos": 0.0}
                }
            
            # Gerar a previsão para o sorteio atual
            parametros = inspect.signature(funcao_prever).parameters
            if 'sorteios_historico' in parametros:
                resultado_prev = funcao_prever(estatisticas, n=5, sorteios_historico=historico_parcial[:-1])
            else:
                resultado_prev = funcao_prever(estatisticas, n=5)

            if resultado_prev and 'numeros' in resultado_prev:
                numeros_previstos = set(resultado_prev["numeros"])
                num_acertos = len(numeros_previstos.intersection(resultado_real))
                
                # Atualizar os contadores de acerto
                relatorios[nome_heuristica]["total_previsoes"] += 1
                for j in range(1, 6):
                    if num_acertos >= j:
                        relatorios[nome_heuristica]["metricas_acerto"][f"acerto_{j}"]["total"] += 1

                # Atualizar a melhor previsão
                if num_acertos > relatorios[nome_heuristica]["melhor_previsao"]["numeros_acertados"]:
                    relatorios[nome_heuristica]["melhor_previsao"] = {
                        "concurso": concurso_atual,
                        "data": sorteio_atual.get('data'),
                        "numeros_acertados": num_acertos,
                        "numeros_previstos_pico": sorted(list(numeros_previstos)),
                        "numeros_reais_pico": sorted(list(resultado_real)),
                        "indice_sorteio": indice_ultimo + i + 1 # Atualiza o índice com base no histórico completo
                    }
        print(f"Sorteio {concurso_atual} processado.")

    # 5. Salvar os relatórios e o novo ponto de controlo
    for nome_heuristica, dados in relatorios.items():
        # Recalcular as taxas de sucesso
        total_prev = dados["total_previsoes"]
        for j in range(1, 6):
            metrica = dados["metricas_acerto"][f"acerto_{j}"]
            taxa = (metrica["total"] / total_prev * 100) if total_prev > 0 else 0
            metrica["taxa_sucesso"] = f"{taxa:.2f}%"
        
        # Salvar o ficheiro individual
        salvar_relatorio_individual(nome_heuristica, dados)
        
    salvar_checkpoint(sorteios_novos[-1]['concurso'])
    print("\nProcessamento incremental concluído.")
    print(f"Relatórios atualizados em: {RELATORIOS_DIR}")
    print(f"Ponto de controlo guardado: '{ULTIMO_CONCURSO_ANALISADO_PATH}' com o concurso {sorteios_novos[-1]['concurso']}")

if __name__ == "__main__":
    main()
