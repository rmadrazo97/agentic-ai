# Session 2: LLM Fundamentals & Prompt Engineering 🧠

**Duration**: 80 minutes | **Time**: 8:30 - 9:50

---

## 🎯 Session Goals
- Understand how LLMs actually work under the hood
- Master core prompt engineering patterns
- Choose the right model for your use case
- Build your first production-ready prompt lab

---

## ⏱️ Session Timeline

### 1. Stand-up #1 (10 min)

#### 📊 Team Progress Format
**1-line per team**: Yesterday's progress → Today's target → Blocker

```markdown
Team Alpha: ✅ Set up repo structure → 🎯 Basic agent skeleton → 🚧 API key setup
Team Beta: ✅ Chose domain (EdTech) → 🎯 Research RAG patterns → 🚧 None
Team Gamma: ✅ Team formation → 🎯 Project charter → 🚧 Need help with scope
```

**Post as comments on your team's Draft PR**

---

### 2. Micro-Lecture 1: "How an LLM Works" (15 min)

#### 🔍 The Magic Revealed

##### **Tokenization** - Words → Numbers
```python
# Example: "Hello world!" becomes [15496, 1917, 0]
import tiktoken
encoder = tiktoken.get_encoding("cl100k_base")
tokens = encoder.encode("Hello world!")
print(f"Tokens: {tokens}")  # [15496, 1917, 0]
print(f"Count: {len(tokens)}")  # 3 tokens
```

##### **Context Windows** - Your Memory Budget
| Model | Context Limit | Real Cost Impact |
|-------|---------------|------------------|
| GPT-4o-mini | 128K tokens | ~$0.60 per full context |
| Claude 3.5 Haiku | 200K tokens | ~$1.00 per full context |
| Gemini 2.0 Flash | 1M tokens | ~$7.50 per full context |

##### **Sampling** - Creativity vs Consistency
```python
# Temperature = 0: Always same output (deterministic)
# Temperature = 0.7: Balanced creativity 
# Temperature = 1.2: Wild and unpredictable
```

#### 🎮 [Live Token Visualizer →](https://platform.openai.com/tokenizer)

---

### 3. Micro-Lecture 2: Prompt Patterns (15 min)

#### 🎯 Evolution of Prompting

##### **Zero-Shot** - Just Ask
```python
prompt = "Summarize this article in 3 bullet points: [ARTICLE]"
```

##### **Few-Shot** - Show Examples
```python
prompt = """
Examples:
Article: "Bitcoin rises 5%..." → • Bitcoin gains 5% • Driven by institutional demand • Market cap hits $1T

Article: "Climate change impacts..." → • Global temperatures rising • Extreme weather increasing • Action needed urgently

Now summarize: [YOUR_ARTICLE]
"""
```

##### **Chain of Thought (CoT)** - Think Step by Step
```python
prompt = "Let's think step by step:\n1. What is the main topic?\n2. What are the key facts?\n3. What's the conclusion?\n\nNow summarize: [ARTICLE]"
```

##### **JSON/Function Calls** - Structured Output
```python
prompt = """
Return JSON with this exact structure:
{
  "summary": "one sentence",
  "key_points": ["point1", "point2", "point3"],
  "sentiment": "positive|neutral|negative"
}
"""
```

#### ⚡ Live Demo Time!
```bash
# Follow along - we'll test each pattern live
cd classes/session-02-llm-fundamentals/labs
python prompt_lab.py --pattern zero
python prompt_lab.py --pattern fewshot --provider anthropic
```

---

### 4. Micro-Lecture 3: Choosing a Model (10 min)

#### 🤔 Decision Framework

##### **Context Need**
- **< 4K tokens**: Any model works
- **< 128K tokens**: GPT-4o, Claude 3.5
- **< 1M tokens**: Gemini 2.0 Pro only

##### **Priority Triangle** (Pick 2 of 3)
```
     SPEED
    /     \
   /       \
  /         \
PRICE ---- ACCURACY
```

##### **Provider Comparison**
| Provider | Best For | Strengths | Cost (per 1M tokens) |
|----------|----------|-----------|---------------------|
| **OpenAI** | General use | Fastest adoption, tools | $2.50 (4o-mini) |
| **Anthropic** | Complex reasoning | Safety, long context | $1.25 (Haiku) |
| **Google** | Multimodal | Huge context, vision | $0.075 (Flash) |
| **X AI** | Real-time data | Live web access | $5.00 (Grok) |

