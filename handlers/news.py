from telegram import Update
from telegram.ext import ContextTypes
from services.rss_feed import get_latest_news

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Obteniendo las últimas noticias de ciberseguridad...")
    noticias = get_latest_news()
    if not noticias:
        await update.message.reply_text("No se pudieron obtener noticias en este momento. Por favor, inténtalo más tarde.")
        return
    mensaje = "📰 Últimas noticias de ciberseguridad:\n\n"
    for n in noticias:
        mensaje += f"*{n['fuente']}*\n{n['titulo']}\n{n['link']}\n\n"
        
    await update.message.reply_text(mensaje, parse_mode="Markdown")
    