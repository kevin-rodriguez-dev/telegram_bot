import logging
import requests
from datetime import datetime
from typing import List
from langchain.tools import Tool
from config import WEATHER_API_KEY, WEATHER_BASE_URL

logger = logging.getLogger(__name__)


class ClimaAPI:
    """Herramienta para consultar el clima usando OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_BASE_URL
    
    def obtener_clima(self, ciudad: str) -> str:
        """
        Obtiene información del clima para una ciudad específica
        
        Args:
            ciudad: Nombre de la ciudad
            
        Returns:
            Información formateada del clima
        """
        try:
            params = {
                "q": ciudad,
                "key": self.api_key,
                "lang": "es"
            }
            
            response = requests.get(f"{self.base_url}/current.json", params=params, timeout=10)
            
            if response.status_code == 404:
                return f" No se encontró información para la ciudad: {ciudad}"
            
            response.raise_for_status()
            data = response.json()
            
            # Extraer información
            # temp = data["temp"]
            # feels_like = data["feels_like"]
            # temp_min = data["temp_min"]
            # temp_max = data["temp_max"]
            # humidity = data["humidity"]
            # description = data["weather"][0]["description"].capitalize()
            
            # # Formatear respuesta
            # resultado = (
            #     f"🌤 *Clima en {ciudad.title()}*\n\n"
            #     f"🌡 Temperatura: {temp}°C\n"
            #     f"🤔 Sensación térmica: {feels_like}°C\n"
            #     f"📊 Min/Max: {temp_min}°C / {temp_max}°C\n"
            #     f"💧 Humedad: {humidity}%\n"
            #     f"☁️ Condición: {description}"
            # )
            
            # return resultado

            location = data["location"]
            current = data["current"]
            clima_info = f"""
            Clima en {location['name']}, {location["country"]}
            Temperatura: {current["temp_c"]}°C (se siente como {current["feelslike_c"]}°C)
            Condicion: {current["condition"]["text"]}
            Viento: {current["wind_kph"]} km/h
            Humedad: {current["humidity"]}%
            Visibilidad: {current["vis_km"]} km
            Ultima actualizacion: {current["last_updated"]}
            """.strip()
            return clima_info
            
        except requests.exceptions.Timeout:
            return " La solicitud tardó demasiado. Intenta de nuevo."
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en API del clima: {str(e)}")
            return f" Error al consultar el clima: {str(e)}"
        except KeyError as e:
            logger.error(f"Error al procesar respuesta del clima: {str(e)}")
            return " Error al procesar los datos del clima"


class FechaHoraAPI:
    """Herramienta para obtener fecha y hora actual"""
    
    @staticmethod
    def obtener_fecha_hora() -> str:
        """
        Obtiene la fecha y hora actual en español
        
        Returns:
            Fecha y hora formateada
        """
        try:
            current_date = datetime.now()
            
            dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
            meses = [
                "enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
            ]
            
            dia_semana = dias[current_date.weekday()]
            mes = meses[current_date.month - 1]
            
            return (
                f" {dia_semana.capitalize()}, {current_date.day} de {mes} de {current_date.year} "
                f"a las {current_date.strftime('%H:%M:%S')}"
            )
            
        except Exception as e:
            logger.error(f"Error al obtener fecha/hora: {str(e)}")
            return f" Error al obtener fecha/hora: {str(e)}"


class MultiAgent:
    """Clase que agrupa todas las herramientas disponibles para el agente"""
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.fecha_hora_api = FechaHoraAPI()
    
    def langchain(self) -> List[Tool]:
        """
        Convierte las herramientas al formato de LangChain Tools
        
        Returns:
            Lista de herramientas en formato LangChain
        """
        tools = [
            Tool(
                name="consultar_clima",
                func=self.clima_api.obtener_clima,
                description=(
                    "Útil para obtener información del clima actual de una ciudad. "
                    "Proporciona temperatura, humedad y condiciones meteorológicas. "
                    "Input: nombre de la ciudad (ej: 'San Salvador', 'Madrid', 'Tokyo')"
                )
            ),
            Tool(
                name="obtener_fecha_hora",
                func=self.fecha_hora_api.obtener_fecha_hora,
                description=(
                    "Útil para obtener la fecha y hora actual. "
                    "No requiere ningún parámetro de entrada. "
                    "Devuelve la fecha completa en español con día, mes, año y hora."
                )
            )
        ]
        
        logger.info(f" {len(tools)} herramientas configuradas para LangChain")
        return tools