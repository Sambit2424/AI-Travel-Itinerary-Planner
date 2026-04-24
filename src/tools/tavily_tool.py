from langchain_tavily import TavilySearch
from src.config.config import TAVILY_API_KEY
from src.utils.logger import get_logger
from langchain_core.tools import tool

logger = get_logger(__name__)

@tool
def tavily_search_tool(query:str) -> str:
    """
    Search the web using Tavily to get the most relevant and up-to-date information
    for travel-related queries.
    """
    tavily_search = TavilySearch(
        tavily_api_key=TAVILY_API_KEY,   
        max_results=5, # Maximum number of search results to return
        topic = "general", # Topic for the search
        search_depth = "advanced", # Search depth can be "basic" or "advanced" depending on how thorough you want the search to be
        include_images = False, # Whether to include images in the search results
        include_answer = True, # Whether to include direct answers in the search results
        time_range = "month", # Time range for search results (e.g., "day", "week", "month", "year")
        include_domains = ["tripadvisor.com", "booking.com","airbnb.com","trip.com","agoda.com"], # List of trusted domains to include in the search results
)


    return tavily_search.invoke({ "query": query })

logger.info("Tavily tool is ready.")