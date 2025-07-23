import os
import smtplib
from email.message import EmailMessage

def enviar_email(txt_path, remetente, senha_app, destinatario, assunto="Resultado Totoloto"):
    # Ler o conteúdo do ficheiro txt
    with open(txt_path, "r", encoding="utf-8") as f:
        corpo = f.read()

    msg = EmailMessage()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(remetente, senha_app)
            server.send_message(msg)
        print("Email enviado com sucesso.")
    except Exception as e:
        print("Erro ao enviar email:", e)

if __name__ == "__main__":
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINO")

    # Ajusta o caminho do txt conforme o teu projeto
    txt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dados/2025.txt")

    if not remetente or not senha_app or not destinatario:
        print("Por favor, configure as variáveis de ambiente EMAIL_REMETENTE, SENHA_APP e EMAIL_DESTINO.")
    else:
        enviar_email(txt_path, remetente, senha_app, destinatario)
