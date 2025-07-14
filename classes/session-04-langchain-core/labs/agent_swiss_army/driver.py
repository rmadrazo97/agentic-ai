#!/usr/bin/env python3
"""
Swiss Army Agent Driver - Production-ready LangChain agent with tools, memory, and callbacks

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key"
    export TAVILY_API_KEY="tvly-your-key"  # Optional for web search
    
    python driver.py "Search for Python jobs and create a summary table"
    python driver.py --interactive  # Interactive mode
    python driver.py --test         # Run test suite

Features:
- Multi-tool agent (search, compute, data, communication)
- Conversation memory with summarization
- Cost and performance tracking
- Extensible chain composition
"""

import os
import sys
import argparse
from typing import Dict, Any
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chains import swiss_army_chain, RouterChain
from tools import ALL_TOOLS, print_tool_stats
from memory import MemoryManager
from callbacks import CostLatencyCallback


class SwissArmyDriver:
    """
    Main driver for the Swiss Army Agent with enhanced features
    """
    
    def __init__(self, session_id: str = "default", verbose: bool = True):
        self.session_id = session_id
        self.verbose = verbose
        
        # Check for required API keys
        self._check_api_keys()
        
        # Initialize the agent chain
        self.chain = swiss_army_chain()
        
        # Initialize router for complex routing
        self.router = RouterChain()
        
        print(f"🤖 Swiss Army Agent initialized (Session: {session_id})")
        if verbose:
            print_tool_stats()
    
    def _check_api_keys(self):
        """Check for required API keys and provide helpful messages"""
        required_keys = {
            "ANTHROPIC_API_KEY": "Required for Claude LLM. Get from: https://console.anthropic.com"
        }
        
        optional_keys = {
            "TAVILY_API_KEY": "Optional for web search. Get from: https://tavily.com",
            "REDIS_URL": "Optional for persistent memory. Format: redis://localhost:6379"
        }
        
        missing_required = []
        for key, description in required_keys.items():
            if not os.getenv(key):
                missing_required.append(f"❌ {key}: {description}")
        
        if missing_required:
            print("Missing required API keys:")
            for msg in missing_required:
                print(f"  {msg}")
            sys.exit(1)
        
        # Show optional key status
        if self.verbose:
            print("🔑 API Key Status:")
            for key, description in {**required_keys, **optional_keys}.items():
                status = "✅" if os.getenv(key) else "⚠️ "
                print(f"  {status} {key}")
    
    def run_query(self, user_input: str, use_router: bool = False) -> Dict[str, Any]:
        """
        Run a single query through the agent
        
        Args:
            user_input: User's question or request
            use_router: Whether to use intelligent routing
            
        Returns:
            Result dictionary with output and metadata
        """
        try:
            if use_router:
                print("🧠 Using intelligent router...")
                result = self.router.run(user_input)
            else:
                result = self.chain.run(user_input)
            
            return result
            
        except KeyboardInterrupt:
            return {
                "output": "Query interrupted by user",
                "interrupted": True
            }
        except Exception as e:
            return {
                "output": f"Error processing query: {str(e)}",
                "error": str(e)
            }
    
    def interactive_mode(self):
        """
        Run in interactive mode for ongoing conversation
        """
        print("\n🎯 Interactive Mode Started")
        print("Type 'quit', 'exit', or press Ctrl+C to stop")
        print("Type 'help' for available commands")
        print("Type 'stats' to see session statistics")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💭 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                elif user_input.lower() == 'stats':
                    self._show_stats()
                    continue
                elif user_input.lower() == 'clear':
                    self.chain.clear_memory()
                    print("🧠 Memory cleared")
                    continue
                elif user_input.lower() == 'tools':
                    print_tool_stats()
                    continue
                
                # Process the query
                print("\n🤖 Agent: ", end="", flush=True)
                result = self.run_query(user_input)
                
                if "error" in result:
                    print(f"❌ {result['output']}")
                else:
                    print(result['output'])
                
            except KeyboardInterrupt:
                print("\n\n👋 Session ended by user")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {str(e)}")
        
        # Show final stats
        self._show_final_stats()
    
    def _show_help(self):
        """Show help information"""
        print("""
🔧 Available Commands:
  help     - Show this help message
  stats    - Show session statistics
  tools    - Show available tools
  clear    - Clear conversation memory
  quit/exit - End session

🎯 Example Queries:
  • "Search for the latest Python news"
  • "Calculate the square root of 12345"
  • "Create a CSV with sample data"
  • "My name is Alice" (memory test)
  • "What's my name?" (memory recall)
  • "Search for Python jobs, analyze the data, and save as CSV"
        """)
    
    def _show_stats(self):
        """Show current session statistics"""
        cost_summary = self.chain.get_cost_summary()
        memory_summary = self.chain.get_memory_summary()
        
        print(f"\n📊 Session Statistics:")
        print(f"  💰 Total Cost: ${cost_summary.get('total_cost', 0):.4f}")
        print(f"  ⏱️  Runtime: {cost_summary.get('session_duration', 0):.2f}s")
        print(f"  🤖 LLM Calls: {cost_summary.get('llm_calls', 0)}")
        print(f"  🔧 Tool Calls: {cost_summary.get('tool_calls', 0)}")
        print(f"  🧠 Memory: {memory_summary}")
    
    def _show_final_stats(self):
        """Show final session statistics"""
        print(f"\n📊 Final Session Report:")
        cost_summary = self.chain.get_cost_summary()
        
        print(f"  Session ID: {self.session_id}")
        print(f"  Total Cost: ${cost_summary.get('total_cost', 0):.4f}")
        print(f"  Total Runtime: {cost_summary.get('session_duration', 0):.2f} seconds")
        print(f"  LLM Calls: {cost_summary.get('llm_calls', 0)}")
        print(f"  Tool Calls: {cost_summary.get('tool_calls', 0)}")
        print(f"  Errors: {cost_summary.get('errors', 0)}")
        
        # Save final metrics
        metrics_file = "outputs/final_metrics.json"
        os.makedirs(os.path.dirname(metrics_file), exist_ok=True)
        with open(metrics_file, "w") as f:
            json.dump(cost_summary, f, indent=2)
        
        print(f"  📁 Metrics saved to: {metrics_file}")
    
    def run_test_suite(self):
        """
        Run a comprehensive test suite
        """
        print("🧪 Running Swiss Army Agent Test Suite")
        print("=" * 50)
        
        test_cases = [
            ("Basic Math", "What is 25 + 17?"),
            ("Memory Test 1", "My name is Alice and I'm a developer"),
            ("Memory Test 2", "What's my name and profession?"),
            ("Search Test", "Search for recent AI news"),
            ("Data Processing", "Create a CSV with sample employee data"),
            ("Complex Query", "Search for Python developer jobs, extract the top 3, and create a summary table")
        ]
        
        results = []
        for test_name, query in test_cases:
            print(f"\n🔍 Test: {test_name}")
            print(f"Query: {query}")
            print("-" * 30)
            
            try:
                result = self.run_query(query)
                success = "error" not in result
                
                if success:
                    print("✅ PASSED")
                    print(f"Output: {result['output'][:100]}...")
                else:
                    print("❌ FAILED")
                    print(f"Error: {result.get('error', 'Unknown error')}")
                
                results.append({
                    "test": test_name,
                    "query": query,
                    "success": success,
                    "output": result['output'][:200] + "..." if len(result['output']) > 200 else result['output']
                })
                
            except Exception as e:
                print(f"❌ FAILED - Exception: {str(e)}")
                results.append({
                    "test": test_name,
                    "query": query,
                    "success": False,
                    "error": str(e)
                })
        
        # Summary
        passed = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"\n📊 Test Results: {passed}/{total} passed ({passed/total*100:.1f}%)")
        
        # Save test results
        test_results_file = "outputs/test_results.json"
        os.makedirs(os.path.dirname(test_results_file), exist_ok=True)
        with open(test_results_file, "w") as f:
            json.dump({
                "summary": {"passed": passed, "total": total, "success_rate": passed/total},
                "results": results
            }, f, indent=2)
        
        print(f"📁 Test results saved to: {test_results_file}")
        
        return passed == total


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Swiss Army Agent - Production LangChain Agent")
    parser.add_argument("query", nargs="*", help="Query to process")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--test", "-t", action="store_true", help="Run test suite")
    parser.add_argument("--session-id", default="default", help="Session ID for memory persistence")
    parser.add_argument("--verbose", "-v", action="store_true", default=True, help="Verbose output")
    parser.add_argument("--router", "-r", action="store_true", help="Use intelligent routing")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode")
    
    args = parser.parse_args()
    
    # Handle quiet mode
    if args.quiet:
        args.verbose = False
    
    # Initialize driver
    driver = SwissArmyDriver(session_id=args.session_id, verbose=args.verbose)
    
    try:
        if args.test:
            # Run test suite
            success = driver.run_test_suite()
            sys.exit(0 if success else 1)
        
        elif args.interactive:
            # Interactive mode
            driver.interactive_mode()
        
        elif args.query:
            # Single query mode
            query = " ".join(args.query)
            print(f"🎯 Processing: {query}")
            print("-" * 50)
            
            result = driver.run_query(query, use_router=args.router)
            
            if "error" in result:
                print(f"❌ Error: {result['output']}")
                sys.exit(1)
            else:
                print(f"🎯 Result:")
                print(result['output'])
                
                # Show cost info if verbose
                if args.verbose and 'cost_info' in result:
                    cost_info = result['cost_info']
                    print(f"\n💰 Cost: ${cost_info.get('total_cost', 0):.4f}")
                    print(f"⏱️  Runtime: {cost_info.get('total_runtime', 0):.2f}s")
        
        else:
            # No arguments - show help
            parser.print_help()
            print("\nExample usage:")
            print('  python driver.py "Search for Python jobs and create a summary"')
            print("  python driver.py --interactive")
            print("  python driver.py --test")
    
    except KeyboardInterrupt:
        print("\n👋 Session interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()