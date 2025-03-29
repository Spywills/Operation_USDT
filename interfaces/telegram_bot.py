import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("[ERRO] TOKEN ou CHAT_ID não configurados.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if not response.ok:
            print(f"[ERRO Telegram] {response.text}")
    except Exception as e:
        print(f"[EXCEÇÃO Telegram] {e}")
