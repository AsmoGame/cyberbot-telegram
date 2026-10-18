#CyberBot

Bot de telegram gratuito enfocado en ciberseguridad noticias automaticas y analisis de URLS desconocidad 

## Pequena descripcion 
Este bot se hizo con la ayuda de claude, si ven algo que le hace falta o 
alguna parte no se ve correcta o hay alguna manera de mejorar el codigo, 
me lo hacen tener en cuenta para investigar y hacerle mejorar o si quieren 
que se pueda agregar otras cosa.

## Funcionalidades 
- **📰 Noticias de ciberseguridad** (`/news`): últimos titulares de The Hacker News y BleepingComputer.
- **🔔 Suscripción automática** (`/subscribe`, `/unsubscribe`): recibe noticias diarias sin pedirlas.
- **🔍 Analizador de phishing** (`/analyze <link o mensaje>`): detecta posibles intentos de phishing combinando:
  - Heurísticas propias: typosquatting, IPs en vez de dominios, TLDs sospechosos, frases de urgencia/presión.
  - VirusTotal API: reputación real contra 90+ motores antivirus.

## Stact Tecnico
- Python 3.12 + [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- SQLite (persistencia de suscriptores)
- APScheduler (envío programado)
- VirusTotal API v3
- feedparser (RSS)

## Arquitectura

\`\`\`
CyberBot/
├── bot.py              # Punto de entrada
├── config.py            # Variables de entorno
├── handlers/             # Lógica de comandos de Telegram
│   ├── basic.py
│   ├── news.py
│   ├── subscripcion.py
│   └── analyzer.py
├── services/             # Lógica de negocio
│   ├── rss_feed.py
│   ├── db.py
│   ├── url_analyzer.py
│   └── virustotal.py
└── requirements.txt
\`\`\`

## Instalación local

\`\`\`bash
git clone https://github.com/AsmoGame/cyberbot-telegram.git
cd cyberbot-telegram
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
\`\`\`

Crea un archivo \`.env\` con:
\`\`\`
TELEGRAM_BOT_TOKEN=tu_token_de_botfather
VIRUSTOTAL_API_KEY=tu_api_key_de_virustotal
\`\`\`

Ejecuta:
\`\`\`bash
python bot.py
\`\`\`

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `/start` | Inicia el bot |
| `/help` | Lista de comandos |
| `/news` | Últimas noticias de ciberseguridad |
| `/subscribe` | Activa noticias automáticas diarias |
| `/unsubscribe` | Desactiva noticias automáticas |
| `/analyze <link>` | Analiza un link o mensaje sospechoso |

## Roadmap / mejoras futuras

- [ ] Integración con Google Safe Browsing (tercera capa de detección)
- [ ] Deploy 24/7 (Railway)
- [ ] Validación del detector contra dataset de PhishTank
- [ ] Mejoras de UX (botones inline)

## Autor

Asmodeus — estudiante de ciberseguridad