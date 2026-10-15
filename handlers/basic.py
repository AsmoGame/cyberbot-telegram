from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu bot de ciberseguridad.\n"
        "Usa /help para ver qué puedo hacer."
    )
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar\n"
        "/help - Ayuda\n"
        "/news - Ultimas noticias de ciberseguridadn\n"    
        "/subscribete - Recibe Noticias Automaticas Diarias\n"
        "/unsubscribe - Dejar de recibir notificaciones\n"
        
        )
        