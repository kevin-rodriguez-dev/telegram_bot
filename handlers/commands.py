from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from utils.tools import ClimaAPI

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Mensaje de bienvenida"""
    welcome_message = (
        "¡Hola! Soy tu asistente virtual inteligente.\n\n"
        "Puedo ayudarte con varias cosas:\n"
        "- Responder preguntas generales\n"
        "- Consultar el clima\n"
        "- Informarte la fecha y hora\n\n"
        "Escribe /help para ver todos los comandos disponibles."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Muestra los comandos disponibles"""
    help_text = (
        "*Comandos Disponibles:*\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar este mensaje de ayuda\n"
        "/fecha - Obtener la fecha y hora actual\n"
        "/clima [ciudad] - Consultar el clima de una ciudad\n\n"
        "También puedes escribirme cualquier pregunta y te responderé."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def date_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /fecha - Muestra la fecha y hora actual"""
    try:
        await update.message.chat.send_action("typing")
        
        current_date = datetime.now()
        
        # Formatear fecha en español
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        
        dia_semana = dias[current_date.weekday()]
        mes = meses[current_date.month - 1]
        
        formatted_date = (
            f"*Fecha y Hora Actual*\n\n"
            f"Hoy es {dia_semana.capitalize()}, {current_date.day} de {mes} de {current_date.year}\n"
            f"{current_date.strftime('%H:%M:%S')}"
        )
        
        await update.message.reply_text(formatted_date, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f" Error al obtener la fecha: {str(e)}")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /clima - Consulta el clima de una ciudad"""
    try:
        if not context.args:
            await update.message.reply_text(
                "⚠️ Por favor especifica una ciudad.\n"
                "Ejemplo: `/clima San Salvador`",
                parse_mode="Markdown"
            )
            return
        
        ciudad = " ".join(context.args)
        
        # Mostrar indicador de "escribiendo..."
        await update.message.chat.send_action("typing")
        
        # Obtener clima usando la herramienta
        clima_tool = ClimaAPI()
        resultado = clima_tool.obtener_clima(ciudad)
        
        await update.message.reply_text(resultado, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f" Error al consultar el clima: {str(e)}")