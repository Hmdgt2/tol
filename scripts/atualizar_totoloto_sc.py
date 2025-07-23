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
    # Grave em logs/ ou na raiz
    pasta_logs = os.path.join(pasta_repo, "logs")
    os.makedirs(pasta_logs, exist_ok=True)
    log_path = os.path.join(pasta_logs, "totoloto_log.txt")
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

def extrair_totoloto_sc():
    url = "https://www.jogossantacasa.pt/web/SCCartazResult/totolotoNew"
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)
        span_data_info = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.dataInfo"))
        )
        texto_sorteio = span_data_info.text.strip()
        linhas = texto_sorteio.split("\n")
        concurso = re.search(r"\d{3}/\d{4}", linhas[0]).group(0)
        data_sorteio = re.search(r"\d{2}/\d{2}/\d{4}", linhas[1]).group(0)
        chave_li = driver.find_element(By.CSS_SELECTOR, "div.betMiddle.twocol.regPad ul.colums li")
        chave_texto = chave_li.text.strip()
        partes = chave_texto.split("+")
        numeros = list(map(int, partes[0].strip().split()))
        especial = int(partes[1].strip())
        return {
            "concurso": concurso,
            "data": data_sorteio,
            "numeros": numeros,
            "especial": especial
        }
    finally:
        driver.quit()

def atualizar_resultados():
    resultado = extrair_totoloto_sc()
    ano = resultado["concurso"].split("/")[1]
    pasta_repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pasta_dados = os.path.join(pasta_repo, "dados")
    os.makedirs(pasta_dados, exist_ok=True)
    json_path = os.path.join(pasta_dados, f"{ano}.json")

    dados = ler_json(json_path, ano)
    lista = dados[str(ano)]

    existe = any(r["concurso"] == resultado["concurso"] for r in lista)
    if existe:
        msg = f"Resultado do concurso {resultado['concurso']} já existe. Nada a fazer."
        print(msg)
        escrever_log(msg)
    else:
        lista.append(resultado)
        lista.sort(key=lambda r: r["concurso"])
        dados[str(ano)] = lista
        gravar_json(json_path, dados)
        msg = f"Resultado do concurso {resultado['concurso']} adicionado ao JSON {ano}."
        print(msg)
        escrever_log(msg)

if __name__ == "__main__":
    atualizar_resultados()
