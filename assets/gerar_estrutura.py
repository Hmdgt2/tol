import os

def listar_estrutura(base_dir='.', output_file='assets/estrutura.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                caminho_relativo = os.path.relpath(os.path.join(root, name), base_dir)
                if not caminho_relativo.startswith('assets/estrutura.txt'):
                    f.write(caminho_relativo.replace("\\", "/") + '\n')

if __name__ == "__main__":
    listar_estrutura()
