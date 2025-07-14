"""
Callback System for Cost and Performance Tracking
Advanced monitoring, logging, and metrics collection for agent operations
"""

import json
import time
import os
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult


class CostLatencyCallback(BaseCallbackHandler):
    """
    Comprehensive callback for tracking cost, latency, and performance metrics
    """
    
    def __init__(self, log_file: str = "metrics.json", session_id: str = "default"):
        super().__init__()
        self.log_file = log_file
        self.session_id = session_id
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else ".", exist_ok=True)
        
        # Session tracking
        self.session_start = time.time()
        self.current_chain_start = None
        self.current_llm_start = None
        self.current_tool_start = None
        
        # Counters and accumulators
        self.total_tokens = 0
        self.total_cost = 0.0
        self.llm_calls = 0
        self.tool_calls = 0
        self.errors = 0
        
        # Detailed logs
        self.events = []
        self.tool_usage = {}
        self.model_usage = {}
        
        # Cost models (per 1M tokens)
        self.token_costs = {
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
            "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
            "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
        }
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on model and token usage"""
        if model not in self.token_costs:
            # Default to Claude Haiku pricing
            model = "claude-3-haiku-20240307"
        
        costs = self.token_costs[model]
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        
        return input_cost + output_cost
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event with timestamp"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)
    
    # Chain-level callbacks
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        """Called when a chain starts running"""
        self.current_chain_start = time.time()
        
        self._log_event("chain_start", {
            "chain_type": serialized.get("name", "unknown"),
            "inputs": list(inputs.keys())
        })
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs) -> None:
        """Called when a chain finishes running"""
        if self.current_chain_start:
            duration = time.time() - self.current_chain_start
            
            self._log_event("chain_end", {
                "duration_seconds": duration,
                "outputs": list(outputs.keys())
            })
            
            self.current_chain_start = None
    
    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs) -> None:
        """Called when a chain encounters an error"""
        self.errors += 1
        
        self._log_event("chain_error", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })
    
    # LLM-level callbacks
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Called when LLM starts generating"""
        self.current_llm_start = time.time()
        self.llm_calls += 1
        
        # Estimate input tokens
        input_tokens = sum(self._estimate_tokens(prompt) for prompt in prompts)
        
        model_name = kwargs.get("invocation_params", {}).get("model_name", "unknown")
        
        self._log_event("llm_start", {
            "model": model_name,
            "prompt_count": len(prompts),
            "estimated_input_tokens": input_tokens
        })
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Called when LLM finishes generating"""
        if self.current_llm_start:
            duration = time.time() - self.current_llm_start
        else:
            duration = 0
        
        # Extract response text and estimate tokens
        output_text = ""
        for generation_list in response.generations:
            for generation in generation_list:
                output_text += generation.text
        
        output_tokens = self._estimate_tokens(output_text)
        self.total_tokens += output_tokens
        
        # Get model info
        model_name = getattr(response, 'llm_output', {}).get('model_name', 'unknown')
        if model_name == 'unknown':
            # Try to extract from kwargs
            model_name = kwargs.get('invocation_params', {}).get('model_name', 'claude-3-haiku-20240307')
        
        # Update model usage stats
        if model_name not in self.model_usage:
            self.model_usage[model_name] = {"calls": 0, "tokens": 0, "cost": 0.0}
        
        self.model_usage[model_name]["calls"] += 1
        self.model_usage[model_name]["tokens"] += output_tokens
        
        # Calculate cost (rough estimate)
        input_tokens = kwargs.get('input_tokens', 100)  # Fallback estimate
        cost = self._calculate_cost(model_name, input_tokens, output_tokens)
        self.total_cost += cost
        self.model_usage[model_name]["cost"] += cost
        
        self._log_event("llm_end", {
            "model": model_name,
            "duration_seconds": duration,
            "output_tokens": output_tokens,
            "estimated_cost": cost
        })
        
        self.current_llm_start = None
    
    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs) -> None:
        """Called when LLM encounters an error"""
        self.errors += 1
        
        self._log_event("llm_error", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })
    
    # Tool-level callbacks
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        """Called when a tool starts executing"""
        self.current_tool_start = time.time()
        self.tool_calls += 1
        
        tool_name = serialized.get("name", "unknown_tool")
        
        # Update tool usage stats
        if tool_name not in self.tool_usage:
            self.tool_usage[tool_name] = {"calls": 0, "total_duration": 0.0, "errors": 0}
        
        self.tool_usage[tool_name]["calls"] += 1
        
        self._log_event("tool_start", {
            "tool_name": tool_name,
            "input_length": len(input_str)
        })
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Called when a tool finishes executing"""
        if self.current_tool_start:
            duration = time.time() - self.current_tool_start
            
            # Update tool duration stats
            for tool_name in self.tool_usage:
                if self.tool_usage[tool_name]["calls"] > 0:
                    self.tool_usage[tool_name]["total_duration"] += duration
                    break
            
            self._log_event("tool_end", {
                "duration_seconds": duration,
                "output_length": len(output)
            })
            
            self.current_tool_start = None
    
    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs) -> None:
        """Called when a tool encounters an error"""
        self.errors += 1
        
        # Update tool error stats
        for tool_name in self.tool_usage:
            if self.tool_usage[tool_name]["calls"] > 0:
                self.tool_usage[tool_name]["errors"] += 1
                break
        
        self._log_event("tool_error", {
            "error_type": type(error).__name__,
            "error_message": str(error)
        })
    
    # Agent-level callbacks
    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """Called when agent takes an action"""
        self._log_event("agent_action", {
            "tool": action.tool,
            "tool_input": action.tool_input[:100] + "..." if len(action.tool_input) > 100 else action.tool_input,
            "log": action.log[:200] + "..." if len(action.log) > 200 else action.log
        })
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """Called when agent finishes"""
        session_duration = time.time() - self.session_start
        
        self._log_event("agent_finish", {
            "return_values": list(finish.return_values.keys()) if finish.return_values else [],
            "session_duration": session_duration
        })
        
        # Write final metrics to file
        self._write_metrics()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session metrics"""
        session_duration = time.time() - self.session_start
        
        return {
            "session_id": self.session_id,
            "session_duration": session_duration,
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "errors": self.errors,
            "events_count": len(self.events),
            "tools_used": list(self.tool_usage.keys()),
            "models_used": list(self.model_usage.keys())
        }
    
    def _write_metrics(self):
        """Write current metrics to log file"""
        metrics = {
            "session_summary": self.get_session_summary(),
            "tool_usage": self.tool_usage,
            "model_usage": self.model_usage,
            "events": self.events[-50:]  # Keep last 50 events to avoid huge files
        }
        
        # Append to log file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")
    
    def print_summary(self):
        """Print a formatted summary of the session"""
        summary = self.get_session_summary()
        
        print("\n📊 SESSION SUMMARY")
        print("=" * 50)
        print(f"Session ID: {summary['session_id']}")
        print(f"Duration: {summary['session_duration']:.2f} seconds")
        print(f"Total Cost: ${summary['total_cost']:.4f}")
        print(f"Total Tokens: {summary['total_tokens']:,}")
        print(f"LLM Calls: {summary['llm_calls']}")
        print(f"Tool Calls: {summary['tool_calls']}")
        print(f"Errors: {summary['errors']}")
        
        if self.tool_usage:
            print(f"\n🔧 Tool Usage:")
            for tool, stats in self.tool_usage.items():
                avg_duration = stats['total_duration'] / stats['calls'] if stats['calls'] > 0 else 0
                print(f"  • {tool}: {stats['calls']} calls, {avg_duration:.2f}s avg, {stats['errors']} errors")
        
        if self.model_usage:
            print(f"\n🤖 Model Usage:")
            for model, stats in self.model_usage.items():
                print(f"  • {model}: {stats['calls']} calls, {stats['tokens']} tokens, ${stats['cost']:.4f}")


class StreamingCallback(BaseCallbackHandler):
    """
    Callback for streaming responses to user
    """
    
    def __init__(self, stream_to_stdout: bool = True):
        super().__init__()
        self.stream_to_stdout = stream_to_stdout
        self.current_output = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated"""
        if self.stream_to_stdout:
            print(token, end="", flush=True)
        self.current_output += token


