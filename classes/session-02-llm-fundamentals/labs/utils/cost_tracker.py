"""
Cost tracking utility for LLM API calls
Estimates costs based on token usage and provider pricing
"""

import tiktoken
from typing import Dict, Tuple


class PriceMeter:
    """Track and estimate costs for different LLM providers"""
    
    # Pricing per 1M tokens (input/output) as of 2024
    PRICING = {
        "openai": {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        },
        "anthropic": {
            "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
            "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        },
        "google": {
            "gemini-2.0-flash-exp": {"input": 0.075, "output": 0.30},
            "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
            "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        }
    }
    
    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.total_cost = 0.0
        self.call_history = []
        
        # Initialize tokenizer for OpenAI models (approximate for others)
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except:
            self.tokenizer = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text (approximate for non-OpenAI models)"""
        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        else:
            # Rough approximation: 1 token ≈ 4 characters
            return len(text) // 4
    
    def estimate_cost(self, input_text: str, output_text: str, model: str) -> Tuple[float, Dict]:
        """
        Estimate cost for an API call
        
        Args:
            input_text: The prompt/input sent to model
            output_text: The response from model
            model: Model name used
            
        Returns:
            Tuple of (total_cost, breakdown_dict)
        """
        input_tokens = self.count_tokens(input_text)
        output_tokens = self.count_tokens(output_text)
        
        # Get pricing for this provider/model
        try:
            pricing = self.PRICING[self.provider][model]
        except KeyError:
            # Fallback to first available model for provider
            available_models = list(self.PRICING[self.provider].keys())
            if available_models:
                pricing = self.PRICING[self.provider][available_models[0]]
                print(f"Warning: Using {available_models[0]} pricing for unknown model {model}")
            else:
                print(f"Warning: No pricing data for {self.provider}")
                return 0.0, {}
        
        # Calculate costs (pricing is per 1M tokens)
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost
        
        breakdown = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost,
            "model": model,
            "provider": self.provider
        }
        
        # Track for session totals
        self.total_cost += total_cost
        self.call_history.append(breakdown)
        
        return total_cost, breakdown
    
    def get_session_summary(self) -> Dict:
        """Get summary of all costs in this session"""
        if not self.call_history:
            return {"total_cost": 0, "total_calls": 0, "avg_cost": 0}
        
        total_input_tokens = sum(call["input_tokens"] for call in self.call_history)
        total_output_tokens = sum(call["output_tokens"] for call in self.call_history)
        
        return {
            "total_cost": self.total_cost,
            "total_calls": len(self.call_history),
            "avg_cost_per_call": self.total_cost / len(self.call_history),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "provider": self.provider
        }
    
    def compare_providers(self, input_text: str, output_text: str) -> Dict:
        """Compare cost across all providers for the same input/output"""
        comparisons = {}
        
        for provider in self.PRICING:
            for model in self.PRICING[provider]:
                temp_meter = PriceMeter(provider)
                cost, _ = temp_meter.estimate_cost(input_text, output_text, model)
                comparisons[f"{provider}_{model}"] = cost
        
        # Sort by cost
        sorted_options = sorted(comparisons.items(), key=lambda x: x[1])
        
        return {
            "cheapest": sorted_options[0],
            "most_expensive": sorted_options[-1],
            "all_options": dict(sorted_options)
        }


# Example usage and testing
if __name__ == "__main__":
    # Test cost estimation
    meter = PriceMeter("openai")
    
    sample_input = "Summarize this article about AI in 3 bullet points."
    sample_output = """
    • AI technology is rapidly advancing across multiple domains
    • Machine learning models are becoming more efficient and accessible  
    • Integration challenges remain for enterprise applications
    """
    
    cost, breakdown = meter.estimate_cost(sample_input, sample_output, "gpt-4o-mini")
    
    print(f"Estimated cost: ${cost:.4f}")
    print(f"Breakdown: {breakdown}")
    
    # Test provider comparison
    comparison = meter.compare_providers(sample_input, sample_output)
    print(f"\nCheapest option: {comparison['cheapest']}")
    print(f"Most expensive: {comparison['most_expensive']}")