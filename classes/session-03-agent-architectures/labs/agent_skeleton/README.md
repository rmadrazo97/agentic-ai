# Agent Skeleton Lab 🤖

Build your first working ReAct agent with LangChain + Claude!

## 🎯 Lab Objective

Create an agent that can answer complex questions by:
1. **Searching** the web for information
2. **Calculating** mathematical expressions  
3. **Reasoning** through multi-step problems

**Target Question**: *"What is the square root of the population of Berlin?"*

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install langchain langchain-anthropic duckduckgo-search
```

### 2. Set API Key
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```
Get your key from: https://console.anthropic.com

### 3. Test Basic Setup
```bash
python driver.py "Hello, who are you?"
```

## 📋 Lab Tasks

### ✅ Task 1: Verify Setup (2 min)
```bash
# Should introduce Claude as an AI assistant
python driver.py "Hello, who are you?"
```

### ✅ Task 2: Test Individual Tools (3 min)
```bash
# Test calculator
python driver.py "What is 25 + 17?"

# Test web search
python driver.py "Who won the 2022 World Cup?"

# Test square root
python driver.py "What is the square root of 100?"
```

### ✅ Task 3: The Main Challenge (10 min)
```bash
# This should trigger: web search → calculation → final answer
python driver.py "What is the square root of the population of Berlin?"
```

**Expected ReAct Trace:**
```
Thought: I need to find Berlin's population first
Action: web_search
Action Input: Berlin population 2024
Observation: Berlin has approximately 3.7 million residents...

Thought: Now I need to calculate the square root of 3,700,000
Action: calculator  
Action Input: sqrt(3700000)
Observation: √3700000.0 = 1924.50

Thought: I now know the final answer
Final Answer: The square root of Berlin's population is approximately 1,924.
```

### ✅ Task 4: Custom Tool Design (5 min)
In `tools.py`, add a TODO comment describing what custom tool your team needs:

```python
# TODO: For our [EdTech/FinTech/DevOps/etc.] agent, we need a tool that:
# - Purpose: [What specific task it accomplishes]
# - Input: [What parameters it needs]
# - Output: [What it returns]
# - Implementation: [What API/library we'll use]
```

### ✅ Task 5: Create Run Log (5 min)
Create `RUN_LOG.md` with output from your successful runs:

```markdown
# Agent Run Log

## Test 1: Basic Math
Command: `python driver.py "What is 25 + 17?"`
Output: [paste console output here]

## Test 2: Web Search  
Command: `python driver.py "Who won the 2022 World Cup?"`
Output: [paste console output here]

## Test 3: Complex Query
Command: `python driver.py "What is the square root of the population of Berlin?"`
Output: [paste console output here]
```

## 📁 File Structure

```
agent_skeleton/
├── driver.py          # 👈 Main entry point (you run this)
├── agent_core.py      # ReAct agent setup (provided)
├── tools.py           # Tool definitions (you extend this)
├── memory.py          # Memory store (optional for now)
└── README.md          # This file
```

## 🔧 Understanding the Code

### `driver.py`
- Main entry point for running queries
- Handles command-line arguments
- TODO: Add cost tracking and memory integration

### `agent_core.py`  
- LangChain + Claude integration
- ReAct prompt template
- Safety limits (max iterations, timeouts)

### `tools.py`
- Web search using DuckDuckGo (no API key needed)
- Math calculator with sqrt support
- TODO: Add your custom tool ideas

### `memory.py`
- Simple JSON-based conversation storage
- Will be used in later sessions for context

## 🚨 Troubleshooting

### ❌ "ImportError: No module named 'langchain_anthropic'"
```bash
pip install langchain langchain-anthropic duckduckgo-search
```

### ❌ "AuthenticationError: Invalid API key"
```bash
# Check your key is set correctly
echo $ANTHROPIC_API_KEY

# Make sure it starts with sk-ant-
export ANTHROPIC_API_KEY="sk-ant-your-actual-key"
```

### ❌ Agent loops infinitely
- The agent might get stuck in thinking loops
- Check that your tools return clear, concise outputs
- Try simpler questions first

### ❌ "Connection error" or search fails
- DuckDuckGo search might be rate-limited
- Try again in a few seconds
- Check your internet connection

### ❌ Math tool errors
- Make sure to use clear expressions: "sqrt(100)" not "√100"
- Stick to basic operations: +, -, *, /, sqrt

## 💡 Tips for Success

### 🎯 Good Questions to Try
```bash
python driver.py "What is 15 * 23?"
python driver.py "What is the capital of France?"  
python driver.py "What is the square root of 144?"
python driver.py "What is the population of Tokyo?"
python driver.py "What is 10% of the population of New York?"
```

### 🛡️ Cost Management
- Use Claude 3 Haiku (default) - much cheaper than Opus
- Keep questions focused and specific
- Agent stops automatically after 10 iterations

### 📊 Understanding ReAct Output
```
Thought: [Agent's reasoning about what to do next]
Action: [Which tool to use: web_search, calculator, current_date]  
Action Input: [Input to give the tool]
Observation: [Tool's response]
```

This cycle repeats until the agent has enough information to give a Final Answer.

## 🎯 Success Criteria

- [ ] Agent responds to basic questions
- [ ] Console shows clear "Thought:" and "Action:" traces  
- [ ] Successfully answers the Berlin population question
- [ ] Custom tool idea documented in tools.py
- [ ] RUN_LOG.md created with example outputs

## 📚 What's Next?

In future sessions, you'll extend this agent with:
- **Session 4**: Memory and conversation context
- **Session 5**: Custom tool development
- **Session 6**: Multi-agent collaboration
- **Session 7**: Voice and multimodal capabilities

This skeleton is your foundation for the entire semester!

---

**Need help?** Ask in #lab-help Slack channel or raise your hand during class.