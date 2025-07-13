# Session 3: Agent Architectures 101 🏗️

**Duration**: 80 minutes | **Time**: 8:30 - 9:50

---

## 🎯 Session Goals
- Understand 3 seminal agent architectures: ReAct, Plan-Act-Reflect, Auto-GPT
- Build your first working LangChain + Claude agent
- Implement tool-calling with web search and math capabilities
- Create the foundation agent you'll extend all semester

---

## ⏱️ Session Timeline

### 1. Stand-up #2 (10 min)

#### 📊 Sprint Update Format
**Team progress updates & blocker identification**

```markdown
Team [Name] Sprint Update:
✅ Completed: [What you finished since last session]
🎯 Today's Goal: [What you're working on today]
🚧 Blockers: [Any issues preventing progress]
💡 Insights: [What you learned from prompt engineering lab]
```

**Post updates in your team's PR comment thread**

---

### 2. Micro-Lecture 1: Why "Architecture" Matters (5 min)

#### 🧠 From Chat to Action

##### **Traditional LLM**: Text In → Text Out
```python
response = llm.chat("What's 2+2?")
# Output: "The answer is 4"
```

##### **Agent LLM**: Text In → **Actions** → Results
```python
response = agent.run("What's the square root of Berlin's population?")
# Process: Think → Search → Calculate → Answer
# Output: "Berlin has ~3.7M people, so √3,700,000 ≈ 1,924"
```

#### 🔄 Architecture Components

##### **Policy Layer** (LLM Reasoning)
- Decides WHAT to do next
- Interprets observations
- Plans multi-step workflows

##### **Executor Layer** (Tools & Memory)
- Actually DOES the work
- Calls APIs, runs calculations
- Stores and retrieves information

```
┌─────────────────┐
│   LLM Policy    │ ← "I need to search for Berlin population"
│   (Claude)      │
└─────────────────┘
          ↓
┌─────────────────┐
│   Tool Router   │ ← Routes to appropriate tool
└─────────────────┘
          ↓
┌─────────────────┐
│  Search Tool    │ ← Actually performs web search
│  Math Tool      │
│  Memory Store   │
└─────────────────┘
```

---

### 3. Micro-Lecture 2: ReAct Pattern (10 min)

#### 🎭 **Re**asoning + **Act**ing Pattern

##### **Core Loop**: Thought → Action → Observation
```
Thought: I need to find Berlin's population
Action: web_search("Berlin population 2024")
Observation: Berlin has approximately 3.7 million residents

Thought: Now I need to calculate the square root  
Action: calculator("sqrt(3700000)")
Observation: 1924.5

Thought: I have the answer
Final Answer: The square root of Berlin's population is approximately 1,924
```

#### ⚡ Live Demo Time!
```bash
cd demos/
python demo_react.py "What's the square root of Tokyo's population?"
```

##### **LangChain Implementation**
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_react_agent, AgentExecutor

# 1. Create LLM
llm = ChatAnthropic(model="claude-3-haiku-20240307")

# 2. Define tools
tools = [search_tool, math_tool]

# 3. Create ReAct agent
agent = create_react_agent(llm=llm, tools=tools, prompt=react_prompt)

# 4. Execute with verbose logging
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
result = executor.invoke({"input": "Your question here"})
```

#### 🎯 When to Use ReAct
- **✅ Good for**: Simple tool chains, quick Q&A
- **❌ Not ideal for**: Complex multi-step planning, long workflows

---

### 4. Micro-Lecture 3: Plan-Act-Reflect (10 min)

#### 🎯 Three-Role Architecture

##### **1. Planner** - Creates the strategy
```python
def plan(goal):
    return [
        "Step 1: Search for current population data",
        "Step 2: Extract numerical value", 
        "Step 3: Calculate square root",
        "Step 4: Format final answer"
    ]
```

##### **2. Executor** - Carries out the plan
```python
def execute_step(step, tools):
    # Use ReAct pattern for each step
    return tool_result
```

##### **3. Critic** - Reviews and corrects
```python
def reflect(plan, results):
    if has_errors(results):
        return revised_plan
    return "Plan succeeded"
```

#### 🔄 Full Workflow
```
User Question → Planner → [Step1, Step2, Step3] → Executor → Results → Critic
                    ↖                                                      ↙
                      Critic finds error, revises plan and re-executes
