# 10 - The Agent Generation: Running the Planner

Once we have our "Answer Key," it's time to let the AI Travel Agent try to plan the trips. We use a script called `tests/generate_trips.py`.

### 1. The Goal
We want to see how the Agent performs on 4 different cities (Paris, Tokyo, Mumbai, and Kerala). Each city is a unique test.

### 2. The Logic (The Loop)
The script works like this:

1.  **Fresh Start**: For every city, we create a brand new version of the Agent. We don't want it to remember Paris while it's planning Tokyo!
2.  **The Reasoning**: The Agent "thinks" about the trip, uses its search tools, and builds a plan.
3.  **The "Safety Throttle"**: Because the API is very fast, it can accidentally send too much data at once. We added a **mandatory 45-second pause** between every city to give the system time to rest.
4.  **Recording Evidence**: We save the final itinerary *and* all the search results the agent found into a file called `results/generated_trips.json`.

### 3. Why do we do this?
By running all our test cases at once and saving them, we can analyze the agent's performance calmly and carefully in the next stage.

---
*This documentation is part of the Project Reliability Suite.*
