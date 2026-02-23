# atualizar_eurodreams_sc.py

import json
import os
import re
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

def escrever_log(mensagem, origem):
    pasta_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_logs = os.path.join(pasta_repo, "logs")
    os.makedirs(pasta_logs, exist_ok=True)
    log_path = os.path.join(pasta_logs, "eurodreams_log.txt")
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{agora}] [{origem}] {mensagem}\n")

def ler_json(json_path, ano):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if str(ano) not in dados or not isinstance(dados[str(ano)], list):
            dados[str(ano)] = []
        return dados
    else:
        return {str(ano): []}

def gravar_json(json_path, dados):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def extrair_eurodreams_sc():
    url = "https://www.jogossantacasa.pt/web/ResultsBoard/EuroDreams"
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Extrair concurso e data
        span_data_info = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.dataInfo"))
        )
        texto = span_data_info.get_attribute("innerHTML").replace("<br>", "\n")
        linhas = texto.split("\n")

        concurso = re.search(r"\d{3}/\d{4}", linhas[0]).group(0)
        data_sorteio = re.search(r"\d{2}/\d{2}/\d{4}", linhas[1]).group(0)

        # Extrair chave
        chave_ul = driver.find_element(By.CSS_SELECTOR, "div.betMiddle.twocol.regPad ul.colums")
        itens = chave_ul.find_elements(By.TAG_NAME, "li")

        chave_ordenada = itens[0].text.strip()
        chave_saida = itens[1].text.strip()

        # Extrair prémios
        premios = []
        try:
            listas = driver.find_elements(
                By.CSS_SELECTOR,
                "div.stripped.betMiddle.customfiveCol.regPad ul.colums"
            )

            for ul in listas:
                itens = ul.find_elements(By.TAG_NAME, "li")
                if len(itens) >= 5:
                    premio = itens[0].text.strip()
                    descricao = itens[1].text.strip()
                    vencedores_pt = itens[2].text.strip()
                    vencedores_eu = itens[3].text.strip()
                    valor = itens[4].text.strip()

                    premios.append({
                        "premio": premio,
                        "descricao": descricao,
                        "vencedores_pt": vencedores_pt,
                        "vencedores_eu": vencedores_eu,
                        "valor": valor
                    })

        except Exception as e:
            escrever_log(f"Erro ao extrair prémios: {e}", "eurodreams")

        return {
            "concurso": concurso,
            "data": data_sorteio,
            "chave_ordenada": chave_ordenada,
            "chave_saida": chave_saida,
            "premios": premios
        }

    finally:
        driver.quit()

def atualizar_resultados():
    resultado = extrair_eurodreams_sc()
    ano = resultado["concurso"].split("/")[1]

    pasta_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_dados = os.path.join(pasta_repo, "dados_eurodreams")
    os.makedirs(pasta_dados, exist_ok=True)

    json_path = os.path.join(pasta_dados, f"{ano}.json")

    # Guardar no TXT
    txt_path = os.path.join(pasta_dados, f"{ano}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Concurso: {resultado['concurso']}\n")
        f.write(f"Data: {resultado['data']}\n")
        f.write(f"Chave: {resultado['chave_ordenada']}\n")
        f.write(f"Ordem de saída: {resultado['chave_saida']}\n")
        f.write("-" * 40 + "\n")

        f.write("Prémios:\n")
        for p in resultado["premios"]:
            f.write(
                f"{p['premio']} - {p['descricao']} | "
                f"PT: {p['vencedores_pt']} | EU: {p['vencedores_eu']} | Valor: {p['valor']}\n"
            )
        f.write("-" * 40 + "\n")

    # JSON mantém apenas dados essenciais
    dados = ler_json(json_path, ano)
    lista = dados[str(ano)]

    existe = any(r["concurso"] == resultado["concurso"] for r in lista)
    if not existe:
        lista.append({
            "concurso": resultado["concurso"],
            "data": resultado["data"],
            "chave": resultado["chave_ordenada"],
            "ordem_saida": resultado["chave_saida"]
        })
        lista.sort(key=lambda r: r["concurso"])
        dados[str(ano)] = lista
        gravar_json(json_path, dados)

if __name__ == "__main__":
    atualizar_resultados()
