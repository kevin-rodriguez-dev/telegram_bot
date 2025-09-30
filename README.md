# 🤖 Bot de Telegram con Google Gemini AI

Este proyecto utiliza **Python**, la API de **Google Gemini** y el framework **LangChain** para crear un bot interactivo, integrando también la librería `python-telegram-bot` para su uso en Telegram.

## Tecnologías Utilizadas

- Python 3.9+
- LangChain
- langchain-google-genai
- Google Gemini API
- python-telegram-bot
- requests
- python-dotenv

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   ```

2. **Crea y activa un entorno virtual**:
   ```bash
   py -m venv bot_env
   ```

   - En **Windows**:
     ```bash
     bot_env\Scripts\activate
     ```
   
   - En **macOS/Linux**:
     ```bash
     source bot_env/bin/activate
     ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**:
   
   Crea un archivo `.env` en la raíz del proyecto:
   ```env
   TELEGRAM_BOT_TOKEN=
   GEMINI_API_KEY=
   WEATHER_API_KEY
   WEATHER_BASE_URL
   ```

   **Obtener las API Keys:**
   - **Telegram Bot Token**: Habla con [@BotFather](https://t.me/BotFather) en Telegram
   - **Gemini API Key**: Regístrate en [Google AI Studio](https://ai.google.dev/)
   - **Weather API Key**: Regístrate en [Weather api](https://www.weatherapi.com/)

5. **Ejecutar el Bot**
   ```bash
   python bot.py || py bot.py
   ```
   
## Comandos Disponibles
   
| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/start` | Inicia el bot y muestra bienvenida | `/start` |
| `/help` | Lista todos los comandos disponibles | `/help` |
| `/fecha` | Muestra fecha y hora actual | `/fecha` |
| `/clima [ciudad]` | Información meteorológica | `/clima San Salvador` |

**Estructura de archivos:**
   ```
   telegram_bot/
   ├── .env                 # Variables secretas
   ├── .gitignore          # Ignorar archivos sensibles
   ├── bot.py              # Archivo principal
   ├── config.py           # Configuraciones
   ├── handlers/           # Carpeta para manejadores
   │   ├── __init__.py
   │   ├── commands.py     # Comandos del bot
   │   └── messages.py     # Manejo de mensajes
   ├── utils/              # Utilidades
   │   ├── __init__.py
   │   └── gemini_client.py # Cliente de Gemini
   |   └── tools.py         # Tools personalizadas
   ├── requirements.txt    # Lista de dependencias
   └── README.md          # Documentación
   ```
