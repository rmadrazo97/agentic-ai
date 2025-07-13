# Model Selection Guide 🎯

Quick reference for choosing the right LLM for your use case.

## Decision Framework

### 1. Context Window Requirements

| Need | Models | Use Cases |
|------|--------|-----------|
| **< 4K tokens** | Any model | Simple Q&A, basic chat |
| **4K - 32K tokens** | GPT-4o-mini, Claude Haiku | Document analysis, code review |
| **32K - 128K tokens** | GPT-4o, Claude 3.5 Sonnet | Long documents, complex reasoning |
| **128K+ tokens** | Claude 3.5 Sonnet, Gemini 2.0 Pro | Research papers, entire codebases |

### 2. Priority Triangle ⚠️ 
**You can only pick 2 of these 3:**

```
      SPEED
     /     \
    /       \
   /         \
 PRICE ---- ACCURACY
```

## Provider Comparison

### OpenAI 🔥
**Best for**: General purpose, fastest ecosystem adoption

| Model | Context | Input Cost* | Output Cost* | Speed | Use Case |
|-------|---------|-------------|--------------|-------|----------|
| GPT-4o | 128K | $2.50 | $10.00 | Medium | Complex reasoning, analysis |
| GPT-4o-mini | 128K | $0.15 | $0.60 | Fast | Most tasks, great value |
| GPT-3.5-turbo | 16K | $0.50 | $1.50 | Very Fast | Simple chat, basic tasks |

**Strengths:**
- ✅ Excellent function calling
- ✅ Fastest ecosystem adoption  
- ✅ Best developer tools
- ✅ Reliable performance

**Weaknesses:**
- ❌ More expensive for high-volume
- ❌ Strict content policies
- ❌ No web browsing

### Anthropic 🧠
**Best for**: Complex reasoning, safety-critical applications

| Model | Context | Input Cost* | Output Cost* | Speed | Use Case |
|-------|---------|-------------|--------------|-------|----------|
| Claude 3.5 Sonnet | 200K | $3.00 | $15.00 | Medium | Advanced reasoning, analysis |
| Claude 3 Haiku | 200K | $0.25 | $1.25 | Fast | Quick tasks, summarization |

**Strengths:**
- ✅ Excellent at following instructions
- ✅ Very large context windows
- ✅ Strong safety guardrails
- ✅ Great for complex reasoning

**Weaknesses:**
- ❌ Limited function calling
- ❌ Smaller ecosystem
- ❌ More conservative outputs

### Google 🌐
**Best for**: Multimodal, massive context, cost efficiency

| Model | Context | Input Cost* | Output Cost* | Speed | Use Case |
|-------|---------|-------------|--------------|-------|----------|
| Gemini 2.0 Flash | 1M | $0.075 | $0.30 | Very Fast | Huge documents, research |
| Gemini 1.5 Pro | 1M | $1.25 | $5.00 | Medium | Complex multimodal tasks |

**Strengths:**
- ✅ Massive context windows (1M tokens!)
- ✅ Very cost effective
- ✅ Excellent multimodal capabilities
- ✅ Fast inference

**Weaknesses:**
- ❌ Less reliable than OpenAI/Anthropic
- ❌ Newer ecosystem
- ❌ Variable quality

*Cost per 1M tokens

## Quick Decision Tree

### For Beginners 🎓
**Start with**: GPT-4o-mini
- Reliable, fast, affordable
- Great documentation
- Large community support

### For Production Apps 🚀
**High accuracy needed**: Claude 3.5 Sonnet
**High volume/cost sensitive**: Gemini 2.0 Flash  
**Balanced**: GPT-4o-mini

### For Specific Use Cases

#### 📄 Document Analysis
- **Short docs (< 32K)**: GPT-4o-mini
- **Long docs (< 200K)**: Claude 3 Haiku
- **Massive docs (< 1M)**: Gemini 2.0 Flash

#### 💬 Chatbots
- **Customer service**: Claude 3 Haiku (safety)
- **Internal tools**: GPT-4o-mini (reliability)
- **High volume**: Gemini 2.0 Flash (cost)

#### 🛠️ Code Generation
- **Simple tasks**: GPT-4o-mini
- **Complex logic**: Claude 3.5 Sonnet
- **Large codebases**: Gemini 2.0 Flash

#### 🎨 Creative Writing
- **Balanced**: GPT-4o
- **Conservative**: Claude 3.5 Sonnet
- **Experimental**: Gemini 1.5 Pro

## Cost Optimization Tips 💰

### 1. Context Management
```python
# Bad: Always include full history
messages = all_previous_messages + [new_message]

# Good: Truncate or summarize old messages
recent_messages = messages[-10:]  # Keep only last 10
summary = summarize_older_messages(messages[:-10])
optimized_messages = [summary] + recent_messages
```

### 2. Model Cascading
```python
# Try cheap model first
try:
    result = cheap_model.chat(prompt)
    if is_good_enough(result):
        return result
except:
    pass

# Fall back to expensive model
return expensive_model.chat(prompt)
```

### 3. Prompt Optimization
```python
# Bad: Verbose prompt
prompt = "Please analyze this document and provide a comprehensive summary..."

# Good: Concise prompt  
prompt = "Summarize key points in 3 bullets:"
```

## API Setup

### Environment Variables
```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic  
export ANTHROPIC_API_KEY="sk-ant-..."

# Google
export GOOGLE_API_KEY="AIza..."
```

### Quick Test
```python
from utils.model_client import LLMClient

# Test each provider
for provider in ["openai", "anthropic", "google"]:
    try:
        client = LLMClient(provider)
        response, time = client.chat([
            {"role": "user", "content": "Say hello!"}
        ])
        print(f"✅ {provider}: {response[:50]}... ({time:.2f}s)")
    except Exception as e:
        print(f"❌ {provider}: {str(e)}")
```

## When to Switch Models

### Upgrade Signals 🔼
- Consistent poor quality results
- Need larger context window
- Speed is too slow for users
- Cost is becoming significant

### Downgrade Signals 🔽
- Overcomplicating simple tasks
- Burning budget on easy requests
- Speed is more important than perfection
- Model is overkill for use case

Remember: **Start simple, optimize based on real usage patterns!**