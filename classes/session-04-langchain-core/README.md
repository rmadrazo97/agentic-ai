# Session 4: LangChain Core - Tools, Chains, Callbacks & Memory 🔧

**Duration**: 80 minutes | **Time**: 8:30 - 9:50

---

## 🎯 Session Goals
- Transform from one-off demos to production-grade LangChain foundation
- Master clean tool interfaces and composable chains
- Implement rich callbacks for monitoring and cost tracking
- Build scalable memory systems for conversational state
- Ship an agent with 3+ heterogeneous tools and persistent memory

---

## ⏱️ Session Timeline

### 1. Stand-up #3 (10 min)

#### 📊 Sprint Update + Tool Demo
**Format**: Progress update + quick demo of custom tool ideas

```markdown
Team [Name] Update:
✅ Completed: [What you finished from agent skeleton lab]
🎯 Today's Goal: [Production agent with tools + memory]
🚧 Blockers: [Any technical issues]
🛠️ Tool Demo: [30-second demo of custom tool idea]
```

**Show your custom tool concepts from tools.py TODO comments!**

---

### 2. Micro-Lecture 1: "What is a Tool?" (10 min)

#### 🔧 Tool Fundamentals

##### **Core Signature**
```python
# Every tool is fundamentally:
Callable[str → str] + name + description

# Example:
def my_tool(input_text: str) -> str:
    return process(input_text)

Tool.from_function(
    name="my_tool",
    description="Clear description for LLM to understand when to use this",
    func=my_tool
)
```

##### **Tool Categories**

| Category | Purpose | Examples |
|----------|---------|----------|
| **🔍 Search** | Information retrieval | Web search, document lookup |
| **💻 Compute** | Data processing | Python REPL, calculators |
| **📊 Data I/O** | File operations | CSV writer, database queries |
| **📢 Comm** | Communication | Email, Slack, notifications |
| **🌐 APIs** | External services | REST calls, cloud services |

##### **Best Practices**
```python
# ✅ Good Tool Design
def search_web(query: str) -> str:
    """Search the web for current information about the query."""
    # Idempotent - same input, same output
    # Stateless - no side effects
    # Fast - completes in <10 seconds
    return search_results

# ❌ Poor Tool Design  
def complex_workflow(params: str) -> str:
    """Does lots of things depending on mood."""
    # Non-descriptive
    # Complex logic
    # Unpredictable timing
```

#### 🛠️ Tool Safety
```python
# For Shell/Python tools - use whitelists
ALLOWED_COMMANDS = ["git status", "pytest", "ls", "pwd"]

def safe_shell_tool(command: str) -> str:
    if command not in ALLOWED_COMMANDS:
        return "Error: Command not allowed"
    return subprocess.run(command, capture_output=True, text=True).stdout
```

---

### 3. Micro-Lecture 2: Chains & Engines (15 min)

#### ⛓️ Chain Types & Composition

##### **LangChain Chain Hierarchy**
```
Simple Chain:     Prompt → LLM → Output
Sequential Chain: Step1 → Step2 → Step3 → Output
Router Chain:     Input → Route → Specialist → Output
Agent Executor:   Goal → Think → Act → Observe → Repeat
```

##### **Code Examples**
```python
# 1. Simple LLM Chain
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

chain = LLMChain(
    llm=ChatAnthropic(model="claude-3-haiku-20240307"),
    prompt=PromptTemplate.from_template("Summarize: {text}")
)

# 2. Sequential Chain - Multi-step workflow
from langchain.chains import SequentialChain

workflow = SequentialChain(
    chains=[extract_chain, process_chain, format_chain],
    input_variables=["raw_data"],
    output_variables=["final_report"]
)

# 3. Router Chain - Delegate to specialists
from langchain.chains.router import MultiPromptChain

router = MultiPromptChain(
    router_chain=router_chain,
    destination_chains={
        "math": math_chain,
        "writing": writing_chain, 
        "coding": coding_chain
    },
    default_chain=general_chain
)
```

##### **Synchronous vs Streaming**
```python
# Synchronous - wait for complete response
result = chain.run("What is AI?")

# Streaming - process tokens as they arrive
for chunk in chain.stream("What is AI?"):
    print(chunk, end="")
```

#### ⚡ Live Demo Time!
```bash
cd demos/
python demo_chain_flow.py
```

---

### 4. Micro-Lecture 3: Callbacks (10 min)

#### 📊 Callback System

##### **Event Taxonomy**
```python
# Key callback events:
on_chat_model_start(messages)    # Before LLM call
on_chat_model_end(response)      # After LLM call
on_tool_start(tool, input)       # Before tool execution
on_tool_end(output)              # After tool execution
on_chain_start(inputs)           # Chain begins
on_chain_end(outputs)            # Chain completes
on_llm_error(error)              # Error handling
```

##### **Built-in Callbacks**
```python
from langchain.callbacks import (
    StdOutCallbackHandler,        # Print to console
    TracingV2CallbackHandler,     # LangSmith tracing
    WandbCallbackHandler,         # Weights & Biases logging
)

# Usage
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[
        StdOutCallbackHandler(),
        TracingV2CallbackHandler()
    ]
)
```

