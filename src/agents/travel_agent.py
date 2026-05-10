import logfire
import time
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from src.tools.serper_tool import google_serper_search_tool
from src.tools.tavily_tool import tavily_search_tool
from src.schema.travel_models import TravelPlan
from src.utils.logger import get_logger

# Ensure Pydantic models are captured by logfire for observability
logfire.instrument_pydantic()

# For internal logging, it can be removed since logfire is in place now
logger = get_logger(__name__)

# Primary Reasoning Model (High Stability 70B model for tool calling)
chat_model = init_chat_model(
    model="groq:llama-3.3-70b-versatile", # Specify the Groq LLM model to use
    temperature=0.3, # Temperature (range 0-1) controls the creativity of the responses. Lower values = more deterministic, higher values = increase randomness.
    top_p=0.9, # Top-p (nucleus sampling) controls the diversity of the responses. The model considers only the most probable tokens whose cumulative probability adds upto 90%.
    max_retries=3
)

print("Chat model initialized with Groq LLM.", chat_model)

tools=[tavily_search_tool,google_serper_search_tool]

# Custom Middleware for LangChain v1.x (Observability & Rate Limiting)
class TravelAgentMiddleware(AgentMiddleware):
    def before_agent(self, state, runtime):
        logger.info(f"🎬 Agent Turn Started (History: {len(state.get('messages', []))} msgs)")
        return None
    
    def after_model(self, state, runtime):
        # 🛡️ TPM PROTECTION: Pause slightly after every model reasoning step
        # This prevents the LLM from blasting multiple tool calls in 1 second
        logger.info("⏳ Catching breath (2s) for TPM refill...")
        time.sleep(2)
        return None
    
    def after_agent(self, state, runtime):
        logger.info("🏁 Agent Turn Completed. Cooling down (5s)...")
        time.sleep(5)
        return None

SYSTEM_PROMPT = """
You are an expert, empathetic travel planner.

Rules:
1. Always use web search tools to get latest info, events, and pricing as of current date.
2. Include food suggestions, local tips, and travel advice.
""".strip()

# Modern LangChain 1.x Agent with Built-in Loop (via LangGraph)
agent = create_agent(
    model=chat_model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,# instructions for the agent
    middleware=[TravelAgentMiddleware()]
)

# Model wrapper for structured output validation
structured_model = chat_model.with_structured_output(TravelPlan)

logger.info("Modern LangChain v1.x Travel Agent with Middleware initialization.")
