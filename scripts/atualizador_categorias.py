import os
import re
import json
from datetime import datetime

# CONFIGURAÇÕES
LISTA_FUNCOES_JSON = "relatorios/lista_funcoes.json"
WRAPPER_SCRIPT = "scripts/gerar_wrappers_funcoes.py"
RELATORIO_PATH = "relatorios/atualizacao_categorias.txt"

os.makedirs(os.path.dirname(RELATORIO_PATH), exist_ok=True)

def carregar_funcoes_do_json():
    """Carrega as funções e categorias do relatório JSON."""
    if not os.path.exists(LISTA_FUNCOES_JSON):
        print(f"❌ Arquivo {LISTA_FUNCOES_JSON} não encontrado.")
        print("💡 Execute primeiro: python scripts/analisador_funcoes.py")
        return {}, []
    
    with open(LISTA_FUNCOES_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    categorias = dados.get("categorias", {})
    duplicados = dados.get("duplicados", [])
    
    print(f"📁 Carregadas {len(categorias)} categorias do JSON")
    return categorias, duplicados

def carregar_mapa_atual(script_path):
    """Carrega o FUNCAO_CATEGORIA_MAP atual do script."""
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Encontrar FUNCAO_CATEGORIA_MAP usando regex
        pattern = r"FUNCAO_CATEGORIA_MAP\s*=\s*\{([^}]+)\}"
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print("❌ Não foi possível encontrar FUNCAO_CATEGORIA_MAP")
            return {}
        
        mapa_str = "{" + match.group(1) + "}"
        
        # Converter string para dicionário com eval seguro
        mapa_atual = eval(mapa_str)
        return mapa_atual
        
    except FileNotFoundError:
        print(f"⚠️  Arquivo {script_path} não encontrado. Criando mapa vazio.")
        return {}
    except Exception as e:
        print(f"❌ Erro ao carregar mapa atual: {e}")
        return {}

# ... (manter as funções gerar_sugestoes_categoria e atualizar_script_wrappers do código anterior)

def main():
    """Executa o pipeline completo de atualização."""
    
    print("🔄 INICIANDO ATUALIZAÇÃO AUTOMÁTICA DE CATEGORIAS...")
    
    # 1. Carregar funções do JSON gerado pelo analisador
    print("📁 Carregando funções do relatório JSON...")
    categorias_detectadas, duplicados = carregar_funcoes_do_json()
    
    if not categorias_detectadas:
        print("💥 Não foi possível carregar as categorias. Pipeline interrompido.")
        return
    
    # 2. Carregar categorias atuais do script
    print("📋 Carregando categorias atuais...")
    mapa_atual = carregar_mapa_atual(WRAPPER_SCRIPT)
    categorias_atuais = set(mapa_atual.keys())
    categorias_detectadas_set = set(categorias_detectadas.keys())
    
    # 3. Identificar mudanças
    novas_categorias = categorias_detectadas_set - categorias_atuais
    categorias_removidas = categorias_atuais - categorias_detectadas_set
    
    print(f"📊 DETECTADAS: {len(categorias_detectadas_set)} categorias")
    print(f"🆕 NOVAS: {len(novas_categorias)} categorias")
    print(f"🗑️ REMOVIDAS: {len(categorias_removidas)} categorias")
    print(f"⚠️ DUPLICADOS: {len(duplicados)} funções")
    
    # Listar categorias detectadas
    print("\n📁 Categorias detectadas:")
    for cat in sorted(categorias_detectadas.keys()):
        print(f"  - {cat}: {len(categorias_detectadas[cat])} funções")
    
    # 4. Atualizar se necessário
    if novas_categorias or categorias_removidas:
        print("\n🔄 ATUALIZANDO SCRIPT DE WRAPPERS...")
        novas_count, removidas_count = atualizar_script_wrappers(
            WRAPPER_SCRIPT, novas_categorias, categorias_removidas, categorias_detectadas
        )
        
        # 5. Gerar relatório
        print("📄 GERANDO RELATÓRIO...")
        gerar_relatorio(novas_categorias, categorias_removidas, duplicados, categorias_detectadas)
        
        print(f"\n✅ ATUALIZAÇÃO CONCLUÍDA!")
        print(f"   ➕ {novas_count} novas categorias adicionadas")
        print(f"   ➖ {removidas_count} categorias removidas") 
        print(f"   📊 Relatório salvo em: {RELATORIO_PATH}")
        
        # 6. Sugerir próximo passo
        if novas_categorias:
            print(f"\n🎯 PRÓXIMO PASSO: Executar 'gerar_wrappers_funcoes.py'")
        
    else:
        print("✅ Nenhuma atualização necessária - todas as categorias estão sincronizadas")
    
    if duplicados:
        print(f"\n⚠️  ATENÇÃO: {len(duplicados)} funções duplicadas encontradas")
        print("   Revise o relatório para corrigir duplicações")

if __name__ == "__main__":
    main()
