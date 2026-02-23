# atualizar_m1lhao_sc.py

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
    log_path = os.path.join(pasta_logs, "m1lhao_log.txt")
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

def extrair_m1lhao_sc():
    url = "https://www.jogossantacasa.pt/web/SCCartazResult/m1lhao"
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

        # Extrair código vencedor
        ul_premio = driver.find_element(By.CSS_SELECTOR, "div.stripped.betMiddle3.threecol.regPad ul")
        itens = ul_premio.find_elements(By.TAG_NAME, "li")

        premio_nome = itens[0].text.strip()
        codigo = itens[1].text.strip()
        vencedores = itens[2].text.strip()

        # Extrair estatísticas
        estatisticas = []
        listas = driver.find_elements(By.CSS_SELECTOR, "div.betMiddle.twocol ul.noLine")

        for ul in listas:
            li = ul.find_elements(By.TAG_NAME, "li")
            if len(li) >= 2:
                estatisticas.append({
                    "nome": li[0].text.strip(),
                    "valor": li[1].text.strip()
                })

        return {
            "concurso": concurso,
            "data": data_sorteio,
            "codigo": codigo,
            "premio_nome": premio_nome,
            "vencedores": vencedores,
            "estatisticas": estatisticas
        }

    finally:
        driver.quit()

def atualizar_resultados():
    resultado = extrair_m1lhao_sc()
    ano = resultado["concurso"].split("/")[1]

    pasta_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_dados = os.path.join(pasta_repo, "dados_m1lhao")
    os.makedirs(pasta_dados, exist_ok=True)

    json_path = os.path.join(pasta_dados, f"{ano}.json")

    # Guardar no TXT
    txt_path = os.path.join(pasta_dados, f"{ano}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Concurso: {resultado['concurso']}\n")
        f.write(f"Data: {resultado['data']}\n")
        f.write(f"Código vencedor: {resultado['codigo']}\n")
        f.write(f"Vencedores: {resultado['vencedores']}\n")
        f.write("-" * 40 + "\n")

        f.write("Estatísticas:\n")
        for e in resultado["estatisticas"]:
            f.write(f"{e['nome']}: {e['valor']}\n")
        f.write("-" * 40 + "\n")

    # JSON mantém apenas dados essenciais
    dados = ler_json(json_path, ano)
    lista = dados[str(ano)]

    existe = any(r["concurso"] == resultado["concurso"] for r in lista)
    if not existe:
        lista.append({
            "concurso": resultado["concurso"],
            "data": resultado["data"],
            "codigo": resultado["codigo"]
        })
        lista.sort(key=lambda r: r["concurso"])
        dados[str(ano)] = lista
        gravar_json(json_path, dados)

if __name__ == "__main__":
    atualizar_resultados()
