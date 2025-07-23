import os
import yaml
from datetime import datetime, timezone

WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows")

def ajustar_hora_cron(cron_str, usar_verao=True):
    partes = cron_str.split()
    if len(partes) < 2:
        return cron_str  # inválido, não altera
    
    minuto = partes[0]
    hora = int(partes[1])

    # Ajusta só se necessário: se já estiver correto, mantém
    if usar_verao and hora == ((hora - 1) % 24):
        nova_hora = (hora + 1) % 24
    elif not usar_verao and hora == ((hora + 1) % 24):
        nova_hora = (hora - 1) % 24
    else:
        # Parece que já está correto
        return cron_str

    partes[1] = str(nova_hora)
    return " ".join(partes)

def atualizar_crons_em_arquivo(filepath, usar_verao):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    horario_registado = data.get("horario", None)
    modo_atual = "verao" if usar_verao else "inverno"

    if horario_registado == modo_atual:
        print(f"{os.path.basename(filepath)} já está em {modo_atual}. Nenhuma alteração necessária.")
        return

    if "on" not in data or "schedule" not in data["on"]:
        print(f"'{os.path.basename(filepath)}' não tem schedule. Ignorando.")
        return

    schedules = data["on"]["schedule"]

    for i, cron_dict in enumerate(schedules):
        cron_antigo = cron_dict.get("cron")
        if cron_antigo:
            cron_novo = ajustar_hora_cron(cron_antigo, usar_verao)
            schedules[i]["cron"] = cron_novo

    # Atualiza o campo horario para o novo modo
    data["horario"] = modo_atual

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

    print(f"{os.path.basename(filepath)} atualizado para {modo_atual}.")

def detectar_modo():
    mes = datetime.now(timezone.utc).month
    return 3 <= mes <= 10

def main():
    usar_verao = detectar_modo()
    print(f"Modo atual detectado: {'Verão' if usar_verao else 'Inverno'}")

    for filename in os.listdir(WORKFLOWS_DIR):
        if filename.endswith((".yml", ".yaml")):
            if filename == "atualiza_horario.yml":
                print(f"Ignorando {filename}")
                continue
            filepath = os.path.join(WORKFLOWS_DIR, filename)
            atualizar_crons_em_arquivo(filepath, usar_verao)

if __name__ == "__main__":
    main()
