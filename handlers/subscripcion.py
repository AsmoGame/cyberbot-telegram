from telegram import Update
from telegram.ext import ContextTypes
from services.db import agregar_suscriptor, quitar_suscriptor

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    agregar_suscriptor(chat_id)
    await update.message.reply_text("✅ Te has suscrito a las noticias de ciberseguridad.")
    
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    quitar_suscriptor(chat_id)
    await update.message.reply_text("❌ Te has dado de baja de las noticias de ciberseguridad.")