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

# Configure Logfire
logfire.configure()
logfire.instrument_pydantic()

from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    GEval
)
from deepeval.test_case import LLMTestCaseParams
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain.chat_models import init_chat_model

from src.config.config import JUDGE_GROQ_API_KEY

INPUT_FILE = "results/generated_trips.json"
GOLD_FILE = "tests/gold_standard.json"
REPORT_PATH = "results/evaluation_report.md"


class LangChainDeepEvalWrapper(DeepEvalBaseLLM):

    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        # Robust extractor for JSON from LLM chatter
        res = self.model.invoke(prompt).content
        if "```json" in res:
            res = res.split("```json")[1].split("```")[0].strip()
        return res

    async def a_generate(self, prompt: str) -> str:
        res = await self.model.ainvoke(prompt)
        content = res.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        return content

    def get_model_name(self) -> str:
        return getattr(self.model, "model_name", "LangChain Model")


# Initialize the Expert Judge
# We use 70B Versatile for high-quality, stable metric evaluations
judge_llm = init_chat_model(
    model="groq:llama-3.3-70b-versatile",
    api_key=JUDGE_GROQ_API_KEY,
    temperature=0,
    max_retries=3
)
judge_model = LangChainDeepEvalWrapper(judge_llm)

def throttle():
    print("⏳ Waiting 45s for Groq refill...")
    time.sleep(45)


def evaluate_trips():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found. Run generate_trips.py first!")
        return

    # Load Gold Data (Ground Truth) if it exists
    gold_data = {}
    if os.path.exists(GOLD_FILE):
        with open(GOLD_FILE, "r") as f:
            gold_data = json.load(f)
            print("🏆 Verified Gold Standard data loaded.")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Global metrics base
    base_metrics = [
        AnswerRelevancyMetric(threshold=0.7, model=judge_model),
        FaithfulnessMetric(threshold=0.7, model=judge_model),
    ]

    all_results = []

    print("\n🎯 Starting Expert Evaluation Suite...")
    with logfire.span("Evaluation Stage: Assessing Itinerary Quality"):
        for i, trip in enumerate(data):
            city = trip["input"]["city"]
            print(f"\n📊 [{i+1}/{len(data)}] Assessing {city}...")

            # Extract Gold components for this specific city
            gold_entry = gold_data.get(city, {})
            ground_truth = gold_entry.get("ground_truth", "N/A (Reference-less)")
            expected_queries = gold_entry.get("expected_queries", [])
            essential_topics = gold_entry.get("essential_topics", [])

            # Dynamic Search Relevancy Metric for this specific case
            search_relevancy_metric = GEval(
                name="Search Relevancy",
                criteria=f"Judge if the agent's search queries for {city} were relevant and comprehensive. "
                         f"Essential topics to cover: {', '.join(essential_topics)}. "
                         f"Example ideal queries: {', '.join(expected_queries)}.",
                evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.TOOLS_CALLED],
                model=judge_model,
                threshold=0.7
            )

            current_metrics = base_metrics + [search_relevancy_metric]

            with logfire.span(f"Evaluating {city}", city=city):
                test_case = LLMTestCase(
                    input=str(trip["input"]),
                    actual_output=json.dumps(trip["itinerary"]), 
                    ground_truth=ground_truth,
                    retrieval_context=[str(c)[:1000] for c in trip["retrieval_context"]],
                    tools_called=[
                        ToolCall(name=tc["name"], input_parameters=tc["args"])
                        for tc in trip["tool_calls"]
                    ],
                )

                case_metrics = []
                for metric in current_metrics:
                    name = metric.__class__.__name__ if not isinstance(metric, GEval) else metric.name
                    
                    with logfire.span(f"Metric: {name}"):
                        try:
                            print(f"  🔍 Measuring {name}...")
                            metric.measure(test_case)
                            case_metrics.append({
                                "name": name,
                                "score": metric.score,
                                "success": metric.score >= metric.threshold,
                                "reason": getattr(metric, 'reason', 'N/A')
                            })
                            print(f"  ✅ Score: {metric.score:.2f}")
                        except Exception as e:
                            logfire.error(f"Metric {name} failed", error=str(e))
                            print(f"  ⚠️ Failed: {str(e)}")
                        
                        # Short sleep between metrics to avoid sub-second rate limits
                        time.sleep(2)

                all_results.append({
                    "city": city,
                    "input": trip["input"],
                    "metrics": case_metrics,
                    "success": all(m["success"] for m in case_metrics)
                })
                
                # Full throttle only between test cases (cities) to respect TPM
                if i < len(data) - 1:
                    throttle()

    # --- GENERATE PREMIUM DASHBOARD REPORT ---
    print(f"\n✨ Writing Executive Dashboard to {REPORT_PATH}...")
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(f"# 📊 AI Travel Planner - Quality Dashboard\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  \n")
        f.write(f"**Architecture**: Two-Stage Decoupled Evaluation  \n")
        f.write(f"**Judge Model**: Llama-3.3-70B-Versatile\n\n")

        # Summary Table
        f.write("## 📈 Global Overview\n\n")
        f.write("| Case | City | Avg Score | Status | Primary Conflict |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")

        for i, res in enumerate(all_results):
            avg = sum(m["score"] for m in res["metrics"]) / len(res["metrics"]) if res["metrics"] else 0
            status = "🟢 PASS" if res["success"] else "🔴 FAIL"
            # Get the reason from the first failing metric, or the first metric overall
            issue = "None"
            for m in res["metrics"]:
                if not m["success"]:
                    issue = m["reason"].split(".")[0] # Short summary
                    break
            
            f.write(f"| {i+1} | **{res['city']}** | {avg:.2f} | {status} | {issue} |\n")

        # Deep Dive Sections
        f.write("\n\n## 🔍 Deep Dive Analysis\n")
        for res in all_results:
            f.write(f"\n### Trip: {res['city']}\n")
            f.write(f"**Input Parameters**: `{res['input']}`\n\n")
            f.write("| Metric | Score | Justification |\n")
            f.write("| :--- | :--- | :--- |\n")
            for m in res["metrics"]:
                indicator = "✅" if m["success"] else "⚠️"
                f.write(f"| {m['name']} | {indicator} {m['score']:.2f} | {m['reason']} |\n")
            f.write("\n---\n")

    print(f"\n🏆 Evaluation Complete. View Report: {REPORT_PATH}")


if __name__ == "__main__":
    evaluate_trips()