"""import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"Token cargado: '{TOKEN}'")
print(f"Longitud: {len(TOKEN) if TOKEN else 0}")


logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu bot de ciberseguridad.\n"
        "Usa /help para ver qué puedo hacer."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar\n"
        "/help - Ayuda"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Recibí: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling()

if __name__ == "__main__":
    main()"""
    
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TOKEN
from handlers.basic import start, help_command
from handlers.news import news
from handlers.subscripcion import subscribe, unsubscribe
from services.db import init_db, obtener_suscriptores
from services.rss_feed import get_latest_news, format_news_message

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def echo(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Recibí: {update.message.text}")
async def enviar_noticias_diarias(context: ContextTypes.DEFAULT_TYPE):
    noticias = get_latest_news()
    mensaje = format_news_message(noticias)
    
    if not mensaje:
        return  # No hay noticias para enviar
    
    for chat_id in obtener_suscriptores():
        try:
            await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode="Markdown")
        except Exception as e:
            logging.warning(f"Error al enviar noticias a {chat_id}: {e}")
def main():
    init_db()  # Inicializa la base de datos y crea la tabla si no existe
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Programa el envio diario a las 8 de la mañana
    app.job_queue.run_daily(enviar_noticias_diarias, time=__import__("datetime").time(hour=8, minute=0, second=0))
    
    app.run_polling()

if __name__ == "__main__":
    main()