class DebugCallback(BaseCallbackHandler):
    """
    Callback for detailed debugging information
    """
    
    def __init__(self, verbose: bool = True):
        super().__init__()
        self.verbose = verbose
    
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs) -> None:
        if self.verbose:
            print(f"🔗 Chain started: {serialized.get('name', 'Unknown')}")
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        if self.verbose:
            print(f"🤖 LLM call started (prompts: {len(prompts)})")
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        if self.verbose:
            tool_name = serialized.get("name", "Unknown")
            print(f"🔧 Tool started: {tool_name}")


# Test function
def test_callbacks():
    """Test callback functionality"""
    print("📊 Testing Callbacks...")
    
    callback = CostLatencyCallback(log_file="test_metrics.json", session_id="test_session")
    
    # Simulate some events
    callback.on_chain_start({"name": "test_chain"}, {"input": "test"})
    time.sleep(0.1)
    
    callback.on_llm_start({"name": "claude"}, ["Test prompt"])
    time.sleep(0.2)
    
    # Mock LLM result
    from langchain.schema import LLMResult, Generation
    result = LLMResult(generations=[[Generation(text="Test response")]])
    callback.on_llm_end(result)
    
    callback.on_tool_start({"name": "test_tool"}, "test input")
    time.sleep(0.1)
    callback.on_tool_end("test output")
    
    callback.on_chain_end({"output": "test result"})
    
    # Print summary
    callback.print_summary()
    
    print("\n✅ Callback test completed")


if __name__ == "__main__":
    test_callbacks()