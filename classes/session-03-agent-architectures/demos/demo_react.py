#!/usr/bin/env python3
"""
ReAct Pattern Demo
Live demonstration of ReAct (Reasoning + Acting) pattern in action

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"
    python demo_react.py "What's the square root of Tokyo's population?"
    python demo_react.py "What is 15 * 23 + the current year?"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs.agent_skeleton.tools import TOOLS
from labs.agent_skeleton.agent_core import build_agent


def demonstrate_react_pattern(question: str):
    """
    Demonstrate the ReAct pattern with detailed explanation
    """
    print("🎭 ReAct Pattern Demonstration")
    print("=" * 60)
    print(f"Question: {question}")
    print("\nReAct = Reasoning + Acting")
    print("Watch the agent cycle through: Thought → Action → Observation\n")
    
    try:
        # Build agent with verbose output
        agent = build_agent(TOOLS, verbose=True)
        
        print("🚀 Starting ReAct process...\n")
        
        # Run the query
        result = agent.invoke({"input": question})
        
        print("\n" + "=" * 60)
        print("🎯 FINAL RESULT:")
        print(result["output"])
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def explain_react_components():
    """
    Explain what happens in each ReAct step
    """
    print("\n📚 Understanding ReAct Components:")
    print("-" * 40)
    
    print("🤔 THOUGHT:")
    print("   The agent reasons about what to do next")
    print("   'I need to find Tokyo's population first'")
    
    print("\n⚡ ACTION:")  
    print("   The agent chooses a tool to use")
    print("   'web_search' or 'calculator'")
    
    print("\n👁️  OBSERVATION:")
    print("   The agent sees the tool's result")
    print("   'Tokyo has 37.4 million people'")
    
    print("\n🔄 LOOP:")
    print("   Repeat until goal is achieved")
    print("   Then provide Final Answer\n")


def show_example_traces():
    """
    Show example ReAct traces for different question types
    """
    print("📝 Example ReAct Traces:")
    print("-" * 40)
    
    print("\n🔢 Math Question: 'What is 25 + 17?'")
    print("   Thought: This is a simple math problem")
    print("   Action: calculator")
    print("   Action Input: 25 + 17")  
    print("   Observation: 25 + 17 = 42")
    print("   Thought: I have the answer")
    print("   Final Answer: 42")
    
    print("\n🌍 Factual Question: 'Who won the 2022 World Cup?'")
    print("   Thought: I need to search for recent World Cup information")
    print("   Action: web_search")
    print("   Action Input: 2022 World Cup winner")
    print("   Observation: Argentina won the 2022 FIFA World Cup...")
    print("   Thought: I found the answer")
    print("   Final Answer: Argentina won the 2022 World Cup")
    
    print("\n🧮 Complex Question: 'Square root of Berlin population?'")
    print("   Thought: I need population data first")
    print("   Action: web_search")
    print("   Action Input: Berlin population 2024")
    print("   Observation: Berlin has approximately 3.7 million...")
    print("   Thought: Now I need to calculate square root")
    print("   Action: calculator") 
    print("   Action Input: sqrt(3700000)")
    print("   Observation: √3700000.0 = 1924.50")
    print("   Thought: I have the final answer")
    print("   Final Answer: The square root is approximately 1,924")


def main():
    """Main demo function"""
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable required!")
        print("Get your key from: https://console.anthropic.com")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
        sys.exit(1)
    
    # Get question from command line or use default
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "What's the square root of Tokyo's population?"
        print(f"No question provided, using default: {question}")
    
    # Show educational content first
    explain_react_components()
    show_example_traces()
    
    print("\n" + "=" * 60)
    print("🎬 LIVE DEMO TIME!")
    
    # Run the actual demo
    result = demonstrate_react_pattern(question)
    
    if result:
        print("\n✅ Demo completed successfully!")
        print("\n💡 Key Takeaways:")
        print("   • ReAct combines reasoning with tool use")
        print("   • Each step builds on the previous observation") 
        print("   • Agent stops when it has enough information")
        print("   • Verbose mode shows the thinking process")
    else:
        print("\n❌ Demo failed - check your setup")


if __name__ == "__main__":
    main()