```

#### 📊 Pros vs Cons
| Pros ✅ | Cons ❌ |
|---------|---------|
| Global plan visibility | 2-3x more LLM calls = higher cost |
| Reflection catches errors | More complex implementation |
| Better for multi-step tasks | Can over-plan simple questions |

---

### 5. Micro-Lecture 4: Auto-GPT & Task Loops (10 min)

#### 🔄 Perpetual Execution Loop

##### **Auto-GPT Lineage**
```python
while not goal_achieved and iterations < max_iterations:
    # 1. Assess current state
    current_state = memory.get_context()
    
    # 2. Generate next task
    next_task = llm.plan_next_action(goal, current_state)
    
    # 3. Execute task
    result = execute_task(next_task)
    
    # 4. Store in memory
    memory.store(next_task, result)
    
    # 5. Check if goal achieved
    goal_achieved = llm.evaluate_progress(goal, memory.get_context())
```

#### ⚠️ Resource Exhaustion Pitfalls

##### **The Token Death Spiral**
```
Iteration 1: 1K tokens  ($0.0003)
Iteration 2: 2K tokens  ($0.0006) ← context grows
Iteration 3: 4K tokens  ($0.0012)
Iteration 4: 8K tokens  ($0.0024)
...
Iteration 10: 1024K tokens ($0.3072) ← unsustainable!
```

#### 🛡️ Safety Valves

##### **1. Max Iterations**
```python
MAX_ITERATIONS = 10  # Hard limit
```

##### **2. Cost Limits**
```python
if total_cost > 0.50:  # $0.50 limit
    break
```

##### **3. Human-in-the-Loop**
```python
if iterations > 5:
    approval = input("Continue? (y/n): ")
    if approval != 'y':
        break
```

##### **4. Timeout Protection**
```python
import signal
signal.alarm(300)  # 5-minute timeout
```

#### 🎯 When to Use Auto-GPT Style
- **✅ Good for**: Open-ended research, exploration tasks
- **❌ Dangerous for**: Production without guardrails, cost-sensitive apps

---

### 6. Guided Lab: "Skeleton Agent" (25 min)

#### 🛠️ Lab Objective
Build a working ReAct agent that can answer: 
**"What is the square root of the population of Berlin?"**

#### 🚀 Getting Started
```bash
# 1. Navigate to lab
cd classes/session-03-agent-architectures/labs/agent_skeleton

# 2. Install dependencies
pip install langchain langchain-anthropic duckduckgo-search

# 3. Set your API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# 4. Test the skeleton
python driver.py "What is 2 + 2?"
```

#### 📋 Lab Tasks

##### **Task 1**: Basic Setup (5 min)
```bash
# Verify your agent runs
python driver.py "Hello, who are you?"

# Expected: Claude introduces itself as an AI assistant
```

##### **Task 2**: Test Tools (5 min)
```bash
# Test math tool
python driver.py "What is 25 + 17?"

# Test search tool  
python driver.py "Who won the 2022 World Cup?"
```

##### **Task 3**: Complex Query (10 min)
```bash
# The main challenge
python driver.py "What is the square root of the population of Berlin?"

