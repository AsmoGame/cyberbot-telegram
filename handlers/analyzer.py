from telegram import Update
from telegram.ext import ContextTypes
from services.url_analyzer import analizar_texto
from services.virustotal import consultar_virustotal

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
    
    mensaje = ""
    
    if resultado["urls_encontradas"]:
        mensaje += f"🔗 URLs analizadas: {len(resultado['urls_encontradas'])}\n\n"

        # Consulta VirusTotal para cada URL encontrada
        for url in resultado["urls_encontradas"]:
            vt_resultado = consultar_virustotal(url)

            if vt_resultado is None:
                mensaje += f"⚠️ No se pudo consultar VirusTotal para: {url}\n\n"
            elif vt_resultado.get("pendiente"):
                mensaje += f"⏳ {url} se envió a análisis, intenta de nuevo en unos minutos.\n\n"
            else:
                maliciosos = vt_resultado["maliciosos"]
                sospechosos = vt_resultado["sospechosos"]
                total = vt_resultado["total_motores"]

                mensaje += f"🛡️ VirusTotal: {maliciosos}/{total} motores lo marcan como malicioso"
                if sospechosos:
                    mensaje += f", {sospechosos} como sospechoso"
                mensaje += "\n\n"

                # Si VirusTotal detecta algo, subimos el nivel de riesgo
                if maliciosos >= 3:
                    nivel = "alto"
                elif maliciosos >= 1 and nivel == "bajo":
                    nivel = "medio"

    emoji = EMOJI_RIESGO[nivel]
    mensaje = f"{emoji} Nivel de riesgo: {nivel.upper()}\n\n" + mensaje

    if resultado["alertas"]:
        mensaje += "⚠️ Alertas encontradas (heurísticas):\n"
        for alerta in resultado["alertas"]:
            mensaje += f"- {alerta}\n"
    else:
        mensaje += "✅ No se encontraron alertas de heurísticas.\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")    