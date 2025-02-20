import telebot
import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import math

# Descargar datos de NLTK (solo la primera vez)
nltk.download("punkt")

# 🔹 Token del bot
TOKEN = "7622474169:AAG2hHAp1C1MAzI7WerytzTxEspkFLHix8M"

# 🔹 Inicialización del bot
bot = telebot.TeleBot(TOKEN)

# 🔹 Diccionario de respuestas basado en el menú
menu_respuestas = {
    "1": "📌 **Horas requeridas:** Debes completar **192 horas** de prácticas.",
    "2": "🖥 **Plataforma de registro:** Utiliza la aplicación de **PowerApps** para registrar tus prácticas. Puedes acceder desde aquí: [PowerApps](https://bit.ly/41aJMdb).",
    "3": "✅ **Aprobación:** Para aprobar necesitas obtener al menos el **70% de la nota** 📝 y completar el **100% de las horas requeridas**, además de presentar un **certificado** que acredite tus prácticas.",
    "4": "📑 **Informes y entregables:** Debes entregar **1 informe** con **3 avances graduales** y **3 entregables separados**.",
    "5": "🎥 **Videocolaboraciones:** Habrá **2 videocolaboraciones** con tu tutor, donde deberás demostrar tus conocimientos y experiencias adquiridas.",
    "6": "📝 **Calificación:** Las actividades que contribuyen a tu **calificación final** incluyen informes, entregables y videocolaboraciones.",
    "7": "📄 **Formato de entregables:** Todos los entregables deben seguir el **formato APA 7ma edición**.",
    "8": "📂 **Contenido de entregables:** Debes incluir **trabajos realizados, evidencias, capturas de pantalla, etc.**",
    "9": "📌 **Postulación a plazas:** Puede postularte a plazas disponibles o proponer una nueva utilizando la aplicación de **PowerApps**.",
    "10": "📜 **Validación de prácticas previas:** Si has participado en prácticas antes, puedes validar esta asignatura presentando los **documentos correspondientes** a través del servicio en línea de la UTPL.",
}

# 🔹 Contactos de tutores
contactos_tutores = (
    "📧 **Contactos de tutores:**\n"
    "- **PhD. Daniel Alejandro Guaman** (Director de carrera TIC) → [daguaman@utpl.edu.ec](mailto:daguaman@utpl.edu.ec)\n"
    "- **PhD. Liliana Elvira Enciso** (Tutora de Practicum) → [lenciso@utpl.edu.ec](mailto:lenciso@utpl.edu.ec)"
)

@bot.message_handler(commands=['start', 'help'])
def enviar_saludo(message):
    """Presentación mejorada para estudiantes universitarios."""
    mensaje_bienvenida = (
        "👋 **¡Hola, futuro profesional!**\n\n"
        "🎓 Soy el *Chatbot de Practicum UTPL* y estoy aquí para ayudarte con toda la info sobre tu práctica preprofesional.\n"
        "Si tienes dudas, pregúntame sobre:\n\n"
        "📌 *Postulación* – ¿Cómo inscribirte?\n"
        "📋 *Requisitos* – Lo que necesitas para participar\n"
        "⏳ *Registro de horas* – ¿Dónde y cómo registrar tus avances?\n"
        "📝 *Evaluaciones* – Cómo se califica y qué debes presentar\n"
        "📁 *Entregables* – Documentos y reportes que debes subir\n"
        "📅 *Tutorías* – Cómo contactar a tu tutor académico\n\n"
        "💡 **Tip:** Usa /menu para ver todas las opciones disponibles.\n\n"
        "¡Estoy listo para ayudarte! 🚀"
    )
    bot.send_message(message.chat.id, mensaje_bienvenida, parse_mode="Markdown")

@bot.message_handler(commands=['menu'])
def enviar_menu(message):
    """Envía un menú con las preguntas más frecuentes."""
    menu_texto = (
        "📌 **Menú de Preguntas Frecuentes** 📌\n\n"
        "1️⃣ **Horas requeridas**\n"
        "2️⃣ **Plataforma de registro**\n"
        "3️⃣ **Aprobación**\n"
        "4️⃣ **Informes y entregables**\n"
        "5️⃣ **Videocolaboraciones**\n"
        "6️⃣ **Calificación**\n"
        "7️⃣ **Formato de entregables**\n"
        "8️⃣ **Contenido de entregables**\n"
        "9️⃣ **Postulación a plazas**\n"
        "🔟 **Validación de prácticas previas**\n\n"
        "✍️ Escribe el **número** sobre el que necesitas información."
    )
    bot.send_message(message.chat.id, menu_texto, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text.strip().isdigit() and message.text.strip() in menu_respuestas)
def responder_menu(message):
    """Responde a las preguntas del menú según el número enviado."""
    respuesta = menu_respuestas[message.text.strip()]
    bot.send_message(message.chat.id, respuesta, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def responder_duda(message):
    """Recibe la pregunta del usuario y busca la mejor respuesta."""
    pregunta_usuario = message.text.strip()
    
    if pregunta_usuario in ["tutor", "contacto", "tutores", "correo"]:
        bot.send_message(message.chat.id, contactos_tutores, parse_mode="Markdown")
        return

    respuesta = "🤔 No encontré información exacta. ¿Podrías reformular tu pregunta?"
    bot.send_message(message.chat.id, respuesta, parse_mode="Markdown")

if __name__ == "__main__":
    print("🔹 Iniciando bot de Practicum UTPL...")
    print("🤖 Bot en ejecución...")
    bot.infinity_polling()
