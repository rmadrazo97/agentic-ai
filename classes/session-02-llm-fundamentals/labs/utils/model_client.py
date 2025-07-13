"""
Multi-provider LLM client wrapper
Supports OpenAI, Anthropic, and Google models with unified interface
"""

from typing import List, Dict, Tuple
import os
import json
import time
import openai
import anthropic
import google.generativeai as genai


class LLMClient:
    """Unified client for multiple LLM providers"""
    
    def __init__(self, provider: str = "openai", model: str = None):
        self.provider = provider.lower()
        self.model = model
        
        # Initialize provider-specific clients
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable required")
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model or "gpt-4o-mini"
            
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable required")
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model or "claude-3-haiku-20240307"
            
        elif self.provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable required")
            genai.configure(api_key=api_key)
            self.model = model or "gemini-2.0-flash-exp"
            self.client = genai.GenerativeModel(self.model)
            
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai', 'anthropic', or 'google'")

    def chat(self, messages: List[Dict], **params) -> Tuple[str, float]:
        """
        Send chat messages to the model and return response + timing
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **params: Additional parameters like temperature, max_tokens
            
        Returns:
            Tuple of (response_text, runtime_seconds)
        """
        start_time = time.time()
        
        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=params.get("temperature", 0.7),
                    max_tokens=params.get("max_tokens", 1000),
                )
                output = response.choices[0].message.content
                
            elif self.provider == "anthropic":
                # Convert messages for Anthropic format
                if messages[0]["role"] == "system":
                    system_msg = messages[0]["content"]
                    user_messages = messages[1:]
                else:
                    system_msg = ""
                    user_messages = messages
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=params.get("max_tokens", 1000),
                    temperature=params.get("temperature", 0.7),
                    system=system_msg,
                    messages=user_messages
                )
                output = response.content[0].text
                
            elif self.provider == "google":
                # Google Gemini expects just the content
                user_content = messages[-1]["content"]
                response = self.client.generate_content(
                    user_content,
                    generation_config=genai.types.GenerationConfig(
                        temperature=params.get("temperature", 0.7),
                        max_output_tokens=params.get("max_tokens", 1000),
                    )
                )
                output = response.text
                
        except Exception as e:
            raise Exception(f"Error calling {self.provider} API: {str(e)}")
        
        runtime = time.time() - start_time
        return output, runtime

    def get_model_info(self) -> Dict:
        """Return information about the current model"""
        return {
            "provider": self.provider,
            "model": self.model,
            "supports_system": self.provider in ["openai", "anthropic"],
            "supports_function_calls": self.provider in ["openai", "google"],
        }


# Example usage
if __name__ == "__main__":
    # Test with environment variables set
    client = LLMClient("openai")
    
    messages = [
        {"role": "user", "content": "Explain what a neural network is in one sentence."}
    ]
    
    response, runtime = client.chat(messages, temperature=0.3)
    print(f"Response ({runtime:.2f}s): {response}")