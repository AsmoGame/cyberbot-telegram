import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("El token del bot de Telegram no está configurado. Por favor, verifica tu archivo .env.")
