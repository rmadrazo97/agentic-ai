"""
Chain Composition for Swiss Army Agent
Combines agent execution with pre/post processing using LangChain chains
"""

from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.schema.runnable import RunnableSequence, RunnableLambda
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain import hub

from tools import ALL_TOOLS
from memory import build_memory
from callbacks import CostLatencyCallback


class SwissArmyChain:
    """
    Production-grade agent chain with preprocessing, agent execution, and postprocessing
    """
    
    def __init__(self, model_name: str = "claude-3-haiku-20240307", verbose: bool = True):
        self.model_name = model_name
        self.verbose = verbose
        self.llm = ChatAnthropic(
            model_name=model_name,
            temperature=0.1,  # Low temperature for consistent tool use
            timeout=60  # 60 second timeout
        )
        
        # Initialize components
        self.memory = build_memory()
        self.cost_callback = CostLatencyCallback()
        self.agent_executor = self._build_agent_executor()
        self.chain = self._build_chain()
    
    def _build_agent_executor(self) -> AgentExecutor:
        """
        Build the core agent executor with tools and memory
        """
        try:
            # Get ReAct prompt template
            prompt = hub.pull("hwchase17/react")
        except Exception:
            # Fallback prompt if hub is unavailable
            prompt = self._create_fallback_prompt()
        
        # Create ReAct agent
        agent = create_react_agent(
            llm=self.llm,
            tools=ALL_TOOLS,
            prompt=prompt
        )
        
        # Create agent executor with safety limits
        agent_executor = AgentExecutor(
            agent=agent,
            tools=ALL_TOOLS,
            memory=self.memory,
            callbacks=[self.cost_callback],
            verbose=self.verbose,
            max_iterations=8,  # Prevent infinite loops
            max_execution_time=120,  # 2 minute timeout
            early_stopping_method="generate",
            handle_parsing_errors=True,
            return_intermediate_steps=True  # For debugging
        )
        
        return agent_executor
    
    def _create_fallback_prompt(self) -> PromptTemplate:
        """
        Create fallback ReAct prompt if hub is unavailable
        """
        template = """You are a helpful AI assistant with access to various tools. Use the tools provided to answer questions accurately and completely.

Available tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: think about what you need to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        return PromptTemplate(
            template=template,
            input_variables=["input", "agent_scratchpad"],
            partial_variables={
                "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in ALL_TOOLS]),
                "tool_names": ", ".join([tool.name for tool in ALL_TOOLS])
            }
        )
    
    def _preprocess_input(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess input before sending to agent
        """
        user_input = inputs.get("input", "")
        
        # Add context or formatting if needed
        processed_input = user_input.strip()
        
        # Add any global instructions or context
        if len(processed_input) > 1000:
            # Truncate very long inputs
            processed_input = processed_input[:1000] + "... (truncated)"
        
        return {"input": processed_input}
    
    def _postprocess_output(self, outputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Postprocess agent output for final presentation
        """
        # Extract the main output
        final_output = outputs.get("output", "")
        
        # Add any formatting or additional information
        processed_output = final_output
        
        # Add cost information if available
        cost_info = self.cost_callback.get_session_summary()
        if cost_info:
            processed_output += f"\n\n💰 Session Cost: ${cost_info.get('total_cost', 0):.4f}"
            processed_output += f" | ⏱️ Runtime: {cost_info.get('total_runtime', 0):.2f}s"
        
        return {
            "output": processed_output,
            "intermediate_steps": outputs.get("intermediate_steps", []),
            "cost_info": cost_info
        }
    
    def _build_chain(self) -> RunnableSequence:
        """
        Build the complete chain with pre/post processing
        """
        # Create preprocessing step
        preprocess = RunnableLambda(self._preprocess_input)
        
        # Create postprocessing step
        postprocess = RunnableLambda(self._postprocess_output)
        
        # Combine into sequence
        chain = RunnableSequence(
            first=preprocess,
            middle=[self.agent_executor],
            last=postprocess
        )
        
        return chain
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Run the complete chain with input
        
        Args:
            user_input: User's question or request
            
        Returns:
            Dict with output and metadata
        """
        try:
            result = self.chain.invoke({"input": user_input})
            return result
        except Exception as e:
            return {
                "output": f"Error processing request: {str(e)}",
                "error": str(e),
                "cost_info": self.cost_callback.get_session_summary()
            }
    
    def stream(self, user_input: str):
        """
        Stream the chain execution (if supported)
        """
        try:
            for chunk in self.chain.stream({"input": user_input}):
                yield chunk
        except Exception as e:
            yield {"error": str(e)}
    
    def get_memory_summary(self) -> str:
        """
        Get summary of conversation memory
        """
        if hasattr(self.memory, 'chat_memory'):
            messages = self.memory.chat_memory.messages
            return f"Memory contains {len(messages)} messages"
        return "No memory information available"
    
    def clear_memory(self):
        """
        Clear conversation memory
        """
        if hasattr(self.memory, 'clear'):
            self.memory.clear()
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """
        Get cost and performance summary
        """
        return self.cost_callback.get_session_summary()


# Factory functions for different configurations

def create_fast_chain() -> SwissArmyChain:
    """
    Create a fast, cost-optimized chain
    """
    return SwissArmyChain(
        model_name="claude-3-haiku-20240307",  # Fastest, cheapest
        verbose=False  # Reduce output for speed
    )


def create_powerful_chain() -> SwissArmyChain:
    """
    Create a powerful, high-accuracy chain
    """
    return SwissArmyChain(
        model_name="claude-3-sonnet-20240229",  # More powerful
        verbose=True
    )


def create_balanced_chain() -> SwissArmyChain:
    """
    Create a balanced chain (default)
    """
    return SwissArmyChain(
        model_name="claude-3-haiku-20240307",
        verbose=True
    )


# Router chain for intelligent model selection
class RouterChain:
    """
    Routes requests to appropriate model based on complexity
    """
    
    def __init__(self):
        self.fast_chain = create_fast_chain()
        self.powerful_chain = create_powerful_chain()
    
    def _assess_complexity(self, user_input: str) -> str:
        """
        Assess if request is simple or complex
        """
        user_input_lower = user_input.lower()
        
        # Simple request indicators
        simple_indicators = [
            "what is", "calculate", "convert", "define", "search for",
            "find", "lookup", "current", "today", "weather"
        ]
        
        # Complex request indicators
        complex_indicators = [
            "analyze", "compare", "evaluate", "plan", "strategy",
            "create a report", "summarize multiple", "research",
            "write a", "explain why", "pros and cons"
        ]
        
        # Check for complex indicators first
        if any(indicator in user_input_lower for indicator in complex_indicators):
            return "complex"
        
        # Check for simple indicators
        if any(indicator in user_input_lower for indicator in simple_indicators):
            return "simple"
        
        # Default to simple for shorter queries, complex for longer ones
        return "simple" if len(user_input) < 100 else "complex"
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        Route request to appropriate chain
        """
        complexity = self._assess_complexity(user_input)
        
        if complexity == "simple":
            print("🚀 Using fast chain for simple request")
            return self.fast_chain.run(user_input)
        else:
            print("🧠 Using powerful chain for complex request")
            return self.powerful_chain.run(user_input)


# Main interface function
def swiss_army_chain() -> SwissArmyChain:
    """
    Create the default Swiss Army agent chain
    
    Returns:
        Configured SwissArmyChain instance
    """
    return create_balanced_chain()


# Test function
def test_chain():
    """Test the chain functionality"""
    print("⛓️  Testing Swiss Army Chain...")
    
    chain = swiss_army_chain()
    
    # Test simple query
    print("\n1. Testing simple query:")
    result = chain.run("What is 2 + 2?")
    print(f"Output: {result['output']}")
    
    # Test memory
    print("\n2. Testing memory:")
    chain.run("My name is Alice")
    result = chain.run("What's my name?")
    print(f"Output: {result['output']}")
    
    # Test tool usage
    print("\n3. Testing tool usage:")
    result = chain.run("Search for the latest Python news")
    print(f"Output: {result['output'][:200]}...")
    
    print("\n✅ Chain test completed")


if __name__ == "__main__":
    test_chain()