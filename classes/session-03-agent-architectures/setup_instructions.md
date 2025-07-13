# Session 3 Setup Instructions 🤖

Get ready to build your first working AI agent with LangChain + Claude!

## Prerequisites

- Python 3.8+ installed
- Anthropic API key (required)
- Basic familiarity with command line

## Step 1: Install Dependencies

```bash
# Navigate to session directory
cd classes/session-03-agent-architectures/labs/agent_skeleton

# Install required packages
pip install langchain langchain-anthropic duckduckgo-search
```

**Package Details:**
- `langchain` - Agent framework
- `langchain-anthropic` - Claude integration
- `duckduckgo-search` - Web search (no API key needed)

## Step 2: Get Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up for an account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

**💰 Cost Estimate:** This lab should cost < $0.05 total using Claude Haiku

## Step 3: Set Environment Variable

### On macOS/Linux:
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# To make it permanent, add to your shell profile:
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### On Windows:
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# For permanent setting, use System Environment Variables
```

## Step 4: Test Your Setup

```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Test basic agent functionality
python driver.py "Hello, who are you?"
```

**Expected Output:**
```
🤖 Processing: Hello, who are you?
============================================================

> Entering new AgentExecutor chain...
I don't need any tools to answer this question. I can respond directly.

I'm Claude, an AI assistant created by Anthropic. I'm running as an agent with access to web search, calculator, and current date tools. How can I help you today?

> Finished chain.

🎯 FINAL ANSWER:
I'm Claude, an AI assistant created by Anthropic...
⏱️  Runtime: 2.34 seconds
```

## Step 5: Quick Functionality Test

```bash
# Test math capability
python driver.py "What is 25 + 17?"

# Test web search
python driver.py "Who won the 2022 World Cup?"

# Test the main challenge
python driver.py "What is the square root of the population of Berlin?"
```

## Troubleshooting

### ❌ "ImportError: No module named 'langchain'"
```bash
pip install --upgrade pip
pip install langchain langchain-anthropic duckduckgo-search
```

### ❌ "AuthenticationError: Invalid API key"
```bash
# Check your key is set correctly
echo $ANTHROPIC_API_KEY

# Make sure it starts with sk-ant-
export ANTHROPIC_API_KEY="sk-ant-your-actual-key"

# Restart your terminal after setting the variable
```

### ❌ "Connection error" or search fails
- DuckDuckGo might be rate-limiting
- Check your internet connection
- Try again in a few seconds

### ❌ Agent loops infinitely
- Use Ctrl+C to stop
- Try simpler questions first
- Check that tools return clear outputs

### ❌ "No module named 'agent_core'"
```bash
# Make sure you're in the right directory
cd classes/session-03-agent-architectures/labs/agent_skeleton
python driver.py "test"
```

## Optional: Run Architecture Demos

After basic setup works, try the architecture demos:

```bash
cd ../demos

# ReAct pattern demo
python demo_react.py "What's the square root of Tokyo's population?"

# Plan-Act-Reflect demo
python demo_plan_act_reflect.py "Calculate average population of top 3 European cities"

# Auto-GPT style demo (WARNING: more expensive)
python demo_autogpt_loop.py "Research AI agent trends"
```

## File Structure Verification

Your lab directory should look like this:

```
agent_skeleton/
├── driver.py          # ✅ Main entry point
├── agent_core.py      # ✅ ReAct agent setup
├── tools.py           # ✅ Tool definitions
├── memory.py          # ✅ Memory store
└── README.md          # ✅ Lab instructions
```

## API Rate Limits & Costs

### Anthropic Limits (as of 2024)
- **Free tier**: Limited requests per day
- **Paid tier**: Higher limits, pay-per-use
- **Claude Haiku**: ~$0.25 per 1M input tokens

### Cost Management Tips
```bash
# Use cheapest model (already default)
export ANTHROPIC_MODEL="claude-3-haiku-20240307"

# Monitor usage in Anthropic console
# Set billing alerts if concerned
```

## Getting Help

### During Class
- Raise your hand or ask in chat
- Work with your team members
- Share screens for debugging

### Outside Class
- **Slack**: #lab-help channel
- **GitHub**: Open issue on course repo
- **Office Hours**: Check course schedule

### Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Agent gives weird responses | Check tool descriptions are clear |
| Math calculations fail | Use exact syntax: "sqrt(100)" not "√100" |
| Search returns no results | Try rephrasing the search query |
| High costs | Stick to Claude Haiku, avoid long conversations |

## Pre-Class Checklist

- [ ] Python packages installed
- [ ] API key obtained and set
- [ ] Basic test runs successfully
- [ ] Can see "Thought:" and "Action:" in output
- [ ] Ready to extend with custom tools

## What You'll Learn Today

1. **ReAct Pattern** - How agents think and act
2. **LangChain Integration** - Production-ready agent framework
3. **Tool Design** - Creating capabilities for your agent
4. **Architecture Patterns** - When to use different approaches
5. **Foundation** - Base agent you'll build on all semester

---

**You're ready! 🚀 See you in Session 3!**