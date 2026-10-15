import sqlite3

DB_PATH = "cyberbot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create a sample table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suscriptores (
            chat_id INTEGER PRIMARY KEY
        )
    """)
    
    conn.commit()
    conn.close()
    
def agregar_suscriptor(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()    
    cursor.execute('INSERT OR IGNORE INTO suscriptores (chat_id) VALUES (?)', (chat_id,))
    
    conn.commit()
    conn.close()

def quitar_suscriptor(chat_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM suscriptores WHERE chat_id = ?', (chat_id,))
    
    conn.commit()
    conn.close()
    
def obtener_suscriptores():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id FROM suscriptores')
    resultado = [fila[0] for fila in cursor.fetchall()]
    conn.close()
    return resultado
    