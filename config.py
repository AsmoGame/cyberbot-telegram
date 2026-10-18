import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
if not TOKEN:
    raise ValueError("El token del bot de Telegram no está configurado. Por favor, verifica tu archivo .env.")

if not VIRUSTOTAL_API_KEY:
    raise ValueError("VIRUSTOTAL_API_KEY no encontrado. Revisa tu archivo .env")

