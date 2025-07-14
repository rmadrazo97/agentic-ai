# Swiss Army Agent Lab 🔧

Build a production-grade LangChain agent with comprehensive tools, memory, and monitoring capabilities.

## 🎯 Lab Objective

Create a multi-tool agent that can:
- **Search** the web for information
- **Process** data with Python computations  
- **Store** results in structured formats (CSV)
- **Communicate** via email notifications (mock)
- **Remember** conversation context across sessions
- **Track** costs and performance metrics

**Target Challenge**: *"Email me the 3 latest Python jobs, make a summary table, and store it as CSV."*

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd classes/session-04-langchain-core/labs/agent_swiss_army

pip install langchain langchain-anthropic tavily-python pandas requests
```

### 2. Set API Keys
```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Optional (for enhanced web search)
export TAVILY_API_KEY="tvly-your-key-here"  # Get from tavily.com

# Optional (for persistent memory)
export REDIS_URL="redis://localhost:6379"
```

### 3. Test Basic Setup
```bash
python driver.py --help
python driver.py "Hello, who are you?"
```

## 📋 Lab Tasks

### ✅ Task 1: Tool Integration Test (5 min)
```bash
# Test individual tool categories
python driver.py "What is 25 * 17?"                    # Compute tool
python driver.py "Search for latest AI news"           # Search tool  
python driver.py "Create CSV with sample data"         # Data I/O tool
```

### ✅ Task 2: Memory Integration Test (5 min)
```bash
# Test conversation memory
python driver.py "My name is Alice and I work at Tech Corp"
python driver.py "What's my name and where do I work?"
```

### ✅ Task 3: Chain Composition Test (5 min)
```bash
# Test multi-step workflow
python driver.py "Search for Python programming trends, then summarize the top 3 trends"
```

### ✅ Task 4: The Swiss Army Challenge (5 min)
```bash
# The ultimate test - multi-tool workflow
python driver.py "Email me the 3 latest Python jobs, make a summary table, and store it as CSV"
```

**Expected Flow:**
1. **Search** for "latest Python developer jobs 2024"
2. **Process** the results to extract top 3 opportunities
3. **Create** a structured summary table
4. **Store** the data as CSV file
5. **Send** email notification (mock)
6. **Remember** the task for follow-up questions

### ✅ Task 5: Interactive Mode (Optional)
```bash
# Try interactive conversation mode
python driver.py --interactive

# Available commands in interactive mode:
# help     - Show commands
# stats    - Show session statistics  
# tools    - Show available tools
# clear    - Clear memory
# quit     - Exit
```

## 🏗️ Architecture Overview

```
📁 agent_swiss_army/
├── driver.py              # Main entry point with CLI interface
├── chains.py               # Chain composition and routing logic
├── memory.py               # Conversation memory with multiple strategies
├── callbacks.py            # Cost tracking and performance monitoring
├── tools/                  # Tool implementations
│   ├── __init__.py        # Tool registry
│   ├── search.py          # Web search (Tavily/DuckDuckGo)
│   ├── compute.py         # Python REPL and math calculations
│   ├── csv_writer.py      # CSV file operations
│   ├── email.py           # Email sending (mock implementation)
│   └── http_tool.py       # HTTP API requests
└── outputs/               # Generated files (CSV, emails, metrics)
    ├── memory/            # Conversation history
    ├── email_outbox/      # Mock email storage
    └── metrics.json       # Cost and performance logs
```

## 🔧 Key Features

### Tool Categories
| Category | Tools | Use Cases |
|----------|-------|-----------|
| **🔍 Search** | Tavily, DuckDuckGo | Web search, fact lookup |
| **💻 Compute** | Python REPL, Calculator | Data processing, math |
| **📊 Data I/O** | CSV Writer | Structured data storage |
| **📢 Communication** | Email Sender | Notifications, reports |
| **🌐 APIs** | HTTP Client | External service integration |

### Memory Strategies
- **Buffer**: Raw conversation storage (small chats)
- **Summary**: Compressed memory (long conversations)  
- **Window**: Last N messages (recent context)
- **Summary Buffer**: Hybrid approach (default)

### Chain Composition
```python
# Pre-processing → Agent Execution → Post-processing
chain = SequentialChain([
    preprocess_step,
    agent_executor,
    postprocess_step
])
```

### Callback Monitoring
- **Cost Tracking**: Token usage and estimated costs
- **Performance**: Latency and throughput metrics
- **Tool Usage**: Statistics per tool category
- **Error Handling**: Graceful failure recovery

## 🎛️ Usage Examples

### Command Line Interface
```bash
# Single query
python driver.py "Calculate compound interest on $1000 at 5% for 10 years"

