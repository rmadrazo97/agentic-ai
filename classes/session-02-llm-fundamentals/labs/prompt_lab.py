#!/usr/bin/env python3
"""
LLM Prompt Engineering Lab
Students edit this file to experiment with different prompting patterns

Usage:
    python prompt_lab.py --pattern zero --provider openai
    python prompt_lab.py --pattern fewshot --provider anthropic --model claude-3-haiku-20240307
    python prompt_lab.py --pattern json --provider google
    python prompt_lab.py --compare  # Compare all patterns and providers

Tasks:
    1. Implement zero_shot() function
    2. Improve few_shot() with examples
    3. Add JSON schema enforcement
    4. (Stretch) Chain of thought reasoning
"""

import json
import argparse
import pathlib
import sys
from typing import Dict, List

# Add utils to path
sys.path.append(str(pathlib.Path(__file__).parent))

from utils.model_client import LLMClient
from utils.cost_tracker import PriceMeter


def zero_shot(client: LLMClient, article: str) -> str:
    """
    Basic zero-shot prompting - just ask directly
    
    TODO: Students implement this function
    - Create a simple, clear prompt for summarization
    - Ask for exactly 3 bullet points
    - Return the model's response
    """
    
    # 🚀 STUDENT TODO: Implement zero-shot prompting
    # Hint: Keep it simple and specific!
    
    messages = [
        {
            "role": "user", 
            "content": f"""Summarize the following article in exactly 3 bullet points:

{article}

Format: Use bullet points (•) and keep each point under 15 words."""
        }
    ]
    
    response, runtime = client.chat(messages, temperature=0.3)
    return response


def few_shot(client: LLMClient, article: str, examples: List[Dict]) -> str:
    """
    Few-shot prompting with examples
    
    TODO: Students improve this function
    - Use the provided examples effectively
    - Structure the prompt clearly
    - Maintain consistent formatting
    """
    
    # 🚀 STUDENT TODO: Improve few-shot prompting
    # Use the examples from fewshot_examples.json
    
    # Format examples for the prompt
    example_text = ""
    for i, ex in enumerate(examples[:2]):  # Use first 2 examples
        example_text += f"\nExample {i+1}:\n"
        example_text += f"Article: {ex['article'][:100]}...\n"
        example_text += "Summary:\n"
        for point in ex['summary']:
            example_text += f"• {point}\n"
    
    messages = [
        {
            "role": "user",
            "content": f"""You are an expert summarizer. Here are examples of good summaries:

{example_text}

Now summarize this article in exactly 3 bullet points:

{article}

Format: Use bullet points (•) and keep each point under 15 words."""
        }
    ]
    
    response, runtime = client.chat(messages, temperature=0.3)
    return response


def json_schema(client: LLMClient, article: str) -> str:
    """
    Structured output with JSON schema
    
    TODO: Students implement JSON enforcement
    - Define a clear JSON structure
    - Handle parsing errors gracefully
    - Validate the output format
    """
    
    # 🚀 STUDENT TODO: Implement JSON schema prompting
    # Force structured output for easier parsing
    
    schema = {
        "summary": "string (one sentence overview)",
        "key_points": ["array", "of", "three", "bullet", "points"],
        "sentiment": "positive|neutral|negative",
        "word_count": "integer (estimated words in original)"
    }
    
    messages = [
        {
            "role": "user",
            "content": f"""Analyze this article and return a JSON response with this exact structure:

{json.dumps(schema, indent=2)}

Article to analyze:
{article}

IMPORTANT: Return only valid JSON, no additional text."""
        }
    ]
    
    response, runtime = client.chat(messages, temperature=0.1)  # Lower temp for consistency
    
    # Try to parse and validate JSON
    try:
        parsed = json.loads(response)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        return f"JSON PARSE ERROR - Raw response:\n{response}"


def chain_of_thought(client: LLMClient, article: str) -> str:
    """
    Chain of thought reasoning (stretch goal)
    
    TODO: Advanced students implement CoT
    - Break down the task into steps
    - Show reasoning process
    - Use <thinking> tags for transparency
    """
    
    # 🚀 STRETCH GOAL: Implement chain of thought
    messages = [
        {
            "role": "user",
            "content": f"""Let's analyze this article step by step:

<thinking>
1. First, I'll identify the main topic
2. Then find the 3 most important points
3. Finally, write concise bullet points
</thinking>

Article:
{article}

Please show your reasoning process and then provide 3 bullet point summary."""
        }
    ]
    
    response, runtime = client.chat(messages, temperature=0.5)
    return response


