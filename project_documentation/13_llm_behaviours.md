# 13 - LLM Behaviours: Understanding the "AI Personality"

AI models aren't like traditional software; they have "personalities" and quirks. Understanding these behaviors is key to building a reliable system. Here are the most important ones we encountered.

---

### 1. The "Chatty" Behavior (Token Wastage)
**What it is**: Sometimes, the AI starts explaining its thinking in too much detail or adds polite "chatter" (e.g., "Certainly! I'd be happy to help you with that trip...").
*   **The Problem**: Every extra word costs **Tokens**. If the AI is too chatty, it will hit your **TPM Rate Limit** without finishing the actual task.
*   **Simple Analogy**: That one friend who tells a 10-minute story just to answer "Yes" or "No."

### 2. Hallucinations (Confidently Lying)
**What it is**: When an AI doesn't know an answer, it often doesn't say "I don't know." Instead, it creates a very believable but completely fake answer.
*   **Direct Impact**: In our project, an AI might invent a "Monday Night Jazz Festival" that doesn't exist. This is why we created the **Faithfulness Metric** to cross-check everything against real search results.
*   **Simple Analogy**: A tour guide who is lost but too embarrassed to admit it, so they start making up names for the buildings you pass.

### 3. Instruction Fragility (The "Goldfish" Memory)
**What it is**: LLMs have a limit on how much they can "focus" on. If your prompt is too long or has too many search results, the AI might "forget" its core instructions (like "Format as JSON only").
*   **Our Fix**: This is why we **Truncated** our search results. By keeping the context small, the AI stays focused on the rules.
*   **Simple Analogy**: If you give someone 1,000 instructions at once, they will likely forget the first five.

### 4. JSON Fragility (Small Model Struggles)
**What it is**: Modern applications need the AI to speak in **JSON** (a specific code format). Smaller models (like 8B) often make "typos" in this format, breaking the whole app.
*   **The Problem**: A single missing comma can crash the system.
*   **Our Fix**: We use the powerful **70B model** as our Judge because it is much more disciplined at following formatting rules.
*   **Simple Analogy**: Trying to get a toddler to fill out a complicated tax form versus hiring a professional accountant.

---

### Summary: Why we build guardrails
We don't "tame" the AI; we build **Guardrails**. Everything we built—from the Throttling to the Truncation—is designed to manage these natural behaviors so the end user gets a perfect experience.

---
*This documentation is part of the Project Reliability Suite.*
