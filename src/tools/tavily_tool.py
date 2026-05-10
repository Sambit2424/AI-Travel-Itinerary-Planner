from src.utils.tavily_helper import get_tavily_context
from src.utils.logger import get_logger
from langchain_core.tools import tool

logger = get_logger(__name__)

@tool
def tavily_search_tool(query:str) -> str:
    """
    Search the web using Tavily to get up-to-date travel information,
    attractions, activities, tips, and local insights for a given query.
    """
    logger.info(f"Tavily Search Tool called with query: {query}")
    # Use centralized helper with standardized parameters
    results = get_tavily_context(query, max_results=5)
    return results

logger.info("Tavily tool is ready.")