def load_sample_data():
    """Load article and examples from files"""
    base_path = pathlib.Path(__file__).parent / "prompts"
    
    # Load sample article
    article_path = base_path / "article.txt"
    if not article_path.exists():
        return "Sample article not found. Please create prompts/article.txt", []
    
    article = article_path.read_text().strip()
    
    # Load few-shot examples
    examples_path = base_path / "fewshot_examples.json"
    if not examples_path.exists():
        return article, []
    
    try:
        with open(examples_path) as f:
            data = json.load(f)
            return article, data.get("examples", [])
    except (json.JSONDecodeError, FileNotFoundError):
        return article, []


def run_single_pattern(args):
    """Run a single prompting pattern"""
    print(f"\n🤖 Testing {args.pattern} pattern with {args.provider} ({args.model})")
    print("=" * 60)
    
    # Initialize client and cost tracker
    client = LLMClient(args.provider, args.model)
    meter = PriceMeter(args.provider)
    
    # Load data
    article, examples = load_sample_data()
    if not article or article.startswith("Sample article not found"):
        print("❌ Error: Could not load sample article")
        return
    
    print(f"📄 Article preview: {article[:100]}...")
    print()
    
    # Run the selected pattern
    try:
        if args.pattern == "zero":
            output = zero_shot(client, article)
        elif args.pattern == "fewshot":
            output = few_shot(client, article, examples)
        elif args.pattern == "json":
            output = json_schema(client, article)
        elif args.pattern == "cot":
            output = chain_of_thought(client, article)
        else:
            print(f"❌ Unknown pattern: {args.pattern}")
            return
        
        # Calculate cost
        cost, breakdown = meter.estimate_cost(article, output, args.model)
        
        print(f"🎯 {args.pattern.upper()} RESULT:")
        print("-" * 40)
        print(output)
        print()
        print(f"💰 Cost: ${cost:.4f} ({breakdown['input_tokens']} in + {breakdown['output_tokens']} out tokens)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def run_comparison():
    """Compare all patterns and providers"""
    print("\n🔬 COMPARISON MODE - Testing all patterns")
    print("=" * 60)
    
    article, examples = load_sample_data()
    if not article:
        print("❌ Error: Could not load sample article")
        return
    
    patterns = ["zero", "fewshot", "json"]
    providers = [
        ("openai", "gpt-4o-mini"),
        ("anthropic", "claude-3-haiku-20240307"),
        ("google", "gemini-2.0-flash-exp")
    ]
    
    results = []
    
    for pattern in patterns:
        for provider, model in providers:
            try:
                print(f"\n⚡ {pattern} + {provider}...")
                client = LLMClient(provider, model)
                meter = PriceMeter(provider)
                
                if pattern == "zero":
                    output = zero_shot(client, article)
                elif pattern == "fewshot":
                    output = few_shot(client, article, examples)
                elif pattern == "json":
                    output = json_schema(client, article)
                
                cost, breakdown = meter.estimate_cost(article, output, model)
                
                results.append({
                    "pattern": pattern,
                    "provider": provider,
                    "model": model,
                    "cost": cost,
                    "tokens": breakdown["input_tokens"] + breakdown["output_tokens"],
                    "output_preview": output[:100] + "..." if len(output) > 100 else output
                })
                
            except Exception as e:
                print(f"❌ Failed {pattern} + {provider}: {str(e)}")
    
    # Print results table
    print("\n📊 COMPARISON RESULTS:")
    print("-" * 80)
    print(f"{'Pattern':<10} {'Provider':<12} {'Cost':<10} {'Tokens':<8} {'Preview':<30}")
    print("-" * 80)
    
    for r in sorted(results, key=lambda x: x["cost"]):
        print(f"{r['pattern']:<10} {r['provider']:<12} ${r['cost']:<9.4f} {r['tokens']:<8} {r['output_preview'][:30]:<30}")


def main():
    parser = argparse.ArgumentParser(description="LLM Prompt Engineering Lab")
    parser.add_argument("--pattern", choices=["zero", "fewshot", "json", "cot"], 
                       default="zero", help="Prompting pattern to test")
    parser.add_argument("--provider", choices=["openai", "anthropic", "google"], 
                       default="openai", help="LLM provider")
    parser.add_argument("--model", help="Specific model (optional)")
    parser.add_argument("--compare", action="store_true", 
                       help="Compare all patterns and providers")
    
    args = parser.parse_args()
    
    if args.compare:
        run_comparison()
    else:
        run_single_pattern(args)


if __name__ == "__main__":
    main()