import telebot
import sqlite3

# ================================
# Chatbot de Asistencia para Practicum
# Universidad Técnica Particular de Loja (UTPL)
# Curso: Practicum I y II
# Autor: [Tu Nombre]
# Fecha: [Fecha de entrega]
#
# Descripción:
#   Este chatbot ha sido desarrollado para brindar asistencia y responder dudas
#   relacionadas con la asignatura Practicum, utilizando información extraída
#   de la guía didáctica. Se implementa en Python con pyTelegramBotAPI y utiliza
#   SQLite para almacenar preguntas frecuentes (FAQ) y sus respuestas.
#
# Nota:
#   En este ejemplo se utiliza directamente el token (por fines académicos),
#   pero en producción es recomendable utilizar variables de entorno para mayor seguridad.
# ================================

# Token del bot proporcionado por BotFather (insertado directamente)
TOKEN = "7622474169:AAG2hHAp1C1MAzI7WerytzTxEspkFLHix8M"

# Inicialización del bot
bot = telebot.TeleBot(TOKEN)

# Nombre del archivo de la base de datos SQLite
DB_FILE = "chatbot.db"

def init_db():
    """
    Inicializa la base de datos y crea la tabla 'faq' para almacenar
    preguntas frecuentes y sus respuestas. Si la tabla está vacía,
    inserta registros iniciales basados en la guía didáctica de Practicum.
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
    # Verificar si la tabla ya tiene registros
    cursor.execute("SELECT COUNT(*) FROM faq")
    count = cursor.fetchone()[0]
    if count == 0:
        faq_entries = [
            ("¿Qué es Practicum?",
             "Practicum es una asignatura orientada al desarrollo de prácticas preprofesionales, "
             "donde el estudiante aplica conocimientos teóricos en entornos reales para desarrollar "
             "competencias profesionales y enfrentar retos del mundo laboral."),
             
            ("¿Cuántas horas dura Practicum?",
             "En la UTPL, las prácticas preprofesionales tienen una duración de 192 horas, según lo establecido en la normativa."),
             
            ("¿Cuáles son las competencias generales de Practicum?",
             "Se desarrollan competencias como el trabajo en equipo, la aplicación de metodologías de TI, "
             "la gestión de proyectos y la solución de problemas en entornos reales."),
             
            ("¿Qué metodologías se utilizan en Practicum?",
             "Se emplean metodologías basadas en proyectos y técnicas de levantamiento de información como encuestas, "
             "entrevistas, simulaciones y análisis de datos para recabar información en entornos organizacionales."),
             
            ("¿Cuál es el rol de los tutores en Practicum?",
             "Existen dos roles: el tutor académico, que guía y acompaña al estudiante, y el tutor externo, "
             "que valida y supervisa las actividades en la empresa."),
             
            ("¿Cómo se postula a las prácticas preprofesionales?",
             "La postulación se realiza a través del portal oficial de la UTPL, siguiendo los lineamientos y normativas "
             "establecidos en la guía didáctica."),
             
            ("¿Qué recursos se utilizan en Practicum?",
             "Se utilizan recursos tecnológicos como bases de datos, sistemas y aplicaciones, infraestructura tecnológica "
             "y recursos informáticos para apoyar el desarrollo de la práctica.")
        ]
        cursor.executemany("INSERT INTO faq (pregunta, respuesta) VALUES (?, ?)", faq_entries)
    conn.commit()
    conn.close()

def buscar_respuesta(mensaje):
    """
    Busca en la base de datos una respuesta que coincida con la consulta del usuario.
    Se realiza una búsqueda simple utilizando 'LIKE' en la columna 'pregunta'.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT respuesta FROM faq WHERE LOWER(pregunta) LIKE ?", ('%' + mensaje.lower() + '%',))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado[0]
    else:
        return ("Lo siento, no dispongo de información sobre ese tema. Intenta formular tu pregunta "
                "de otra manera o consulta la documentación de Practicum para obtener más detalles.")

@bot.message_handler(commands=['start', 'help'])
def enviar_saludo(message):
    """
    Maneja los comandos /start y /help.
    Envía un mensaje de bienvenida explicando la funcionalidad del bot.
    """
    mensaje_bienvenida = (
        "¡Hola! Soy el asistente virtual de Practicum de la UTPL.\n\n"
        "Estoy aquí para ayudarte con cualquier duda relacionada con Practicum I y II, "
        "ya sea sobre metodologías, competencias, roles de tutores, postulación, recursos tecnológicos, etc.\n\n"
        "Por favor, escribe tu pregunta y haré lo posible por brindarte la información necesaria."
    )
    bot.send_message(message.chat.id, mensaje_bienvenida)

@bot.message_handler(func=lambda message: True)
def responder_duda(message):
    """
    Maneja cualquier consulta que realice el usuario.
    Busca en la base de datos la respuesta correspondiente y la envía.
    """
    consulta_usuario = message.text.strip()
    respuesta = buscar_respuesta(consulta_usuario)
    bot.send_message(message.chat.id, respuesta)

if __name__ == "__main__":
    # Inicializa la base de datos y crea la tabla si es necesario
    init_db()
    print("Bot en ejecución...")
    # Inicia el bot con polling infinito para mantenerlo activo
    bot.infinity_polling()
