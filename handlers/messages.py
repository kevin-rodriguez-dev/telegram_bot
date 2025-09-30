import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

logger = logging.getLogger(__name__)

def handle_message(agente):
    """
    Crea un manejador de mensajes que usa el agente conversacional
    """
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        
        try:
            # Mostrar indicador de "escribiendo"
            await update.message.chat.send_action(ChatAction.TYPING)
            
            # Invocar el agente para obtener respuesta
            response = await agente.ainvoke(user_message)
            
            # Extraer el texto de la respuesta
            if isinstance(response, dict):
                response_text = response.get('output', str(response))
            else:
                response_text = str(response)
            
            # Enviar respuesta al usuario
            await update.message.reply_text(response_text)
            
        except Exception as e:
            logger.error(f"Error al procesar mensaje: {str(e)}")
            error_message = (
                " Lo siento, ocurrió un error al procesar tu mensaje.\n"
                "Por favor, intenta de nuevo o usa /help para ver los comandos disponibles."
            )
            await update.message.reply_text(error_message)
    
    return handle