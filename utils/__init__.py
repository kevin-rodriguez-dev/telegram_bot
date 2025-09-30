"""
Módulo de utilidades del bot
Contiene el cliente de Gemini y las herramientas personalizadas
"""

from .gemini_client import crear_agente_conversacional, generar_respuesta
from .tools import ClimaAPI, FechaHoraAPI, MultiAgent

__all__ = [
    'crear_agente_conversacional',
    'generar_respuesta',
    'ClimaAPI',
    'FechaHoraAPI',
    'MultiAgent'
]