##### **Custom Callback Example**
```python
class CostLatencyCallback(BaseCallbackHandler):
    def __init__(self):
        self.start_time = None
        self.token_count = 0
        
    def on_chain_start(self, serialized, inputs, **kwargs):
        self.start_time = time.time()
        
    def on_chat_model_end(self, response, **kwargs):
        # Track token usage for cost calculation
        self.token_count += len(response.content) // 4
        
    def on_chain_end(self, outputs, **kwargs):
        runtime = time.time() - self.start_time
        cost = self.token_count * 0.25 / 1_000_000  # Haiku pricing
        
        # Log metrics
        with open("metrics.json", "a") as f:
            json.dump({
                "timestamp": time.time(),
                "runtime_seconds": runtime,
                "tokens": self.token_count,
                "estimated_cost": cost
            }, f)
            f.write("\n")
```

#### 🔗 Integrations
- **OpenTelemetry**: Distributed tracing
- **Weights & Biases**: ML experiment tracking  
- **LangSmith**: LangChain-native monitoring
- **Custom dashboards**: Real-time agent metrics

---

### 5. Micro-Lecture 4: Context & Memory (10 min)

#### 🧠 Why Memory Matters

##### **The Problem**
```python
# Without memory - every conversation is isolated
User: "My name is Alice"
Agent: "Nice to meet you!"

User: "What's my name?"  
Agent: "I don't know your name"  # 😞
```

##### **With Memory**
```python
# With memory - maintains context
User: "My name is Alice"
Agent: "Nice to meet you, Alice!"

User: "What's my name?"
Agent: "Your name is Alice"  # 😊
```

#### 🗃️ Memory Types

| Type | How It Works | Best For | Cost |
|------|--------------|----------|------|
| **Buffer** | Stores raw conversation | Short chats | High |
| **Summary** | Compresses old messages | Long conversations | Medium |
| **Window** | Keeps last N messages | Recent context | Low |
| **Vector** | Semantic similarity search | Large knowledge base | Variable |

##### **Memory Strategy Selection**
```python
# Conversation length × Cost budget = Memory choice

if conversation_length < 10 and budget > 0.10:
    memory = ConversationBufferMemory()       # Raw storage
    
elif conversation_length < 50:
    memory = ConversationSummaryBufferMemory( # Hybrid approach
        max_token_limit=4000
    )
    
elif conversation_length < 100:
    memory = ConversationSummaryMemory()      # Compressed storage
    
else:
    memory = VectorStoreRetrieverMemory()     # Semantic search
```

##### **Persistence Options**
```python
# In-memory (development)
memory = ConversationBufferMemory()

# Redis (production)
from langchain.memory import RedisChatMessageHistory
memory = ConversationBufferMemory(
    chat_memory=RedisChatMessageHistory(session_id="user_123")
)

# PostgreSQL (enterprise)
from langchain.memory import PostgresChatMessageHistory
memory = ConversationBufferMemory(
    chat_memory=PostgresChatMessageHistory(session_id="user_123")
)
```

---

### 6. Guided Lab: "Swiss-Army Agent" (20 min)

#### 🎯 Lab Objective
Build a production-grade agent that can:
1. **Search** the web for information
2. **Process** data with Python
3. **Store** results in files
4. **Remember** conversation context
5. **Track** costs and performance

#### 🧰 Tool Selection Menu

**Pick at least 3 tools from different categories:**

| Category | Tool | Use Case |
|----------|------|----------|
| **🔍 Search** | TavilySearchResults | Fast web snippets |
| **💻 Compute** | PythonREPLTool | Data processing |
| **📊 Data I/O** | CSVWriterTool | Save structured data |
| **📢 Comm** | EmailTool | Send notifications |
| **🌐 APIs** | HTTPRequestTool | REST API calls |
| **☁️ Cloud** | S3FileTool | Cloud storage |
| **📱 DB** | SQLDatabaseTool | Database queries |

#### 🚀 Lab Setup
```bash
# Navigate to lab
cd classes/session-04-langchain-core/labs/agent_swiss_army

# Install dependencies
pip install langchain langchain-anthropic tavily-python pandas

# Set API keys
export ANTHROPIC_API_KEY="sk-ant-your-key"
export TAVILY_API_KEY="tvly-your-key"  # Get from tavily.com

# Test basic setup
python driver.py --help
```

#### 📋 Lab Tasks

##### **Task 1**: Tool Integration (8 min)
```bash
# Test individual tools
python -c "from tools import ALL_TOOLS; print([t.name for t in ALL_TOOLS])"

# Expected output: ['web_search', 'python_repl', 'csv_writer', ...]
```

##### **Task 2**: Chain Composition (6 min)
```bash
# Test the full chain
python driver.py "Search for the top 3 programming languages in 2024"
```

