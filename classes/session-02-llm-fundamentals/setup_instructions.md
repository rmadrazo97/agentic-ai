# Session 2 Setup Instructions 🛠️

Follow these steps to get ready for the LLM Fundamentals lab.

## Prerequisites

- Python 3.8+ installed
- Git access to course repository
- Text editor or IDE

## Step 1: Install Dependencies

```bash
# Navigate to session directory
cd classes/session-02-llm-fundamentals/labs

# Install required packages
pip install openai anthropic google-generativeai pyyaml tiktoken
```

## Step 2: Get API Keys

You'll need at least ONE of these API keys to participate:

### Option A: OpenAI (Recommended for beginners)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

### Option B: Anthropic Claude
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up for an account  
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### Option C: Google Gemini
1. Go to [ai.google.dev](https://ai.google.dev)
2. Sign up for an account
3. Navigate to API section
4. Create a new API key
5. Copy the key (starts with `AIza`)

## Step 3: Set Environment Variables

### On macOS/Linux:
```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export OPENAI_API_KEY="sk-your-key-here"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"  
export GOOGLE_API_KEY="AIza-your-key-here"

# Reload your shell or run:
source ~/.bashrc  # or ~/.zshrc
```

### On Windows:
```cmd
# Set for current session
set OPENAI_API_KEY=sk-your-key-here
set ANTHROPIC_API_KEY=sk-ant-your-key-here
set GOOGLE_API_KEY=AIza-your-key-here

# Or set permanently in System Environment Variables
```

## Step 4: Test Your Setup

```bash
# Navigate to labs directory
cd classes/session-02-llm-fundamentals/labs

# Test basic functionality
python prompt_lab.py --help

# Test with your provider (choose one)
python prompt_lab.py --pattern zero --provider openai
python prompt_lab.py --pattern zero --provider anthropic  
python prompt_lab.py --pattern zero --provider google
```

**Expected output:**
```
🤖 Testing zero pattern with openai (gpt-4o-mini)
============================================================
📄 Article preview: AI Agents Transform Customer Service: Major Banks Report 40% Cost Reduction...

🎯 ZERO RESULT:
----------------------------------------
• Major banks report 40% cost reduction using AI customer service agents
• AI systems handle 73% of inquiries without human intervention  
• Customer satisfaction scores increased by 23% across participating institutions

💰 Cost: $0.0012 (156 in + 45 out tokens)
```

## Step 5: Verify File Structure

Your lab directory should look like this:

```
labs/
├── prompt_lab.py          # ✅ Main lab file
├── prompts/
│   ├── article.txt        # ✅ Sample article
│   └── fewshot_examples.json # ✅ Example prompts
├── eval/
│   ├── rubric.yaml        # ✅ Evaluation config
│   └── run_eval.py        # ✅ Evaluation runner
├── utils/
│   ├── model_client.py    # ✅ Multi-provider client
│   └── cost_tracker.py    # ✅ Cost tracking
└── docs/
    └── model_selection.md  # ✅ Provider guide
```

## Troubleshooting

### ❌ "API key not found"
- Check environment variable is set: `echo $OPENAI_API_KEY`
- Restart your terminal after setting variables
- Make sure key doesn't have extra spaces

### ❌ "Module not found"
```bash
pip install --upgrade pip
pip install openai anthropic google-generativeai
```

### ❌ "Permission denied" or rate limit errors
- Check your API key is valid and has credits
- Try a different provider
- Wait a few seconds between requests

### ❌ Import errors with utils modules
```bash
# Make sure you're in the labs directory
cd classes/session-02-llm-fundamentals/labs
python prompt_lab.py
```

## Optional: Install Promptfoo (Advanced)

For automated evaluation:

```bash
# Install Node.js first, then:
npm install -g promptfoo

# Test installation
promptfoo --version

# Run evaluation
promptfoo eval eval/rubric.yaml
```

## Cost Warning ⚠️

- Each API call costs money (usually < $0.01)
- The lab should cost under $1 total to complete
- Monitor your usage in provider dashboards
- Set billing alerts if concerned

## Getting Help

- **During class**: Raise your hand or ask in chat
- **Slack**: Post in #lab-help channel
- **GitHub**: Open an issue on the course repo
- **Office hours**: Check course schedule

---

**You're ready! 🚀 See you in Session 2!**