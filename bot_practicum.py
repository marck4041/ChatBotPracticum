import telebot
import sqlite3
import os

# ================================
# Chatbot de Asistencia para Practicum
# UTPL - Prácticas Preprofesionales
# ================================

# Obtener el token desde las variables de entorno (Railway lo usará)
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("ERROR: No se encontró el TOKEN. Asegúrate de configurarlo en Railway.")
    exit(1)

bot = telebot.TeleBot(TOKEN)

# Nombre del archivo de la base de datos SQLite
DB_FILE = "chatbot.db"

def init_db():
    """
    Inicializa la base de datos y crea la tabla 'faq' si no existe.
    Si la tabla está vacía, inserta registros iniciales con información de Practicum.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            respuesta TEXT NOT NULL
        )
    """)

    # Verificar si la tabla tiene registros
    cursor.execute("SELECT COUNT(*) FROM faq")
    count = cursor.fetchone()[0]
    if count == 0:
        faq_entries = [
            ("¿Qué es Practicum?", "Es una asignatura para realizar prácticas preprofesionales en empresas o instituciones."),
            ("¿Cuántas horas dura Practicum?", "Practicum en la UTPL tiene una duración de 192 horas."),
            ("¿Cómo se postula a Practicum?", "Debes postularte a través del portal de prácticas preprofesionales de la UTPL."),
            ("¿Qué debo entregar en Practicum?", "Debes presentar informes semanales y una evaluación final de tu tutor."),
            ("¿Dónde realizo mis prácticas?", "En empresas con convenios con la UTPL o en dependencias universitarias."),
            ("¿Qué pasa si no completo las horas?", "Debes solicitar una extensión con tu tutor."),
        ]
        cursor.executemany("INSERT INTO faq (pregunta, respuesta) VALUES (?, ?)", faq_entries)
    conn.commit()
    conn.close()

def buscar_respuesta(mensaje):
    """
    Busca en la base de datos una respuesta relacionada con la consulta del usuario.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM faq WHERE LOWER(pregunta) LIKE ?", ('%' + mensaje.lower() + '%',))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Lo siento, no tengo información sobre eso. Intenta preguntar de otra manera."

@bot.message_handler(commands=['start', 'help'])
def enviar_saludo(message):
    """
    Responde con un mensaje de bienvenida cuando el usuario envía /start o /help.
    """
    mensaje_bienvenida = (
        "¡Hola! Soy el bot de asistencia de Practicum UTPL. "
        "Puedes preguntarme sobre horarios, postulación, requisitos y más. "
        "Escribe tu pregunta y te responderé con la mejor información disponible."
    )
    bot.send_message(message.chat.id, mensaje_bienvenida)

@bot.message_handler(func=lambda message: True)
def responder_duda(message):
    """
    Maneja cualquier consulta del usuario y busca la mejor respuesta en la base de datos.
    """
    consulta_usuario = message.text.strip()
    respuesta = buscar_respuesta(consulta_usuario)
    bot.send_message(message.chat.id, respuesta)

if __name__ == "__main__":
    init_db()  # Inicializa la base de datos antes de arrancar el bot
    print("Bot en ejecución...")
    bot.infinity_polling()
