import logging
from config import GEMINI_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from utils.tools import MultiAgent

logger = logging.getLogger(__name__)

# Crear el cliente Gemini usando LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

def generar_respuesta(mensaje_usuario: str) -> str:
    """
    Genera una respuesta simple usando Gemini sin herramientas
    
    Args:
        mensaje_usuario: El mensaje del usuario
        
    Returns:
        La respuesta generada por Gemini
    """
    try:
        response = llm.invoke([HumanMessage(content=mensaje_usuario)])
        return response.content
    except Exception as e:
        logger.error(f"Error al generar respuesta: {str(e)}")
        return f" Error al generar respuesta: {str(e)}"


def crear_agente_conversacional():
    """
    Crea un agente LangChain con todas las herramientas personalizadas.
    El agente decide automáticamente cuándo usar cada herramienta.
    
    Returns:
        Agente LangChain configurado con memoria y herramientas
    """
    try:
        # Crear memoria conversacional
        memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        
        # Obtener herramientas de MultiAgent
        multi_agent = MultiAgent()
        tools = multi_agent.langchain()
        
        logger.info(f" Herramientas cargadas: {[tool.name for tool in tools]}")
        
        # Crear agente conversacional
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=4
        )
        
        logger.info(" Agente conversacional creado exitosamente")
        return agent
        
    except Exception as e:
        logger.error(f" Error al crear agente conversacional: {str(e)}")
        raise