import os
import yaml
from datetime import datetime

WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), "..", ".github", "workflows")

#  Crons para cada modo (exemplo baseado no que mostraste)
CRONS_VERAO = [
    "10 8 * * 4",
    "10 8 * * 0",
    "11 0 * * 2",
    "40 19 * * 3",
    "40 19 * * 6",
    "2 8 * * 4",
    "2 8 * * 0",
    "3 0 * * 2",
    "15 8 * * 4",
    "15 8 * * 0",
    "16 0 * * 2",
]

CRONS_INVERNO = [
    "9 8 * * 4",
    "9 8 * * 0",
    "10 0 * * 2",
    "39 18 * * 3",
    "39 18 * * 6",
    "1 8 * * 4",
    "1 8 * * 0",
    "2 0 * * 2",
    "14 8 * * 4",
    "14 8 * * 0",
    "15 0 * * 2",
]

def detectar_modo():
    mes = datetime.utcnow().month
    # Horário de verão de março a outubro (inclusive)
    if 3 <= mes <= 10:
        return "verao"
    return "inverno"

def atualizar_crons_em_arquivo(filepath, usar_verao):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "on" not in data or "schedule" not in data["on"]:
        print(f"'{os.path.basename(filepath)}' não tem schedule. Ignorando.")
        return

    schedules = data["on"]["schedule"]
    total_crons = len(schedules)

    novos_crons = CRON_VERAO if usar_verao else CRON_INVERNO

    # Ajusta para o número de schedules existentes, reutilizando os crons conforme possível
    for i in range(total_crons):
        cron_novo = novos_crons[i] if i < len(novos_crons) else novos_crons[-1]
        schedules[i]["cron"] = cron_novo

    with open(filepath, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)

    print(f"{os.path.basename(filepath)} atualizado para {'Verão' if usar_verao else 'Inverno'}.")

def main():
    modo = detectar_modo()
    usar_verao = modo == "verao"
    print(f"Modo atual detectado: {'Verão' if usar_verao else 'Inverno'}")

    for filename in os.listdir(WORKFLOWS_DIR):
        if filename.endswith(".yml") or filename.endswith(".yaml"):
            if filename == "atualiza_horario.yml":
                print(f"Ignorando {filename}")
                continue
            filepath = os.path.join(WORKFLOWS_DIR, filename)
            atualizar_crons_em_arquivo(filepath, usar_verao)

if __name__ == "__main__":
    main()