#### 📋 [Model Selection Cheat Sheet →](./docs/model_selection.md)

---

### 5. Guided Lab: Prompt Engineering CLI (20 min)

#### 🛠️ Setup Instructions

```bash
# 1. Navigate to lab directory
cd classes/session-02-llm-fundamentals/labs

# 2. Set up API keys (choose one)
export OPENAI_API_KEY="sk-..."        # GPT models
export ANTHROPIC_API_KEY="sk-ant-..."  # Claude models  
export GOOGLE_API_KEY="AI..."          # Gemini models

# 3. Install dependencies
pip install openai anthropic google-generativeai pyyaml

# 4. Test basic functionality
python prompt_lab.py --help
```

#### 🧪 Lab Tasks

##### **Task 1: Zero-Shot Baseline**
```bash
python prompt_lab.py --pattern zero --provider openai
```

##### **Task 2: Few-Shot Improvement**
```bash
python prompt_lab.py --pattern fewshot --provider anthropic
```

##### **Task 3: JSON Schema Enforcement**
```bash
python prompt_lab.py --pattern json --provider google
```

##### **Task 4: Cost Comparison**
```bash
python prompt_lab.py --pattern fewshot --provider openai --model gpt-4o-mini
python prompt_lab.py --pattern fewshot --provider anthropic --model claude-3-haiku-20240307
```

#### 📊 Track Your Results
- **Quality**: Which pattern gives best summaries?
- **Speed**: Which provider is fastest?
- **Cost**: Which setup is most economical?

---

### 6. Wrap-up & Next Steps (10 min)

#### ✅ Before You Leave
- [ ] Ran all 4 lab tasks successfully
- [ ] Compared results across providers
- [ ] Committed your best prompt_lab.py
- [ ] Created branch `lab-prompt-eng`

#### 📚 Homework (Due Session 3)

1. **Read**: [Anthropic's Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/introduction-to-prompt-design)
2. **Read**: Chapter 2 of [LLM Agents in Practice](https://www.manning.com/books/llm-agents-in-practice)
3. **Complete**: Lab deliverable (see below)
4. **Optional**: Try [Promptfoo](https://www.promptfoo.dev/) for automated evaluation

#### 🎯 Lab Deliverable

**Push to branch `lab-prompt-eng`:**

1. **Modified `prompt_lab.py`** with:
   - ✅ Working zero-shot implementation
   - ✅ Working few-shot implementation  
   - ✅ Working JSON schema implementation
   - ✅ Cost tracking and comparison

2. **Create `EVAL_REPORT.md`** with:
   - Results table (pattern vs quality score)
   - Cost comparison across providers
   - Reflection: "Which tweak gave the biggest quality jump and why?"

**Auto-grading**: PR must pass CI tests = Lab Checkpoint 1 complete

---

## 🔧 Lab Files Structure

```
labs/
├── prompt_lab.py          # 👈 Main file you'll edit
├── prompts/
│   ├── article.txt        # Sample article to summarize
│   └── fewshot_examples.json
├── eval/
│   ├── rubric.yaml        # Automated test cases
│   └── run_eval.py        # Evaluation runner
├── utils/
│   ├── model_client.py    # Multi-provider wrapper
│   └── cost_tracker.py    # Token & cost tracking
└── docs/
    └── model_selection.md  # Provider comparison guide
```

---

## 🚨 Quick Fixes for Common Issues

| Problem | Solution |
|---------|----------|
| **"Under-specified output"** | Add format: "Return exactly 3 bullets ≤ 12 words each" |
| **"Hallucinated facts"** | Add: "Only use information from the provided text" |
| **"Unstable JSON"** | Use function calling or strict schema validation |
| **"High cost"** | Truncate context, use cheaper models for simple tasks |
| **"High latency"** | Try Claude Haiku or Gemini Flash for speed |

---

## 🎉 Share Your Wins!

**Post your best results in #lab-results Slack:**
- Screenshot of cost comparison
- Your most improved prompt
- Interesting failure cases

---

*Next Session: Tool-Calling Agents & ReAct Patterns*