from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agents.travel_agent import agent, structured_model
from src.utils.logger import get_logger
import logfire

logger = get_logger(__name__)


class TravelPlanner:
    def __init__(self):
        self.messages = []
        logger.info("Travel Planner initialized")

    @logfire.instrument("create_itinerary")
    def create_itinerary(
        self,
        city: str,
        days: int,
        interests: list[str],
        style: str,
        pace: str,
        month: str | None = None
    ):
        try:
            from datetime import datetime
            today = datetime.now().strftime("%Y-%m-%d")

            user_prompt = f"""
            Plan a {days}-day trip to {city}
            
            Current Date: {today}
            Interests: {', '.join(interests)}
            Travel Style: {style}
            Pace: {pace}
            Month: {month or 'Any'}

            Provide a detailed itinerary.
            """

            self.messages.append(HumanMessage(content=user_prompt))

            # Step 1: Run the agent (LangGraph-based stateful graph)
            response = agent.invoke({
                "messages": self.messages
            })

            # The response is the final state dictionary
            full_history = response.get("messages", [])
            # Extract only the NEW messages added during this turn
            new_messages = full_history[len(self.messages):]
            
            # Sync our internal message state
            self.messages = full_history

            # Capture evidence for evaluations from the new messages
            tool_calls = []
            retrieval_context = []
            
            for msg in new_messages:
                # Capture tool calls from AI messages
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_calls.append({
                            "name": tc["name"],
                            "args": tc["args"]
                        })
                        logger.info(f"Agent used tool: {tc['name']} with args: {tc['args']}")
                
                # Capture tool outputs (observations) from Tool messages
                if isinstance(msg, ToolMessage):
                    content = str(msg.content)
                    # 💡 LEAN DATA: Truncate context entries for storage and simpler evaluation
                    if len(content) > 1000:
                        content = content[:1000] + "... [TRUNCATED FOR LEAN STORAGE]"
                    retrieval_context.append(content)

            # Step 2: Use structured model to ensure the output is perfectly formatted
            logger.info("Structuring the agent response into TravelPlan model")
            structured_itinerary = structured_model.invoke(self.messages)

            return {
                "itinerary": structured_itinerary,
                "tool_calls": tool_calls,
                "retrieval_context": retrieval_context
            }

        except Exception as e:
            logger.error(f"Planner error: {e}")
            raise RuntimeError(f"Failed to generate itinerary: {e}") from e
