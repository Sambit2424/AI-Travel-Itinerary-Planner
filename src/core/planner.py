from langchain_core.messages import HumanMessage,AIMessage
from src.utils.logger import get_logger
from src.utils.custom_exception import DetailedException
from src.agents.travel_agent import agent
from pydantic import BaseModel,ConfigDict, Field
from typing import Optional, List, Union
from datetime import datetime


logger = get_logger(__name__)

# Defining schema for the travel planner agent using Pydantic BaseModel
class Travelplanner(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    messages: List[Union[HumanMessage, AIMessage]] = Field(default_factory=list, description="List of messages exchanged between the user and the agent.")
    city: str = Field(..., description="The city for which the travel itinerary is to be planned.")
    days: int = Field(..., ge=1, description="Number of days for the travel plan.")
    interests: Optional[List[str]] = Field(None, description="User's interests to tailor the itinerary.")
    style: Optional[str] = Field(None, description="User's travel style (e.g., budget, luxury, adventure).")
    pace: Optional[str] = Field("moderate", description="User's preferred pace of travel (e.g., relaxed, moderate, fast).")
    month: Optional[str] = Field(None, description="Month of travel to consider seasonal factors.")
    accom_rate_per_day_inr: Optional[float] = Field(None, ge=500, description="User's budget per day for the accommodation.")

    logger.info("TravelPlanner initialized.")
    

def plan_trip(data: Travelplanner) -> str:
    """Yields streamed chunks from the LLM."""
    try:
        user_prompt = f"""
        Plan a {data.days}-day trip to {data.city}.
        Interests: {', '.join(data.interests)}
        Travel Style: {data.style}
        Pace: {data.pace}
        Budget: {data.accom_rate_per_day_inr}
        Month: {data.month or 'Any'}.
        """

        # Update message history
        data.messages.append(HumanMessage(content=user_prompt))

        # Invoke agent
        response = agent.invoke({"messages": data.messages})

        final_answer = response["messages"][-1].content if response["messages"] else "No response from agent."
        data.messages.append(AIMessage(content=final_answer))

        return final_answer
    
    except Exception as e:
        logger.error(f"Error in planning trip: {str(e)}")
        raise DetailedException(f"Failed to plan trip: {str(e)}")


        

