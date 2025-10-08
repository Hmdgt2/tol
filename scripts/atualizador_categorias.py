import json
import os
from analisador_funcoes import extrair_funcoes_com_estatisticas

def atualizar_categorias_automaticamente():
    """Atualiza FUNCAO_CATEGORIA_MAP com novas categorias detectadas."""
    
    # Carregar categorias atuais do gerar_wrappers_funcoes.py
    with open("scripts/gerar_wrappers_funcoes.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extrair FUNCAO_CATEGORIA_MAP atual
    start = content.find("FUNCAO_CATEGORIA_MAP = {")
    end = content.find("}", start) + 1
    mapa_atual_str = content[start:end]
    
    # Analisar novas categorias
    funcoes, categorias, _ = extrair_funcoes_com_estatisticas("lib/funcoes_analiticas")
    
    categorias_atuais = set(eval(mapa_atual_str).keys())
    categorias_detectadas = set(categorias.keys())
    
    novas_categorias = categorias_detectadas - categorias_atuais
    categorias_removidas = categorias_atuais - categorias_detectadas
    
    print("🔄 ATUALIZAÇÃO DE CATEGORIAS:")
    print(f"   Categorias atuais: {len(categorias_atuais)}")
    print(f"   Categorias detectadas: {len(categorias_detectadas)}")
    print(f"   Novas categorias: {len(novas_categorias)}")
    print(f"   Categorias removidas: {len(categorias_removidas)}")
    
    # Gerar novo mapa se necessário
    if novas_categorias or categorias_removidas:
        print("\n📝 Atualizando FUNCAO_CATEGORIA_MAP...")
        
        # Aqui implementaríamos a lógica para atualizar automaticamente
        # Por enquanto, só reportamos
        for nova_cat in novas_categorias:
            print(f"   ➕ NOVA CATEGORIA: {nova_cat}")
            print(f"      Sugestão: {nova_cat.title()}Wrapper")
        
        for cat_removida in categorias_removidas:
            print(f"   ➖ CATEGORIA REMOVIDA: {cat_removida}")
            
        return True  # Indica que precisa atualização
    else:
        print("✅ Nenhuma atualização necessária")
        return False

if __name__ == "__main__":
    atualizar_categorias_automaticamente()
