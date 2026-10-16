from telegram import Update
from telegram.ext import ContextTypes
from services.url_analyzer import analizar_texto

EMOJI_RIESGO = {
    "bajo": "🟢",
    "medio": "🟡",
    "alto": "🔴"
}

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text.replace("/analyze", "", 1).strip()

    if not texto:
        await update.message.reply_text(
            "Por favor, proporciona un texto para analizar.\n"
            "Ejemplo: /analyze https://gogle-verificacion.tk/login"
        )
        return

    resultado = analizar_texto(texto)
    nivel = resultado["nivel_riesgo"].lower()
    emoji = EMOJI_RIESGO[nivel]

    mensaje = f"{emoji} Nivel de riesgo: {nivel.upper()}\n\n"

    if resultado["urls_encontradas"]:
        mensaje += f"🔗 URLs analizadas: {len(resultado['urls_encontradas'])}\n\n"

    if resultado["alertas"]:
        mensaje += "⚠️ Alertas encontradas:\n"
        for alerta in resultado["alertas"]:
            mensaje += f"- {alerta}\n"
    else:
        mensaje += "✅ No se encontraron alertas.\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")