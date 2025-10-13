# check_environment.py
import os
import sys
import importlib

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def check_environment():
    """Verifica se o ambiente está configurado corretamente"""
    print("🔍 Verificando ambiente...")
    
    # Verificar ficheiros essenciais
    essential_files = [
        'lib/dados.py',
        'lib/despachante_new.py', 
        'lib/GeradorHeuristicasDinamicas.py',
        'treinar_decisor_1.py',
        'avaliador/avaliador1.py',
        'decisor/decisor_final_1.py'
    ]
    
    missing_files = []
    for file in essential_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Ficheiros em falta:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ Todos os ficheiros essenciais encontrados")
    
    # Verificar dependências Python
    required_packages = [
        'numpy',
        'sklearn',
        'scipy', 
        'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Pacotes Python em falta:")
        for package in missing_packages:
            print(f"   - {package}")
        return False
    
    print("✅ Todas as dependências Python encontradas")
    
    # Verificar estrutura de imports
    try:
        from lib.dados import Dados
        from lib.despachante_new import Despachante
        print("✅ Imports básicos funcionando")
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        return False
    
    print("🎉 Ambiente verificado com sucesso!")
    return True

if __name__ == "__main__":
    if check_environment():
        sys.exit(0)
    else:
        sys.exit(1)
