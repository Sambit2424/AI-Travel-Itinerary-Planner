# 09 - The Expert Research: Creating the "Correct Answer"

To know if our AI is doing a good job, we first need to know what a "Perfect Answer" looks like. We call this the **Gold Standard**.

### 1. The Goal
Before we let the AI Agent try to plan a trip, we use a separate process to gather the best possible real-world information. This creates a "Key" that we use to grade the agent later.

### 2. The Logic (How it works)
We use a script called `tests/create_gold_data.py`. It follows three simple steps:

1.  **Real-Time Search**: It uses the **Tavily Search API** to find current events, weather, and food for a specific city.
2.  **Expert Distillation**: It sends all those raw search results to a very powerful AI model (**Llama 3.3 70B**). 
3.  **Fact Extraction**: The powerful AI summarizes the search results into:
    *   **Ground Truth**: A summary of what *actually* exists in that city right now.
    *   **Ideal Queries**: What questions a human travel expert would ask to get the best results.

### 3. Why do we do this?
Imagine a teacher grading a test. If the teacher doesn't have the answer key, they are just guessing. By creating the **Gold Standard** first, we give our system the "Answer Key."

---
*This documentation is part of the Project Reliability Suite.*
