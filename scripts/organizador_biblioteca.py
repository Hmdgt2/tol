# scripts/organizador_biblioteca.py
import os
from ast_consolidador import ASTConsolidator

# Configurações
FUNCOES_DIR = 'lib/funcoes_analiticas'

# REGRAS CANÓNICAS - Defina aqui todas as suas duplicações
REGRAS_CANONICAS = {
    # Formato: (nome_funcao, modulo_origem): (modulo_destino, [novo_nome_opcional])
    
    # Estatísticas Básicas → estatisticas.py
    ("unique_count", "conjuntos"): ("estatisticas", None),
    ("intersection", "conjuntos"): ("estatisticas", None),
    ("union", "conjuntos"): ("estatisticas", None),
    ("mirror_count", "conjuntos"): ("estatisticas", None),
    ("pair_sum_count", "conjuntos"): ("estatisticas", None),
    ("iqr_outliers", "deteccao_anomalias"): ("estatisticas", None),
    
    # Números Especiais → numeros_especiais.py
    ("bell_number", "teoria_numeros"): ("numeros_especiais", "bell_number"),
    ("partition_number", "teoria_numeros"): ("numeros_especiais", "partition_number"),
    ("bernoulli_number", "teoria_numeros"): ("numeros_especiais", "bernoulli_number"),
    ("fibonacci", "teoria_numeros"): ("numeros_especiais", "fibonacci_num"),
    ("lucas", "teoria_numeros"): ("numeros_especiais", "lucas_num"),
    ("catalan_number", "teoria_numeros"): ("numeros_especiais", "catalan_num"),
    
    # Funções Especiais → funcoes_especiais.py
    ("gamma_func", "matematica_especial"): ("funcoes_especiais", None),
    ("beta_func", "matematica_especial"): ("funcoes_especiais", None),
    ("bessel_j", "matematica_especial"): ("funcoes_especiais", None),
    
    # Processamento de Sinal → temporais.py
    ("fft_phase", "processamento_sinal"): ("temporais", None),
    ("ifft_real", "processamento_sinal"): ("temporais", None),
    
    # Teoria da Informação → teoria_informacao.py
    ("mutual_info", "estatistica_multivariada"): ("teoria_informacao", None),
    ("normalized_mutual_info", "estatistica_multivariada"): ("teoria_informacao", None),
}

# Funções que requerem intervenção manual
ACOES_MANUAIS = [
    "sum_of_pairs",  # Conflito com sum_combinations2/3
    "sum_of_triples", # Conflito com sum_combinations3
    "shortest_paths_length", # Conflito com shortest_path_all_pairs
    # Adicione aqui outras funções que precisam de fusão manual
]

def criar_backup():
    """Cria um backup da biblioteca antes de fazer alterações."""
    import shutil
    import datetime
    
    backup_dir = f"backup_biblioteca_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    if os.path.exists(FUNCOES_DIR):
        shutil.copytree(FUNCOES_DIR, backup_dir)
        print(f"📦 Backup criado em: {backup_dir}")
    else:
        print("⚠️ Diretório de funções não encontrado para backup")

def executar_consolidacao_automatica():
    """Executa a consolidação automática baseada nas regras canónicas."""
    print("🚀 INICIANDO CONSOLIDAÇÃO AUTOMÁTICA DA BIBLIOTECA")
    print("=" * 60)
    
    # Criar backup primeiro
    criar_backup()
    
    sucesso_count = 0
    falha_count = 0
    ignoradas_count = 0
    
    for (func_name, source_mod), (target_mod, novo_nome) in REGRAS_CANONICAS.items():
        print(f"\n📋 Processando: {func_name}")
        print(f"   De: {source_mod}.py")
        print(f"   Para: {target_mod}.py" + (f" (como {novo_nome})" if novo_nome else ""))
        
        # Verificar se o módulo de origem existe
        source_path = os.path.join(FUNCOES_DIR, f"{source_mod}.py")
        if not os.path.exists(source_path):
            print(f"   ⚠️ Ignorado: Módulo de origem {source_path} não existe")
            ignoradas_count += 1
            continue
            
        try:
            consolidator = ASTConsolidator(target_mod, source_mod, FUNCOES_DIR)
            resultado = consolidator.mover_funcao(func_name, novo_nome)
            
            if resultado:
                sucesso_count += 1
            else:
                falha_count += 1
                
        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")
            falha_count += 1
    
    return sucesso_count, falha_count, ignoradas_count

def mostrar_relatorio_manual():
    """Mostra as ações que precisam de intervenção manual."""
    print("\n🔧 AÇÕES MANUAIS NECESSÁRIAS")
    print("=" * 60)
    print("As seguintes funções têm conflitos complexos e precisam de fusão manual:")
    
    for i, acao in enumerate(ACOES_MANUAIS, 1):
        print(f"   {i}. ⚠️ {acao}")
    
    print("\n📝 INSTRUÇÕES PARA FUSÃO MANUAL:")
    print("   1. Analise o código de cada função em conflito")
    print("   2. Escolha a implementação mais eficiente/geral")
    print("   3. Funda as funções manualmente")
    print("   4. Mantenha apenas uma versão no módulo canónico apropriado")
    print("   5. Remova as versões duplicadas dos outros módulos")

def main():
    """Função principal do organizador."""
    print("🧹 ORGANIZADOR DE BIBLIOTECA - FASE DE LIMPEZA")
    print("=" * 60)
    
    # Executar consolidação automática
    sucesso, falha, ignoradas = executar_consolidacao_automatica()
    
    # Mostrar relatório final
    print("\n📊 RELATÓRIO FINAL DA AUTOMAÇÃO")
    print("=" * 60)
    print(f"✅ Consolidações bem sucedidas: {sucesso}")
    print(f"❌ Falhas: {falha}")
    print(f"⚠️ Ignoradas: {ignoradas}")
    
    # Mostrar ações manuais
    if ACOES_MANUAIS:
        mostrar_relatorio_manual()
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"   1. Resolver as ações manuais listadas acima")
    print(f"   2. Executar o analisador novamente para verificar duplicações restantes")
    print(f"   3. Iniciar o desenvolvimento do Motor de IA com a biblioteca limpa")

if __name__ == "__main__":
    main()
