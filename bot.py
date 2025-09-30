# import logging
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
# from config import TELEGRAM_BOT_TOKEN
# from handlers.commands import start_command, help_command, date_command, weather_command
# from handlers.messages import handle_message
# from utils.gemini_client import crear_agente_conversacional

# # Configurar logs
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# # Crear y ejecutar la app
# def main(agente):
#     app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

#     # Comandos
#     app.add_handler(CommandHandler("start", start_command))
#     app.add_handler(CommandHandler("help", help_command))
#     app.add_handler(CommandHandler("fecha", date_command))
#     app.add_handler(CommandHandler("clima", weather_command))

#     # Mensajes normales usando el agente
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message(agente)))

#     print("Bot iniciado...")
#     app.run_polling()


# if __name__ == "__main__":
#     try:
#         agente = crear_agente_conversacional()
#         main(agente)
#     except Exception as e:
#         print(f"Error al iniciar el bot: {str(e)}")

import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN
from handlers.commands import start_command, help_command, date_command, weather_command
from handlers.messages import handle_message
from utils.gemini_client import crear_agente_conversacional

# Configurar logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Función principal para iniciar el bot"""
    try:
        # Crear el agente conversacional
        logger.info("Creando agente conversacional...")
        agente = crear_agente_conversacional()
        
        # Crear la aplicación del bot
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

        # Registrar comandos
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("fecha", date_command))
        app.add_handler(CommandHandler("clima", weather_command))

        # Registrar manejador de mensajes con el agente
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            handle_message(agente)
        ))

        logger.info(" Bot iniciado correctamente")
        print("🤖 Bot está corriendo... Presiona Ctrl+C para detener")
        
        # Iniciar el bot
        app.run_polling()
        
    except Exception as e:
        logger.error(f" Error al iniciar el bot: {str(e)}")
        raise


if __name__ == "__main__":
    main()