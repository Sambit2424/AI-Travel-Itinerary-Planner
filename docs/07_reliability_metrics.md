# 07 - The Reliability Metrics: Your AI's Report Card

To move past "Vibes-based testing," we use three core metrics to grade every trip the AI generates. These metrics act as a digital "Bar Exam" for your agent.

### 1. Answer Relevancy (The User Check)
- **What it checks**: Does the plan actually meet the user's specific request? (e.g., If I asked for "Luxury" and "Michelin Dining," did you give me that?)
- **Judge logic**: The expert judge checks if the interests, style, and pace indicated in the input are respected in the output activities.

### 2. Faithfulness (The Anti-Hallucination Pack)
- **What it checks**: Is every claim in the itinerary backed by information found in the web search results?
- **Judge logic**: It cross-checks the final answer against the `retrieval_context`. If the AI invents a restaurant that wasn't in the search results, the score drops.

### 3. Search Relevancy (The Research Check)
- **What it checks**: Was the agent's research strategy actually smart enough to find the right data?
- **Judge logic**: This is a dynamic **G-Eval** metric. It doesn't look at the final answer; it looks at the **Queries** and **Tool Calls**. 
- It rewards the agent for searching for specific, real-world data and penalizes it for "guessing" (even if the guess is lucky).

---

### 📊 The Reliability Dashboard
When you run the tests, you get a score for each metric. 
- **Score > 0.7**: Passing. The agent is production-ready for this scenario.
- **Score < 0.7**: Failing. The system provides a **Justification** explaining exactly why the AI made a mistake.

### 💡 Why we removed "Contextual Precision"
We found that generic metrics like "Contextual Precision" were "token hogs"—they consumed 60% of our daily quota just to tell us that search results contain some noise. By focusing on **Search Relevancy**, we judge the agent's *logic*, which is much more efficient and reliable.

---
*This documentation is part of the Project Reliability Suite.*
