import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

GRQQ_API_KEY = os.getenv("GRQQ_API_KEY")
JUDGE_GROQ_API_KEY = os.getenv("JUDGE_GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
LOGFIRE_TOKEN = os.getenv("LOGFIRE_TOKEN")

logger.info("Configuration loaded successfully.")