##### **Task 3**: Memory Integration (4 min)
```bash
# Test conversation memory
python driver.py "My name is [YourName]"
python driver.py "What's my name?"  # Should remember
```

##### **Task 4**: The Big Challenge (2 min)
```bash
# Test the composite workflow
python driver.py "Email me the 3 latest Python jobs, make a summary table, and store it as CSV"
```

**Expected Flow:**
1. **Search**: "latest Python jobs 2024"
2. **Process**: Extract and format data
3. **Store**: Save as CSV file
4. **Remember**: Context for follow-up

#### 🔧 Lab Files Structure
```
agent_swiss_army/
├── driver.py              # 👈 Main entry point
├── tools/
│   ├── __init__.py        # Tool registry
│   ├── search.py          # Web search tool
│   ├── compute.py         # Python REPL tool
│   ├── csv_writer.py      # File I/O tool
│   └── email.py           # Communication tool
├── chains.py              # Chain composition
├── memory.py              # Memory management
├── callbacks.py           # Cost/latency tracking
├── metrics.json           # Generated metrics log
└── README.md              # Lab instructions
```

---

### 7. Wrap-up & Next Steps (5 min)

#### ✅ Before You Leave
- [ ] Agent uses at least 3 different tool categories
- [ ] Conversation memory working (remembers name)
- [ ] metrics.json file generated with cost data
- [ ] Successfully completes the composite workflow
- [ ] Committed to branch `lab-swiss-army`

#### 📚 Homework (Due Session 5)

1. **Read**: [LangChain Memory Documentation](https://python.langchain.com/docs/modules/memory/)
2. **Read**: [LangChain Callbacks Guide](https://python.langchain.com/docs/modules/callbacks/)
3. **Prepare**: Demo of your custom domain-specific tool
4. **Complete**: Lab deliverable (see below)

#### 🎯 Lab Deliverable

**Push to branch `lab-swiss-army`:**

1. **Working `driver.py`** that completes the composite workflow
2. **`metrics.json`** with at least 1 run showing tokens and runtime
3. **`TOOLS.md`** listing each tool with category and use case

**CI Pass Criteria:**
- ✅ Agent invokes at least 3 distinct tools
- ✅ Callback logs cost and latency data
- ✅ Total runtime < 20 seconds
- ✅ Memory persists across conversation turns

---

## 🏗️ Key Concepts Summary

### Tool Abstraction
```python
# Treat every capability as a pure function with clear interface
Tool.from_function(
    name="descriptive_name",
    description="Clear explanation of what this tool does",
    func=stateless_function
)
```

### Chain Composition  
```python
# Break complex jobs into reusable components
chain = SequentialChain([
    preprocess_chain,
    agent_executor,
    postprocess_chain
])
```

### Callback Monitoring
```python
# Tap into execution lifecycle without polluting business logic
agent = AgentExecutor(
    callbacks=[CostTracker(), LatencyMonitor(), ErrorLogger()]
)
```

### Memory Strategy
```python
# Choose based on conversation length and cost budget
if long_conversation:
    memory = ConversationSummaryBufferMemory(max_token_limit=4000)
else:
    memory = ConversationBufferMemory()
```

---

## 🚀 Performance & Cost Tips

### 1. Streaming Responses
```python
# Start processing before complete response
llm = ChatAnthropic(model="claude-3-haiku-20240307", streaming=True)
```

### 2. Router Chains
```python
# Use cheap models for simple tasks, upgrade for complex reasoning
router = create_router_chain({
    "simple": ChatAnthropic(model="claude-3-haiku-20240307"),    # $0.25/M
    "complex": ChatAnthropic(model="claude-3-sonnet-20240229")   # $3.00/M
})
```

### 3. Memory Optimization
```python
# Bounded memory prevents cost explosion
memory = ConversationSummaryBufferMemory(
    max_token_limit=4000,  # When reached, summarize old messages
    return_messages=True
)
```

### 4. Retry Logic
```python
# Handle rate limits gracefully
from langchain.callbacks import RetryCallbackHandler

executor = AgentExecutor(
    callbacks=[RetryCallbackHandler(max_retries=3, backoff_factor=2)]
)
```

---

## 🚨 Troubleshooting Guide

### ❌ "Tool not found" errors
```python
# Check tool registration
from tools import ALL_TOOLS
print([tool.name for tool in ALL_TOOLS])
```

### ❌ Memory not persisting
```python
# Verify memory is attached to agent
agent = AgentExecutor(
    agent=react_agent,
    tools=tools,
    memory=memory,  # ← Make sure this is included
    verbose=True
)
```

### ❌ High costs
```python
# Use token limits and cheap models
memory = ConversationSummaryBufferMemory(max_token_limit=2000)
llm = ChatAnthropic(model="claude-3-haiku-20240307")  # Cheapest option
```

### ❌ Slow performance
```python
# Enable streaming and set timeouts
llm = ChatAnthropic(streaming=True, timeout=30)
executor = AgentExecutor(max_execution_time=60)
```

---

*Next Session: Custom Tool Development & Domain-Specific Integrations*