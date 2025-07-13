#!/usr/bin/env python3
"""
Agent Driver - Main entry point for running your ReAct agent

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"
    python driver.py "What is the square root of the population of Berlin?"
    python driver.py "Who won the 2022 World Cup?"
    python driver.py "What is 25 * 17?"

Students edit this file to:
1. Add memory integration (later sessions)
2. Customize agent behavior
3. Add cost tracking and limits
4. Implement reflection/retry logic
"""

import sys
import time
from tools import TOOLS
from agent_core import build_agent


def run_query(question: str, verbose: bool = True) -> dict:
    """
    Run a single query through the agent
    
    Args:
        question: User's question to answer
        verbose: Whether to show agent's thinking process
        
    Returns:
        Dict with result and metadata
    """
    
    # 🚀 STUDENT TODO: Add cost tracking here
    # Example: start_cost = track_cost()
    
    start_time = time.time()
    
    try:
        # Build the agent with available tools
        agent = build_agent(TOOLS, verbose=verbose)
        
        print(f"🤖 Processing: {question}")
        print("=" * 60)
        
        # Run the query
        result = agent.invoke({"input": question})
        
        runtime = time.time() - start_time
        
        # 🚀 STUDENT TODO: Calculate costs here  
        # Example: total_cost = track_cost() - start_cost
        
        return {
            "question": question,
            "answer": result["output"],
            "runtime": runtime,
            "success": True
            # "cost": total_cost  # TODO: Add this
        }
        
    except Exception as e:
        runtime = time.time() - start_time
        return {
            "question": question,
            "error": str(e),
            "runtime": runtime,
            "success": False
        }


def main():
    """Main entry point"""
    
    # Check for question in command line args
    if len(sys.argv) < 2:
        print("Usage: python driver.py \"Your question here\"")
        print("\nExample questions to try:")
        print("  python driver.py \"What is 15 * 23?\"")
        print("  python driver.py \"What is the capital of France?\"")
        print("  python driver.py \"What is the square root of 100?\"")
        print("  python driver.py \"What is the square root of the population of Berlin?\"")
        sys.exit(1)
    
    # Get question from command line
    question = " ".join(sys.argv[1:])
    
    # Check for API key
    import os
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set!")
        print("Get your key from: https://console.anthropic.com")
        print("Set it with: export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
        sys.exit(1)
    
    # Run the query
    result = run_query(question)
    
    # Print results
    print("\n" + "=" * 60)
    if result["success"]:
        print(f"🎯 FINAL ANSWER:")
        print(f"{result['answer']}")
        print(f"\n⏱️  Runtime: {result['runtime']:.2f} seconds")
        # print(f"💰 Cost: ${result['cost']:.4f}")  # TODO: Uncomment when cost tracking added
    else:
        print(f"❌ ERROR: {result['error']}")
        print(f"⏱️  Runtime: {result['runtime']:.2f} seconds")
    
    print("=" * 60)


# 🚀 STUDENT TODO: Add these functions in future sessions

def add_memory_integration():
    """TODO: Add conversation memory in Session 4"""
    pass

def add_reflection_loop():
    """TODO: Add reflection/retry logic in Session 5"""
    pass

def add_cost_tracking():
    """TODO: Add cost monitoring and limits"""
    pass


if __name__ == "__main__":
    main()