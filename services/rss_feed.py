import feedparser

FEED = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    }

def get_latest_news(limit_per_source=3):
    """Esto deberia de obtener los titutlos mas reciente de cada fuente """
    resultado = []
    for nombre_fuentes, url in FEED.items():
        feed = feedparser.parse(url)
        if feed.bozo:
            # El feed no se pudo parsear correctamentes se salta
            continue
        for entrada in feed.entries[:limit_per_source]:
            resultado.append({
                "fuente":nombre_fuentes,
                "titulo": entrada.get("title", "Sin titutlo"),
                "link": entrada.get("link", "Sin enlace")
            })
    return resultado