# Interactive mode
python driver.py --interactive

# Test suite
python driver.py --test

# With intelligent routing
python driver.py --router "Analyze market trends and create detailed report"

# Quiet mode
python driver.py --quiet "What's 2+2?"
```

### Python API
```python
from chains import swiss_army_chain

# Create agent
agent = swiss_army_chain()

# Run query
result = agent.run("Search for AI news and summarize")
print(result['output'])

# Check costs
cost_info = agent.get_cost_summary()
print(f"Cost: ${cost_info['total_cost']:.4f}")
```

## 📊 Monitoring & Metrics

### Real-time Monitoring
```bash
# View session statistics
python driver.py --interactive
> stats

# Generated metrics files
cat outputs/metrics.json         # Detailed event log
cat outputs/final_metrics.json   # Session summary
```

### Cost Tracking
The agent automatically tracks:
- **Token usage** per LLM call
- **Estimated costs** by model (Claude Haiku: ~$0.25/M tokens)
- **Tool execution time** and frequency
- **Error rates** and types

### Memory Usage
```bash
# Memory snapshots saved automatically
ls outputs/memory/
cat outputs/memory/chat_history_default.json
```

## 🚨 Troubleshooting

### ❌ "API key not found"
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
export ANTHROPIC_API_KEY="sk-ant-your-actual-key"
```

### ❌ "Tool not working"
```bash
# Check tool availability
python -c "from tools import ALL_TOOLS; print([t.name for t in ALL_TOOLS])"

# Test individual tools
python tools/search.py
python tools/compute.py
```

### ❌ "Memory not persisting"
```bash
# Check memory files
ls outputs/memory/

# Clear and restart
python driver.py --interactive
> clear
```

### ❌ "High costs"
```bash
# Check cost tracking
python driver.py --interactive  
> stats

# Use cheaper model (edit chains.py)
model_name = "claude-3-haiku-20240307"  # Cheapest option
```

## 📚 Advanced Features

### Custom Tool Development
Add your own tools in `tools/` directory:

```python
# tools/my_custom_tool.py
from langchain.tools import Tool

def my_function(input_str: str) -> str:
    return f"Processed: {input_str}"

def create_my_tool() -> Tool:
    return Tool.from_function(
        name="my_tool",
        description="Description for the LLM",
        func=my_function
    )

# Add to tools/__init__.py
from .my_custom_tool import create_my_tool
# tools.append(create_my_tool())
```

### Memory Strategies
```python
# Different memory configurations
from memory import build_memory

# For short conversations
memory = build_memory(strategy="buffer")

# For long conversations  
memory = build_memory(strategy="summary")

# For cost-conscious usage
memory = build_memory(strategy="window")
```

### Chain Customization
```python
# Create specialized chains
from chains import create_fast_chain, create_powerful_chain

# Fast/cheap for simple tasks
fast_agent = create_fast_chain()

# Powerful for complex analysis  
smart_agent = create_powerful_chain()
```

## 🎯 Success Criteria

- [ ] Agent uses at least 3 different tool categories
- [ ] Conversation memory works across multiple exchanges
- [ ] `metrics.json` file generated with cost and timing data
- [ ] Successfully completes the Swiss Army Challenge workflow
- [ ] Interactive mode responds to all special commands

## 📦 Deliverable Requirements

**Create these files for submission:**

1. **Working `driver.py`** - Completes the target challenge end-to-end
2. **`metrics.json`** - Contains at least one complete run with cost/timing data
3. **`TOOLS.md`** - Lists each tool with category and use case description

**CI Pass Criteria:**
- ✅ Agent invokes minimum 3 distinct tools in target challenge
- ✅ Metrics file contains valid cost and latency data
- ✅ Total runtime under 20 seconds for basic queries
- ✅ Memory persists across conversation turns

---

**Need help?** Use `python driver.py --help` or ask in #lab-help Slack channel!