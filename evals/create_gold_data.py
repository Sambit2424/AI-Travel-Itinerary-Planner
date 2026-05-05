# Generate ground truth with data used in gold_standard_json
# Our LLM itself will generate this ground truth

import json
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

import logfire

logfire.configure()
logfire.instrument_pydantic()

from langchain.chat_models import init_chat_model
from src.utils.tavily_helper import get_tavily_context
from evals.eval_dataset import EVAL_DATASET

GOLD_FILE = "evals/gold_standard.json"

def create_gold_standard():
    """
    Stage 0: Use real-time web search and a high-reasoning model (70B)
    to create the 'Correct Answer' key for our evaluation.
    """
    logfire.info('Initializing Gold Standard Creation')
    print("🪙 Initializing Gold Standard Creation...")
    
    # Use Llama 3.3 70B for expert distillation
    gold_llm = init_chat_model(
        model="groq:llama-3.3-70b-versatile",
        temperature=0.1
    )
    
    gold_standard = {}

    for i, case in enumerate(EVAL_DATASET):
        city = case["inputs"]["city"]
        interests = ", ".join(case["inputs"]["interests"])
        month = case["inputs"]["month"]
        
        logfire.info(f'Researching {city} for {month}')
        print(f"\n🔍 [{i+1}/{len(EVAL_DATASET)}] Researching {city} for {month}...")
        
        # 1. Real-time Web Search using helper
        # We're making the search quite rigid here to reduce randomness
        search_query = f"top attractions, events, and food recommendations for {city} in {month} for interests: {interests}"
        raw_search_results = get_tavily_context(search_query)
        
        # 2. Distill into Gold Standard with enhanced prompt
        prompt = f"""
        You are a world-class travel expert. I have search results about {city} for the month of {month}.
        Interests: {interests}
        
        Search Results:
        {str(raw_search_results)}
        
        Based on these ACTUAL search results, create a 'Gold Standard' reference for this trip.
        Identify:
        1. GROUND TRUTH: A concise summary (200 words) of the 5 absolute must-include attractions/events.
        2. ESSENTIAL SEARCH TOPICS: 3 core topics that MUST be searched to plan this trip (e.g. 'Mumbai ticket availability').
        3. IDEAL SEARCH QUERIES: 3 specific, high-intent queries a professional agent would use.
        
        FORMAT YOUR RESPONSE AS VALID JSON ONLY:
        {{
            "ground_truth": "...",
            "essential_topics": ["topic1", "topic2", "topic3"],
            "expected_queries": ["query1", "query2", "query3"]
        }}
        """
        
        try:
            response = gold_llm.invoke(prompt)
            clean_content = response.content
            
            # Robust JSON extraction
            start_index = clean_content.find('{')
            end_index = clean_content.rfind('}')
            if start_index != -1 and end_index != -1:
                clean_content = clean_content[start_index:end_index + 1]
            
            distilled_data = json.loads(clean_content)
            
            gold_standard[city] = {
                "input": case["inputs"],
                "ground_truth": distilled_data.get("ground_truth", "N/A"),
                "essential_topics": distilled_data.get("essential_topics", []),
                "expected_queries": distilled_data.get("expected_queries", []),
                "raw_context": str(raw_search_results)[:1500] #Restricting the raw search results to first 1500 characters only
            }
            logfire.info(f'Gold Data generated for {city}')
            print(f"✨ Gold Data generated for {city}.")
            
            # Throttle to respect Groq Free Tier
            time.sleep(15)
            
        except Exception as e:
            logfire.error(f'Error distilling data for {city}: {str(e)}')
            print(f"❌ Error distilling data for {city}: {str(e)}")
            continue

    # Save to JSON
    with open(GOLD_FILE, "w", encoding="utf-8") as f:
        json.dump(gold_standard, f, indent=2)

    logfire.info(f'Gold Standard successfully saved to {GOLD_FILE}')
    print(f"\n🏆 Gold Standard successfully saved to {GOLD_FILE}")

if __name__ == "__main__":
    create_gold_standard()
