from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from src.tools.serper_tool import google_serper_search_tool
from src.tools.tavily_tool import tavily_search_tool
from src.utils.logger import get_logger
from src.config.config import GRQQ_API_KEY

logger = get_logger(__name__)

chat_model = init_chat_model(
    model="groq:llama-3.3-70b-versatile", # Specify the Groq LLM model to use
    temperature=0.3, # Temperature (range 0-1) controls the creativity of the responses. Lower values = more deterministic, higher values = increase randomness.
    top_p=0.9, # Top-p (nucleus sampling) controls the diversity of the responses. The model considers only the most probable tokens whose cumulative probability exceeds top_p.
    max_tokens=2048, # Maximum number of tokens in the generated response. Adjust based on your needs and model limits.
)

print("Chat model initialized with Groq LLM.", chat_model)

system_prompt = """
You are an expert, empathetic travel planner assistant.

Rules:
- Always use web search tools to provide accurate, up-to-date information.
- Create a detailed day-wise itinerary 
- Include food recommendations, local attractions, and cultural experiences.
- Cite sources. Do not make up information.

User Inputs:
City, Number of days, Interests, Travel Style, Pace, Month, Accommodation Budget per Day (INR)
"""

agent = create_agent(
    model=chat_model,
    tools=[tavily_search_tool,google_serper_search_tool],
    system_prompt=system_prompt.strip()    # instructions for the agent
)

logger.info("Travel agent created.")
