import re 
import tldextract
import Levenshtein 

#Dominio legitimos comunes a proteger contra typosquiatiting

DOMINIOS_LEGITIMOS = [
    "google.com",
    "facebook.com",
    "twitter.com",
    "instagram.com",
    "linkedin.com",
    "github.com",
    "paypal.com",
    "amazon.com",
    "apple.com",
    "microsoft.com",
    "whatsapp.com",
    "youtube.com",
    "netflix.com",
]

PALABRAS_CLAVE = [
    "login",
    "secure",
    "account",
    "update",
    "verify",
    "bank",
    "paypal",
    "Vrificar Cuenta",
    "cuenta bloqueada",
    "cuenta suspendida",
    "cuenta comprometida",
    "cuenta inactiva",
    "cuenta desactivada",
    "cuenta no verificada",
    "cuenta no segura",
    "cuenta no actualizada",
    "premio",
    "codigo de verificacion"
]

def extraer_url(texto):
    """Extrae la primera URL de un texto dado"""
    patron = r"https?://[^\s]+|www\.[^\s]+"
    return re.findall(patron, texto)

def es_ip(dominio):
    """Verifica si el dominio es en realidad una IP"""
    patron_ip = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return bool(re.match(patron_ip, dominio))

def detectar_typosquatting(dominio_completo):
    """Detecta si una URL es un posible caso de typosquatting"""
    for conocido in DOMINIOS_LEGITIMOS:
        distancia = Levenshtein.distance(dominio_completo, conocido)
        if 0 < distancia <= 2:
            return conocido
    return None

def analizar_url(url):
    """Analiza una URL y devuelve una lista de alertas encontradas."""
    alertas = []

    extraido = tldextract.extract(url)
    dominio_completo = f"{extraido.domain}.{extraido.suffix}"

    if es_ip(extraido.domain):
        alertas.append(" El enlace usa una dirección IP en vez de un dominio normal — muy común en phishing.")

    parecido = detectar_typosquatting(dominio_completo)
    if parecido:
        alertas.append(f" El dominio '{dominio_completo}' se parece sospechosamente a '{parecido}' (posible typosquatting).")

    tlds_sospechosos = ["tk", "ml", "ga", "cf", "gq", "xyz"]
    if extraido.suffix in tlds_sospechosos:
        alertas.append(f" El dominio usa una extensión ('.{extraido.suffix}') frecuentemente asociada a sitios maliciosos.")

    return alertas

def analizar_texto(texto):
    """Analiza un texto en busca de URLs y devuelve alertas sobre posibles riesgos."""
    resultado = {
        "urls_encontradas": [],
        "alertas": [],
        "nivel_riesgo": "Bajo"
    }

    urls = extraer_url(texto)
    for url in urls:
        alertas_url = analizar_url(url)
        resultado["urls_encontradas"].append(url)
        resultado["alertas"].extend(alertas_url)
        
    texto_lower = texto.lower()
    for palabra in PALABRAS_CLAVE:
        if palabra in texto_lower:
            resultado["alertas"].append(f" Se encontró la palabra clave '{palabra}' en el texto, lo cual puede indicar un intento de phishing.")
            
    #Calcular el nivel de riesgo segun la cantidad de alertas 
    n_alertas = len(resultado["alertas"])
    if n_alertas >= 5:
        resultado["nivel_riesgo"] = "Alto"
    elif n_alertas >= 3:
        resultado["nivel_riesgo"] = "Medio"
    
    return resultado