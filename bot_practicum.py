import telebot
import sqlite3
import os

# El token se obtiene de la variable de entorno 'TOKEN'
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    print("ERROR: No se encontró el TOKEN. Asegúrate de establecer la variable de entorno 'TOKEN'.")
    exit(1)

bot = telebot.TeleBot(TOKEN)
DB_FILE = "chatbot.db"

def init_db():
    """
    Crea la base de datos y la tabla 'faq' si no existen,
    e inserta datos iniciales extraídos de la guía didáctica de Practicum.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT,
            respuesta TEXT
        )
    """)
    # Insertar datos iniciales solo si la tabla está vacía
    cursor.execute("SELECT COUNT(*) FROM faq")
    count = cursor.fetchone()[0]
    if count == 0:
        faq_entries = [
            ("¿Qué es Practicum?", 
             "Practicum es una asignatura orientada al desarrollo de prácticas preprofesionales, donde el estudiante aplica conocimientos y desarrolla competencias en entornos organizacionales."),
            ("¿Cuántas horas dura Practicum?", 
             "Las prácticas preprofesionales de la UTPL tienen una duración de 192 horas."),
            ("¿Cuáles son las competencias generales de Practicum?", 
             "Entre las competencias se encuentran el trabajo en equipo, la aplicación de buenas prácticas en TI y la capacidad de gestionar proyectos en entornos reales."),
            ("¿Qué metodologías se utilizan en Practicum?", 
             "Se utilizan metodologías basadas en proyectos y técnicas de levantamiento de información como encuestas, entrevistas, simulación y análisis de datos."),
            ("¿Cuál es el rol de los tutores en Practicum?", 
             "Existen dos roles: el tutor académico, que guía y acompaña al estudiante, y el tutor externo, que valida el cumplimiento de las actividades en la empresa.")
        ]
        cursor.executemany("INSERT INTO faq (pregunta, respuesta) VALUES (?, ?)", faq_entries)
    conn.commit()
    conn.close()

def buscar_respuesta(mensaje):
    """
    Busca en la base de datos una respuesta cuyo campo 'pregunta' coincida con el texto ingresado.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM faq WHERE LOWER(pregunta) LIKE ?", ('%' + mensaje.lower() + '%',))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Lo siento, no tengo información sobre ese tema. Intenta formular tu pregunta de otra forma o consulta la documentación disponible."

# Inicializar la base de datos al arrancar el bot
init_db()

@bot.message_handler(commands=["start", "help"])
def enviar_saludo(message):
    saludo = (
        "¡Hola! Soy tu asistente de Practicum.\n"
        "Puedes preguntarme cualquier duda relacionada con Practicum I y II, "
        "como información sobre metodologías, competencias, tutores, postulación y más.\n"
        "¿En qué puedo ayudarte hoy?"
    )
    bot.reply_to(message, saludo)

@bot.message_handler(func=lambda message: True)
def responder_duda(message):
    respuesta = buscar_respuesta(message.text)
    bot.reply_to(message, respuesta)

if __name__ == "__main__":
    print("Bot en ejecución...")
    bot.infinity_polling()