# Expected output:
# Thought: I need to find Berlin's population first
# Action: web_search
# Observation: [population data]
# Thought: Now I need to calculate the square root
# Action: calculator
# Observation: [calculation result]
# Final Answer: [coherent response]
```

##### **Task 4**: Custom Tool Design (5 min)
In `tools.py`, add a TODO comment describing a custom tool your team's project will need:

```python
# TODO: For our [domain] agent, we need a tool that:
# - Purpose: [what it does]
# - Input: [what parameters it takes]  
# - Output: [what it returns]
# - API/Library: [how we'll implement it]
```

#### 🔧 Lab Files Structure
```
agent_skeleton/
├── driver.py          # 👈 Main entry point (you edit this)
├── agent_core.py      # ReAct wrapper (provided)
├── tools.py           # Tool definitions (you extend this)
├── memory.py          # Simple memory store (optional today)
└── README.md          # Setup instructions
```

#### 🎯 Success Criteria
- [ ] Agent responds to basic questions
- [ ] Console shows "Thought:" and "Action:" traces
- [ ] Successfully answers Berlin population question
- [ ] Custom tool idea documented in tools.py

---

### 7. Wrap-up & Next Steps (10 min)

#### ✅ Before You Leave
- [ ] driver.py working with sample queries
- [ ] ReAct trace visible in console output
- [ ] Custom tool idea added to tools.py
- [ ] Committed to branch `lab-agent-skeleton`

#### 📚 Homework (Due Session 4)

1. **Read**: [ReAct Paper (Yao et al., 2023)](https://arxiv.org/abs/2210.03629) - Focus on sections 3-4
2. **Watch**: [LangChain Agent Deep Dive (15min)](https://www.youtube.com/watch?v=MlK6SIjcjE8)
3. **Explore**: [AutoGPT Repository](https://github.com/Significant-Gravitas/AutoGPT) - Read the README
4. **Complete**: Lab deliverable (see below)

#### 🎯 Lab Deliverable

**Push to branch `lab-agent-skeleton`:**

1. **Working `driver.py`** that responds correctly to:
   - "What is 15 * 23?"
   - "What is the capital of France?"
   
2. **`RUN_LOG.md`** with console output showing ReAct trace

3. **Custom tool idea** in `tools.py` TODO comment

**CI Checks:**
- ✅ "Thought:" and "Action:" tokens present in output
- ✅ Exit code 0 for test queries
- ✅ Cost < $0.02 per run (use Claude Haiku!)

---

## 📚 Architecture Comparison Reference

| Pattern | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **ReAct** | Few tools, short chains | ✅ Simple<br>✅ No planning overhead | ❌ Can loop/stall<br>❌ No global view |
| **Plan-Act-Reflect** | Multi-step with branching | ✅ Global plan visible<br>✅ Error correction | ❌ 2-3x LLM calls<br>❌ More complex |
| **Auto-GPT Loop** | Open-ended exploration | ✅ Fully autonomous<br>✅ Handles complexity | ❌ Unbounded cost<br>❌ Needs guardrails |

## 🔧 Claude + LangChain Quick Reference

| Task | Code |
|------|------|
| **Set API Key** | `export ANTHROPIC_API_KEY=sk-ant-...` |
| **Change Model** | `ChatAnthropic(model="claude-3-opus-20240229")` |
| **Cost Tracking** | Use `langchain.callbacks.get_openai_callback()` |
| **Best for ReAct** | Claude 3 Haiku (~$0.25/M tokens) |

## 📖 Additional Resources

### 📄 Papers & Research
- **[ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)** - Original ReAct paper
- **[Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)** - Planning strategies
- **[AutoGPT: An Experimental Open-Source Attempt](https://github.com/Significant-Gravitas/AutoGPT)** - Auto-GPT implementation

### 🎥 Videos & Tutorials
- **[LangChain Agents Explained](https://www.youtube.com/watch?v=MlK6SIjcjE8)** (15 min)
- **[Building ReAct Agents from Scratch](https://www.youtube.com/watch?v=Eug2clsLtFs)** (20 min)
- **[AutoGPT Architecture Breakdown](https://www.youtube.com/watch?v=jn8294ORr-E)** (12 min)

### 📝 Blog Posts & Articles
- **[LangChain Agent Documentation](https://python.langchain.com/docs/modules/agents/)**
- **[ReAct Pattern in Practice](https://blog.langchain.dev/react-agent/)**
- **[Multi-Agent Systems with AutoGen](https://microsoft.github.io/autogen/)**

### 🛠️ Tools & Libraries
- **[LangChain](https://github.com/langchain-ai/langchain)** - Agent framework
- **[AutoGen](https://github.com/microsoft/autogen)** - Multi-agent conversations
- **[CrewAI](https://github.com/joaomdmoura/crewAI)** - Agent orchestration
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Graph-based agents

---

## 🚨 Troubleshooting Guide

### ❌ "ImportError: No module named 'langchain_anthropic'"
```bash
pip install langchain langchain-anthropic
```

### ❌ "AuthenticationError: Invalid API key"
```bash
echo $ANTHROPIC_API_KEY  # Check key is set
export ANTHROPIC_API_KEY="sk-ant-your-actual-key"
```

### ❌ Agent loops infinitely
- Check your tools return clear, concise outputs
- Reduce prompt complexity
- Add iteration limits in agent_core.py

### ❌ "Too expensive" - costs adding up
- Use Claude 3 Haiku instead of Opus
- Shorten tool descriptions
- Add cost tracking and limits

---

*Next Session: Tool Design & Function Calling Deep Dive*