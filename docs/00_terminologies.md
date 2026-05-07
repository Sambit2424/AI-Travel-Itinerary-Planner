# 00 - The Project Glossary: Big Words Made Simple

To understand this project, you need to know a few "Big Words." Here is a list of everything we use, explained with simple analogies so anyone can understand!

---

### 1. The API Limits (The Token Arcade)

| Term | Definition | Simple Analogy |
| :--- | :--- | :--- |
| **Token** | A tiny piece of text (roughly 4 characters). APIs use these to measure work. | Think of these as "Arcade Tokens." Every question you ask the AI costs tokens. |
| **TPM** | **Tokens Per Minute**. The limit of how many tokens you can spend in 1 minute. | Imagine a vending machine that only lets you buy 10 snacks per minute. If you try to buy 11, it locks you out. |
| **TPD** | **Tokens Per Day**. Your total daily budget of work. | Your daily allowance. Once your "allowance" is gone, you have to wait until tomorrow (or until it resets). |
| **Rate Limit** | A hard stop when you try to do too much at once. | Like a "Speed Limit" on the highway. If you go too fast (too many requests), you get stopped. |

---

### 2. The Architecture (The Building Blocks)

| Term | Definition | Simple Analogy |
| :--- | :--- | :--- |
| **Middleware** | A layer of code that sits between the User and the AI to add extra logic. | A security guard at a door who checks your ID before letting you in and gives you a receipt when you leave. |
| **Throttling** | Manually slowing down the code using pauses (`time.sleep`). | Taking a deep breath between sentences so you don't run out of air while talking. |
| **Decoupling** | Breaking a big, tangled process into separate, smaller steps. | Instead of cooking a whole dinner in one pot, you use separate pans for the rice, the curry, and the veggies. |
| **Pydantic** | A tool that forces the AI to follow a strict format (JSON). | A **Cookie Cutter**. No matter how the dough looks, the cookie always comes out in the exact same shape. |

---

### 3. The Evaluation (The Grading Jury)

| Term | Definition | Simple Analogy |
| :--- | :--- | :--- |
| **Gold Standard** | The "Correct Answer" researched by an expert before the test starts. | The **Teacher's Answer Key**. Without it, the teacher can't grade the students fairly. |
| **Ground Truth** | The actual facts (weather, prices, open hours) found in the real world. | A **Map**. It doesn't matter what you "think" the road looks like; the map shows the truth. |
| **Faithfulness** | A score checking if the AI told the truth or invented facts (hallucinations). | A **Fact-Checker** for a newspaper who verifies every quote and name before printing. |
| **G-Eval** | Using a very powerful AI (a Judge) to grade the work of a smaller AI (the Agent). | A **Senior Professor** grading a college student's final paper. |
| **DeepEval** | The framework we use to run our "Jury" and calculate our reliability scores. | The **Olympics Scoring System**. It provides the rules and the tools to decide who wins. |

---

### 4. Observability (The X-Ray Vision)

| Term | Definition | Simple Analogy |
| :--- | :--- | :--- |
| **Logfire** | A dashboard where we can see every "hidden" thought the AI has. | **X-Ray Vision**. It lets us see "inside the AI's head" to see exactly where it got confused. |
| **Trace** | A step-by-step history of one specific trip calculation. | A **Breadcrumb Trail**. It shows exactly which path the AI took to get to the final answer. |

---
*This glossary is designed to help everyone—from beginners to experts—understand the magic behind our Reliability Suite.*
