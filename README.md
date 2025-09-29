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

4. **Configura las API Keys**:
   
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```env
   TELEGRAM_BOT_TOKEN=
   GEMINI_API_KEY=
   ```
