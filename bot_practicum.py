
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from telegram.ext import ContextTypes  # Aquí está la corrección

# Configuración básica del logging para ver errores
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir los estados de la conversación
QUESTION_1, QUESTION_2, QUESTION_3, QUESTION_4, QUESTION_5 = range(5)

# Lista para guardar respuestas
answers = []

# Función que se llama cuando el usuario inicia el bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # Cambié CallbackContext por ContextTypes
    await update.message.reply_text(
        "¡Hola! Este chatbot recopilará tu experiencia en Practicum 1. \n\n"
        "Primera pregunta: ¿Cómo describirías tu experiencia general en la materia?"
    )
    return QUESTION_1

# Funciones para cada pregunta
async def question_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers.append(update.message.text)
    await update.message.reply_text("¿Qué actividades realizaste durante Practicum 1?")
    return QUESTION_2

async def question_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers.append(update.message.text)
    await update.message.reply_text("¿Cómo crees que estas actividades contribuyen a tu formación profesional?")
    return QUESTION_3

async def question_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers.append(update.message.text)
    await update.message.reply_text("¿Qué desafíos enfrentaste durante Practicum 1?")
    return QUESTION_4

async def question_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers.append(update.message.text)
    await update.message.reply_text("¿Cómo planeas aplicar lo aprendido en Practicum 1 en tu futuro profesional?")
    return QUESTION_5

async def question_5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answers.append(update.message.text)
    await update.message.reply_text("Gracias por compartir tu experiencia en Practicum 1. ¡Hasta luego!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Conversación cancelada.")
    return ConversationHandler.END

def main():
    # Reemplaza 'YOUR_BOT_API_KEY' con el token de tu bot de Telegram
    TOKEN = os.getenv("TOKEN")
    application = Application.builder().token(TOKEN).build()

    # Configuración del flujo de preguntas
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION_1: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_1)],
            QUESTION_2: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_2)],
            QUESTION_3: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_3)],
            QUESTION_4: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_4)],
            QUESTION_5: [MessageHandler(filters.TEXT & ~filters.COMMAND, question_5)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Iniciar el bot
    application.run_polling()

if __name__ == "__main__":
    main()
