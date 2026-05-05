import json
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
import logfire

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Configure Logfire Observability
logfire.configure()
logfire.instrument_pydantic()

from src.core.planner import TravelPlanner
from evals.eval_dataset import EVAL_DATASET

OUTPUT_FILE = "results/generated_trips.json"

def generate_trips():
    os.makedirs("results", exist_ok=True)
    results = []
    print("🚀 Starting Production Trip Generation Pipeline...")
    
    with logfire.span("Generation Stage: Processing Dataset"):
        for i, case in enumerate(EVAL_DATASET):
            inputs = case["inputs"]
            city = inputs["city"]

            # 🛠️ BUG FIX: Instantiate a FRESH planner for every city to avoid context accumulation
            # This prevents Paris trips from leaking into Tokyo research and blowing up tokens!
            planner = TravelPlanner()

            # Nested span for detailed tracing per city
            with logfire.span(f"Generating for {city}", **inputs):
                print(f"\n🌍 [{i+1}/{len(EVAL_DATASET)}] Creating itinerary for {city}...")

                try:
                    result = planner.create_itinerary(
                        city=city,
                        days=inputs["days"],
                        interests=inputs["interests"],
                        style=inputs["style"],
                        pace=inputs["pace"],
                        month=inputs["month"],
                    )

                    trip_data = {
                        "input": inputs,
                        "itinerary": result["itinerary"].model_dump(),
                        "retrieval_context": result["retrieval_context"],
                        "tool_calls": result["tool_calls"],
                        "generated_at": datetime.now().isoformat(),
                    }

                    results.append(trip_data)
                    print(f"✅ Success. Waiting 45s to allow TPD/TPM buckets to refill...")
                    time.sleep(45)
                    
                except Exception as e:
                    logfire.error(f"Generation failed for {city}", error=str(e))
                    print(f"❌ Failed for {city}: {str(e)}")
                    continue

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n✨ Generation Complete. Results saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_trips()