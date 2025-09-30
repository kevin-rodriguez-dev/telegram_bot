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

            location = data["location"]
            current = data["current"]
            
            clima_info = f"""
            Clima actual en {location['name']}, {location['region']}, {location['country']}
            Hora local: {location['localtime']}

            Temperatura: {current['temp_c']}°C
            Sensación térmica: {current['feelslike_c']}°C
            Condición: {current['condition']['text']}
            Viento: {current['wind_kph']} km/h, dirección {current['wind_dir']}
            Humedad: {current['humidity']}%
            Presión atmosférica: {current['pressure_mb']} hPa
            Visibilidad: {current['vis_km']} km
            Índice UV: {current['uv']}

            Última actualización: {current['last_updated']}
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
    
    def obtener_fecha_hora(self, _: str = "") -> str:
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

class BusquedaWeb:
    """Herramienta para buscar información en la web usando DuckDuckGo"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
        }
    
    def buscar_web(self, consulta:str, cantidad:int = 3) -> str:
        try:
            params = {
                "q": consulta,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }

            response = requests.get(
                self.base_url, params=params, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            resultados_texto = f"Resultados de busqueda para '{consulta}':\n\n"

            if data.get("Answer"):
                resultados_texto += f"Respuesta directa: {data['Answer']}\n\n"
            
            if data.get("AbstractText"):
                resultados_texto += f"Resumen: {data['AbstractText']}\n\n"
                if data.get("AbstractSource"):
                    resultados_texto += f"Fuente: {data['AbstractSource']}\n\n"

            if data.get("RelatedTopics"):
                resultados_texto += "Temas relacionados:\n\n"
                for i, tema in enumerate(data["RelatedTopics"][:cantidad], 1):
                    if isinstance(tema, dict) and tema.get("Text"):
                        texto = tema["Text"][:200] + "..." if len(tema["Text"]) > 200 else tema["Text"]
                        resultados_texto += f"{i}. {texto}\n\n"
                resultados_texto += "\n"
            
            if data.get("Definition"):
                resultados_texto += f"Definicion: {data['Definition']}\n\n"
                if data.get("DefinitionSource"):
                    resultados_texto += f"Fuente: {data['DefinitionSource']}\n\n"
            
            if not any([data.get("Answer"), data.get("AbstractText"), data.get("RelatedTopics"), data.get("Definition")]):
                return self._busqueda_alternativa(consulta)

            return resultados_texto.strip()

        except Exception as e:
            return f"Error al buscar en la web: {str(e)}"
    
    def _busqueda_alternativa(self, consulta:str) -> str:
        try:
            url = "https://duckduckgo.com/html/"
            params = {
                "q": consulta
            }

            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                content = response.text

                import re
                titles = re.findall(r'<a[^>]*class="result__a"[^>]*>([^<]+)</a>', content)

                if titles:
                    resultado = f"Resultados de busqueda para '{consulta}':\n\n"
                    for i, title in enumerate(titles[:3], 1):
                        resultado += f"{i}. {title}\n\n"
                    
                    return resultado.strip()

            return f"Busqueda realizada para '{consulta}'. No se encontraron resultados."
                

        except Exception as e:
            return f"Error al buscar en la web: {str(e)}"

class MultiAgent:
    """Clase que agrupa todas las herramientas disponibles para el agente"""
    
    def __init__(self):
        self.clima_api = ClimaAPI()
        self.fecha_hora_api = FechaHoraAPI()
        self.busqueda_web = BusquedaWeb()
    
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
            ),
            Tool(
                name="buscar_en_web",
                func=self.busqueda_web.buscar_web,
                description=(
                    "Útil para buscar información en la web."
                    "Input: término o pregunta de búsqueda (ej: 'Que es Machine learning?')"
                )
            )
        ]
        
        logger.info(f" {len(tools)} herramientas configuradas para LangChain")
        return tools