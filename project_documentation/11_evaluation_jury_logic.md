# 11 - The Evaluation Jury: Grading the Work

The final step is the most important: **The Report Card**. We use a script called `tests/evaluate_trips.py`.

### 1. The Goal
We compare what the Agent planned (from Stage 2) against what the Expert Research said (from Stage 1).

### 2. The Logic (The Judge)
We use a separate, high-intelligence AI to act as a **Jury**. It looks at three main areas:

1.  **Relevancy**: Did the agent give the user what they actually asked for? If the user asked for "Relaxed," is the plan too "Packed"?
2.  **Faithfulness**: Did the agent tell the truth? If it mentions a restaurant, was that restaurant actually in the search results, or did the AI "hallucinate" (invent) it?
3.  **Search Logic**: Did the agent ask the right questions? We reward the agent for searching for specific, useful information.

### 3. The Result
After the Judge is finished, it creates a file called `results/evaluation_report.md`. This dashboard shows you exactly where the Agent passed and where it failed.

---
*This documentation is part of the Project Reliability Suite.*
