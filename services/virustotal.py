import base64
import requests
import logging
from config import VIRUSTOTAL_API_KEY

VT_API_SCAN = "https://www.virustotal.com/api/v3/urls"

def _codificar_url(url):
    """
    Codifica la URL en base64 y la devuelve en formato URL-safe.
    """
    url_bytes = url.encode('utf-8')
    url_b64 = base64.urlsafe_b64encode(url_bytes).decode("utf-8").rstrip("=")
    return url_b64

def consultar_virustotal(url):
    """
    Consulta el analisis existente de una URL en VirusTotal
    Devuelve un diccionario con el resultado, o None si hubo un error 
    """
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    url_id = _codificar_url(url)

    try:
        respuesta = requests.get(
            f"{VT_API_SCAN}/{url_id}",
            headers=headers,
            timeout=10
        )

        #logging.info(f"VirusTotal status code: {respuesta.status_code}")
        #logging.info(f"VirusTotal response: {respuesta.text[:300]}")

        if respuesta.status_code == 404:
            return _enviar_para_analisis(url, headers)

        if respuesta.status_code != 200:
            return None

        datos = respuesta.json()
        stats = datos["data"]["attributes"]["last_analysis_stats"]
        return {
            "maliciosos": stats.get("malicious", 0),
            "sospechosos": stats.get("suspicious", 0),
            "inofensivos": stats.get("harmless", 0),
            "sin_detectar": stats.get("undetected", 0),
            "total_motores": sum(stats.values())
        }
    except requests.exceptions.RequestException as e:
        #logging.error(f"Error al consultar VirusTotal: {e}")
        return None

def _enviar_para_analisis(url, headers):
    """
    Envía la URL a VirusTotal para su análisis.
    """
    try:
        respuesta = requests.post(
            VT_API_SCAN,
            headers=headers,
            files={"url": (None, url)},
            timeout=10
        )

        #logging.info(f"VirusTotal POST status code: {respuesta.status_code}")
        #logging.info(f"VirusTotal POST response: {respuesta.text[:300]}")

        if respuesta.status_code == 200:
            return {"pendiente": True}
        return None

    except requests.exceptions.RequestException as e:
        #logging.error(f"Error al enviar URL a VirusTotal: {e}")
        return None