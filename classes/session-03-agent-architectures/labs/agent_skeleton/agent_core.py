"""
ReAct Agent Core - LangChain + Anthropic Claude integration
Provides a simple wrapper for creating ReAct agents with tools
"""

from typing import List
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub
import os


def build_agent(tools: List[Tool], model_name: str = "claude-3-haiku-20240307", verbose: bool = True) -> AgentExecutor:
    """
    Build a ReAct agent with the provided tools
    
    Args:
        tools: List of LangChain tools to give the agent
        model_name: Claude model to use (haiku recommended for cost)
        verbose: Whether to show thinking process
        
    Returns:
        AgentExecutor ready to run queries
    """
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable required.\n"
            "Get your key from: https://console.anthropic.com\n"
            "Set it with: export ANTHROPIC_API_KEY='sk-ant-...'"
        )
    
    # Initialize Claude LLM
    llm = ChatAnthropic(
        model_name=model_name,
        temperature=0,  # Deterministic for better tool use
        max_tokens=1000  # Reasonable limit
    )
    
    # Get ReAct prompt template from LangChain hub
    try:
        prompt = hub.pull("hwchase17/react")  # Standard ReAct template
    except Exception:
        # Fallback prompt if hub is unavailable
        prompt = create_fallback_react_prompt()
    
    # Create the ReAct agent
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Wrap in executor with safety limits
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        max_iterations=10,  # Prevent infinite loops
        max_execution_time=60,  # 60 second timeout
        early_stopping_method="generate",  # Stop on final answer
        handle_parsing_errors=True  # Graceful error handling
    )
    
    return agent_executor


def create_fallback_react_prompt():
    """
    Create a fallback ReAct prompt template if LangChain hub is unavailable
    """
    from langchain.prompts import PromptTemplate
    
    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
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
            "tools": "{tools}",
            "tool_names": "{tool_names}"
        }
    )


def test_agent_setup():
    """
    Quick test to verify agent setup works
    """
    from tools import TOOLS
    
    try:
        agent = build_agent(TOOLS)
        print("✅ Agent setup successful!")
        print(f"Available tools: {[tool.name for tool in TOOLS]}")
        return True
    except Exception as e:
        print(f"❌ Agent setup failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Quick test when run directly
    test_agent_setup()