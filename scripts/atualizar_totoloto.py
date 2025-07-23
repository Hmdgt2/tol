import requests
from bs4 import BeautifulSoup
import re
import os
import json
from datetime import datetime

def extrair_totoloto():
    url = "https://www.vercapas.com/jogos-santa-casa/numeros-chave-totoloto-resultados-premios/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.select_one("div.card-body")
    if not container:
        raise ValueError("Não foi possível encontrar o container com os dados do Totoloto.")

    # Concurso
    concurso_div = container.find(string=re.compile("Sorteio"))
    if concurso_div:
        m = re.search(r"Sorteio[:\s]*([\d/]+)", concurso_div)
        concurso = m.group(1) if m else None
    else:
        raise ValueError("Não foi possível encontrar o texto do sorteio.")

    # Data
    data_div = container.find(string=re.compile("Data do Sorteio"))
    if data_div:
        m = re.search(r"Data do Sorteio[:\s]*(\d{4}-\d{2}-\d{2})", data_div)
        data = m.group(1) if m else None
    else:
        raise ValueError("Não foi possível encontrar o texto da data.")

    if not concurso or not data:
        raise ValueError("Não foi possível extrair concurso ou data.")

    ano, mes, dia = data.split("-")
    data_formatada = f"{dia}/{mes}/{ano}"

    # Números + especial
    numeros_p = container.select_one("p.card-text")
    if not numeros_p:
        raise ValueError("Não foi possível encontrar os números sorteados.")

    numeros_texto = numeros_p.text.strip()
    partes = numeros_texto.split("+")
    numeros = list(map(int, partes[0].strip().split()))
    especial = int(partes[1].strip())

    return {
        "concurso": concurso,
        "data": data_formatada,
        "numeros": numeros,
        "especial": especial
    }

def salvar_no_json(resultado):
    ano_corrente = datetime.now().year
    pasta_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_dados = os.path.join(pasta_repo, "dados")
    caminho_json = os.path.join(pasta_dados, f"{ano_corrente}.json")
    chave_ano = str(ano_corrente)

    # Carregar dados existentes, formato {"2025": [ ... ]}
    if os.path.exists(caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}
        # Corrigir formato se necessário
        if not isinstance(dados, dict) or chave_ano not in dados or not isinstance(dados[chave_ano], list):
            dados = {chave_ano: []}
    else:
        dados = {chave_ano: []}

    concursos_existentes = {d["concurso"] for d in dados[chave_ano]}
    if resultado["concurso"] not in concursos_existentes:
        dados[chave_ano].append(resultado)
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print("Novo resultado adicionado ao JSON.")
    else:
        print("Resultado já existente. Nenhuma alteração feita.")

if __name__ == "__main__":
    resultado = extrair_totoloto()
    print("Último resultado Totoloto extraído:")
    print(resultado)
    salvar_no_json(resultado)
