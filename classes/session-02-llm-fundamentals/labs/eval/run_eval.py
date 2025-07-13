#!/usr/bin/env python3
"""
Evaluation runner for prompt engineering lab
Compares different prompting patterns and provides automated scoring

Usage:
    python eval/run_eval.py                    # Run basic evaluation
    python eval/run_eval.py --detailed         # Detailed analysis
    python eval/run_eval.py --save-report      # Save results to file
"""

import argparse
import json
import pathlib
import subprocess
import sys
import time
from typing import Dict, List

# Add utils to path
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from utils.model_client import LLMClient
from utils.cost_tracker import PriceMeter


def run_promptfoo_eval():
    """Run Promptfoo evaluation if available"""
    try:
        # Check if promptfoo is installed
        result = subprocess.run(['promptfoo', '--version'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  Promptfoo not installed. Skipping automated evaluation.")
            return None
        
        # Run evaluation
        eval_path = pathlib.Path(__file__).parent / "rubric.yaml"
        result = subprocess.run(['promptfoo', 'eval', str(eval_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Promptfoo evaluation completed successfully")
            return result.stdout
        else:
            print(f"❌ Promptfoo evaluation failed: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("⚠️  Promptfoo not found. Install with: npm install -g promptfoo")
        return None


def manual_evaluation():
    """Run manual evaluation using our lab functions"""
    print("🔧 Running manual evaluation...")
    
    # Import our lab functions
    from prompt_lab import zero_shot, few_shot, json_schema, load_sample_data
    
    article, examples = load_sample_data()
    if not article:
        print("❌ Could not load sample data")
        return {}
    
    patterns = ["zero", "fewshot", "json"]
    providers = [
        ("openai", "gpt-4o-mini"),
        ("anthropic", "claude-3-haiku-20240307"),
    ]
    
    results = {}
    
    for pattern in patterns:
        for provider, model in providers:
            key = f"{pattern}_{provider}"
            try:
                print(f"  Testing {key}...")
                
                client = LLMClient(provider, model)
                meter = PriceMeter(provider)
                
                start_time = time.time()
                
                if pattern == "zero":
                    output = zero_shot(client, article)
                elif pattern == "fewshot":
                    output = few_shot(client, article, examples)
                elif pattern == "json":
                    output = json_schema(client, article)
                else:
                    continue
                
                runtime = time.time() - start_time
                cost, breakdown = meter.estimate_cost(article, output, model)
                
                # Simple quality scoring
                quality_score = calculate_quality_score(output, pattern)
                
                results[key] = {
                    "pattern": pattern,
                    "provider": provider,
                    "model": model,
                    "output": output,
                    "cost": cost,
                    "runtime": runtime,
                    "tokens": breakdown["input_tokens"] + breakdown["output_tokens"],
                    "quality_score": quality_score
                }
                
            except Exception as e:
                print(f"  ❌ Failed {key}: {str(e)}")
                results[key] = {"error": str(e)}
    
    return results


def calculate_quality_score(output: str, pattern: str) -> float:
    """
    Simple heuristic scoring for output quality
    Returns score from 0-100
    """
    score = 0
    
    # Basic formatting checks
    if "•" in output or "-" in output:
        score += 20  # Has bullet points
    
    # Content length check
    word_count = len(output.split())
    if 30 <= word_count <= 100:
        score += 20  # Good length
    elif word_count <= 150:
        score += 10  # Acceptable length
    
    # Key term relevance
    key_terms = ["AI", "bank", "customer", "service", "cost", "reduction"]
    found_terms = sum(1 for term in key_terms if term.lower() in output.lower())
    score += min(found_terms * 5, 25)  # Up to 25 points for relevance
    
    # Pattern-specific checks
    if pattern == "json":
        try:
            json.loads(output)
            score += 25  # Valid JSON
        except:
            score -= 20  # Invalid JSON penalty
    
    # Structure check for bullet points
    bullet_count = output.count("•") + output.count("-")
    if bullet_count == 3:
        score += 10  # Exactly 3 points
    elif bullet_count > 0:
        score += 5   # Some structure
    
    return min(score, 100)


def print_evaluation_report(results: Dict, detailed: bool = False):
    """Print formatted evaluation results"""
    print("\n" + "="*80)
    print("🎯 EVALUATION REPORT")
    print("="*80)
    
    if not results:
        print("❌ No results to display")
        return
    
    # Sort by quality score
    sorted_results = sorted(
        [(k, v) for k, v in results.items() if "error" not in v],
        key=lambda x: x[1].get("quality_score", 0),
        reverse=True
    )
    
    print(f"\n📊 SUMMARY (Top performers by quality score):")
    print("-" * 60)
    print(f"{'Rank':<4} {'Pattern':<10} {'Provider':<12} {'Score':<6} {'Cost':<8} {'Time':<6}")
    print("-" * 60)
    
    for i, (key, result) in enumerate(sorted_results[:5]):
        print(f"{i+1:<4} {result['pattern']:<10} {result['provider']:<12} "
              f"{result['quality_score']:<6.1f} ${result['cost']:<7.4f} {result['runtime']:<6.2f}s")
    
    if detailed:
        print(f"\n📝 DETAILED RESULTS:")
        print("-" * 80)
        
        for key, result in sorted_results:
            print(f"\n🔍 {key.upper()}")
            print(f"Quality Score: {result['quality_score']:.1f}/100")
            print(f"Cost: ${result['cost']:.4f}")
            print(f"Runtime: {result['runtime']:.2f}s")
            print(f"Tokens: {result['tokens']}")
            print(f"Output preview: {result['output'][:200]}...")
            print("-" * 40)
    
    # Show errors if any
    errors = [(k, v) for k, v in results.items() if "error" in v]
    if errors:
        print(f"\n❌ ERRORS:")
        for key, error_result in errors:
            print(f"  {key}: {error_result['error']}")


def save_report(results: Dict, filename: str = "eval_report.json"):
    """Save evaluation results to file"""
    output_path = pathlib.Path(__file__).parent / filename
    
    # Prepare data for JSON serialization
    json_results = {}
    for key, result in results.items():
        if "error" not in result:
            json_results[key] = {
                "pattern": result["pattern"],
                "provider": result["provider"],
                "model": result["model"],
                "cost": result["cost"],
                "runtime": result["runtime"],
                "tokens": result["tokens"],
                "quality_score": result["quality_score"],
                "output_preview": result["output"][:300]
            }
    
    with open(output_path, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"💾 Report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate prompt engineering lab results")
    parser.add_argument("--detailed", action="store_true", 
                       help="Show detailed results for each pattern")
    parser.add_argument("--save-report", action="store_true",
                       help="Save results to JSON file")
    parser.add_argument("--promptfoo", action="store_true",
                       help="Try to run Promptfoo evaluation first")
    
    args = parser.parse_args()
    
    print("🔬 Starting Prompt Engineering Evaluation")
    
    # Try Promptfoo first if requested
    if args.promptfoo:
        promptfoo_results = run_promptfoo_eval()
        if promptfoo_results:
            print("Promptfoo Results:")
            print(promptfoo_results)
    
    # Run manual evaluation
    results = manual_evaluation()
    
    # Print results
    print_evaluation_report(results, detailed=args.detailed)
    
    # Save if requested
    if args.save_report:
        save_report(results)
    
    # Return success code based on results
    if results and any("error" not in v for v in results.values()):
        print("\n✅ Evaluation completed successfully!")
        return 0
    else:
        print("\n❌ Evaluation failed or no valid results")
        return 1


if __name__ == "__main__":
    sys.exit(main())