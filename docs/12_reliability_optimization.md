# 08 - Reliability Optimization: Solving the Token Limit

In a production environment, you don't just solve for "accuracy"—you solve for **API Limits**. During development, we hit a "Token Wall" on Groq's free tier. Here is how we engineered the solution.

### 1. The Challenge (The "413/429" Problem)
- **TPM (Tokens Per Minute)**: Limit of 12,000. Large search results from Tavily were pushing each request to 20,000+, causing immediate 413 Payload Too Large errors.
- **TPD (Tokens Per Day)**: Limit of 100,000. Without optimization, running just 4 cities would exhaust the entire daily quota.
- **Context Accumulation**: A major bug where history from City A (Paris) was being sent in the request for City B (Tokyo), causing token usage to grow exponentially.

---

### 2. The Solution: "The Great Token Refactor"

We implemented four key reliability layers to ensure the system never crashes:

#### A. Smart Truncation
In `src/utils/tavily_helper.py`, we now intercept search results and cap them at **800 characters** each. 
- **Impact**: Reduced input token size by ~70% without losing planning quality.

#### B. Context Isolation
In `tests/generate_trips.py`, we now instantiate a **fresh `TravelPlanner`** inside the loop for every city. 
- **Impact**: Fixed the accumulation bug. Every city starts with a clean 0-token history.

#### C. Mandatory Throttling (The "Breath" Pause)
We added `AgentMiddleware` that forces the AI to wait **2-5 seconds** after every single tool call.
- **Impact**: Prevents "bursting" through the 12k TPM limit during complex reasoning loops.

#### D. The "Decoupled Judge" Architecture
We use a **separate Groq API Key** and a separate model name (`JUDGE_GROQ_API_KEY`) for the evaluation judge.
- **Impact**: Prevents the Agent's tokens from interfering with the Judge's quota, ensuring you can always run a report even if the agent is busy.

---

### 3. Cost-Efficiency vs. Intelligence
| Model | Role | Trade-off |
| :--- | :--- | :--- |
| **70B (Versatile)** | Expert Judge | **High Intelligence**. Used for scoring because it follows JSON instructions perfectly. |
| **8B (Instant)** | Budget Judge | **High Speed**. Can be used for testing, but it is a "weaker judge" and may throw JSON format errors. |

### Summary
By engineering for the limits of our infrastructure, we turned a "failing" script into a **Resilient Production Pipeline**.

---
*This documentation is part of the Project Reliability Suite.*
