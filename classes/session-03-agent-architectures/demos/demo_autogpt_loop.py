#!/usr/bin/env python3
"""
Auto-GPT Style Loop Demo
Demonstrates perpetual task execution with memory and goal assessment

⚠️  WARNING: This pattern can be expensive! Use with cost limits.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"
    python demo_autogpt_loop.py "Research and summarize the latest trends in AI agent development"
"""

import sys
import os
import time
import json
from typing import Dict, List
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs.agent_skeleton.tools import TOOLS
from langchain_anthropic import ChatAnthropic


class AutoGPTStyleAgent:
    """
    Demonstrates Auto-GPT style perpetual execution loop
    
    Components:
    - Task generation based on current state
    - Memory of all previous actions
    - Goal assessment after each iteration
    - Safety limits to prevent runaway costs
    """
    
    def __init__(self, cost_limit: float = 0.10, max_iterations: int = 5):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",  # Use cheapest model
            temperature=0.3
        )
        self.tools = {tool.name: tool for tool in TOOLS}
        
        # Safety limits
        self.cost_limit = cost_limit
        self.max_iterations = max_iterations
        self.estimated_cost = 0.0
        
        # Memory storage
        self.memory = {
            "goal": "",
            "actions_taken": [],
            "facts_learned": {},
            "current_state": "initialized"
        }
    
    def estimate_cost(self, text: str) -> float:
        """
        Rough cost estimation (tokens * price per token)
        Using Haiku pricing: ~$0.25 per 1M input tokens
        """
        # Rough approximation: 1 token ≈ 4 characters
        tokens = len(text) // 4
        cost_per_token = 0.25 / 1_000_000  # Haiku input pricing
        return tokens * cost_per_token
    
    def assess_goal_progress(self, goal: str) -> Dict:
        """
        Assess whether the goal has been achieved based on current memory
        """
        print("🎯 GOAL ASSESSMENT: Checking progress...")
        
        context = self._build_context_summary()
        
        assessment_prompt = f"""
Goal: {goal}

Current State:
{context}

Assess the goal completion:
1. What percentage is complete? (0-100)
2. Is the goal fully achieved? (true/false)
3. What key information is still missing?
4. What should be the next priority action?

Return JSON:
{{"completion_percentage": 0-100, "goal_achieved": true/false, "missing_info": "description", "next_priority": "suggested action"}}
"""
        
        messages = [{"role": "user", "content": assessment_prompt}]
        response = self.llm.invoke(messages)
        
        # Update cost estimate
        self.estimated_cost += self.estimate_cost(assessment_prompt + response.content)
        
        try:
            response_text = response.content
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0]
            else:
                json_text = response_text
            
            assessment = json.loads(json_text)
            
            print(f"   Progress: {assessment.get('completion_percentage', 0)}%")
            print(f"   Goal Achieved: {'✅ YES' if assessment.get('goal_achieved') else '❌ NO'}")
            print(f"   Missing: {assessment.get('missing_info', 'Unknown')}")
            print(f"   Next Priority: {assessment.get('next_priority', 'Continue')}")
            print()
            
            return assessment
            
        except (json.JSONDecodeError, KeyError):
            print("⚠️  Assessment parsing failed")
            return {
                "completion_percentage": 25,
                "goal_achieved": False,
                "missing_info": "Unable to assess progress",
                "next_priority": "Gather more information"
            }
    
    def generate_next_task(self, goal: str, assessment: Dict) -> str:
        """
        Generate the next task to work on based on goal and current state
        """
        print("📝 TASK GENERATION: Planning next action...")
        
        context = self._build_context_summary()
        
        task_prompt = f"""
Goal: {goal}

Current Progress: {assessment.get('completion_percentage', 0)}%
Missing Information: {assessment.get('missing_info', 'Unknown')}
Suggested Priority: {assessment.get('next_priority', 'Continue')}

Context:
{context}

Generate the single most important task to do next. Make it:
- Specific and actionable
- Achievable with available tools (web_search, calculator, current_date)
- Different from recent actions to avoid loops

Return just the task description, no extra text.
"""
        
        messages = [{"role": "user", "content": task_prompt}]
        response = self.llm.invoke(messages)
        
        # Update cost estimate
        self.estimated_cost += self.estimate_cost(task_prompt + response.content)
        
        task = response.content.strip()
        print(f"   Generated Task: {task}")
        print()
        
        return task
    
    def execute_task(self, task: str) -> Dict:
        """
        Execute a task using available tools
        """
        print(f"⚡ TASK EXECUTION: {task}")
        
        # Simple tool selection logic
        task_lower = task.lower()
        
        try:
            if any(keyword in task_lower for keyword in ["search", "find", "research", "look up"]):
                tool = self.tools["web_search"]
                result = tool.func(task)
                
            elif any(keyword in task_lower for keyword in ["calculate", "compute", "math"]):
                tool = self.tools["calculator"]
                result = tool.func(task)
                
            elif any(keyword in task_lower for keyword in ["date", "time", "current"]):
                tool = self.tools["current_date"]
                result = tool.func(task)
                
            else:
                # Default to search
                tool = self.tools["web_search"]
                result = tool.func(task)
            
            print(f"   Tool: {tool.name}")
            print(f"   Result: {result[:150]}{'...' if len(result) > 150 else ''}")
            print()
            
            execution_result = {
                "task": task,
                "tool_used": tool.name,
                "result": result,
                "success": True,
                "timestamp": time.time()
            }
            
            # Store in memory
            self.memory["actions_taken"].append(execution_result)
            
            return execution_result
            
        except Exception as e:
            print(f"   ❌ Execution failed: {str(e)}")
            
            execution_result = {
                "task": task,
                "tool_used": None,
                "result": f"Error: {str(e)}",
                "success": False,
                "timestamp": time.time()
            }
            
            self.memory["actions_taken"].append(execution_result)
            return execution_result
    
    def _build_context_summary(self) -> str:
        """
        Build a summary of current state for prompt context
        """
        actions = self.memory["actions_taken"]
        
        if not actions:
            return "No actions taken yet."
        
        summary_parts = []
        summary_parts.append(f"Actions completed: {len(actions)}")
        
        # Recent actions
        recent_actions = actions[-3:]  # Last 3 actions
        for i, action in enumerate(recent_actions, 1):
            status = "✅" if action["success"] else "❌"
            summary_parts.append(f"{status} {action['task'][:50]}...")
        
        # Key facts learned
        if self.memory["facts_learned"]:
            summary_parts.append("Key facts:")
            for key, value in list(self.memory["facts_learned"].items())[:3]:
                summary_parts.append(f"  • {key}: {value}")
        
        return "\n".join(summary_parts)
    
    def run_autonomous_loop(self, goal: str) -> Dict:
        """
        Run the main Auto-GPT style loop
        """
        print("🤖 Auto-GPT Style Agent Starting")
        print("=" * 50)
        print(f"Goal: {goal}")
        print(f"Safety Limits: {self.max_iterations} iterations, ${self.cost_limit:.2f} budget")
        print()
        
        self.memory["goal"] = goal
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"🔄 ITERATION {iteration}")
            print("-" * 30)
            
            # Check cost limit
            if self.estimated_cost > self.cost_limit:
                print(f"💰 COST LIMIT REACHED: ${self.estimated_cost:.4f} > ${self.cost_limit:.2f}")
                print("   Stopping to prevent overcharges")
                break
            
            # 1. Assess current progress toward goal
            assessment = self.assess_goal_progress(goal)
            
            # 2. Check if goal is achieved
            if assessment.get("goal_achieved", False):
                print("🎉 GOAL ACHIEVED! Stopping loop.")
                break
            
            # 3. Generate next task
            next_task = self.generate_next_task(goal, assessment)
            
            # 4. Execute the task
            execution_result = self.execute_task(next_task)
            
            # 5. Update memory with any new facts
            if execution_result["success"]:
                # Simple fact extraction (in real implementation, this would be more sophisticated)
                key = f"result_{iteration}"
                self.memory["facts_learned"][key] = execution_result["result"][:100]
            
            print(f"💰 Estimated cost so far: ${self.estimated_cost:.4f}")
            print()
            
            # Small delay to prevent overwhelming APIs
            time.sleep(1)
        
        # Final summary
        final_assessment = self.assess_goal_progress(goal)
        
        return {
            "goal": goal,
            "iterations": iteration,
            "final_assessment": final_assessment,
            "total_actions": len(self.memory["actions_taken"]),
            "estimated_cost": self.estimated_cost,
            "memory": self.memory,
            "completed": final_assessment.get("goal_achieved", False)
        }


def demonstrate_autogpt_risks():
    """
    Explain the risks and benefits of Auto-GPT style loops
    """
    print("⚠️  Auto-GPT Loop: Benefits and Risks")
    print("=" * 45)
    print()
    print("✅ BENEFITS:")
    print("   • Fully autonomous operation")
    print("   • Can handle complex, multi-step goals")
    print("   • Maintains memory across iterations")
    print("   • Adaptive - changes strategy based on results")
    print()
    print("❌ RISKS:")
    print("   • Unbounded token/cost consumption")
    print("   • Can get stuck in loops")
    print("   • May pursue tangents unrelated to goal")
    print("   • Requires careful safety limits")
    print()
    print("🛡️  SAFETY MEASURES:")
    print("   • Max iteration limits")
    print("   • Cost/budget limits")
    print("   • Human-in-the-loop checkpoints")
    print("   • Timeout protection")
    print()
    print("🎯 BEST USE CASES:")
    print("   • Research and information gathering")
    print("   • Exploratory data analysis")
    print("   • Content creation workflows")
    print("   • Personal assistant tasks")
    print()


def main():
    """Main demo function"""
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable required!")
        print("Get your key from: https://console.anthropic.com")
        sys.exit(1)
    
    # Get goal from command line or use default
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
    else:
        goal = "Research and summarize the latest trends in AI agent development"
        print(f"No goal provided, using default: {goal}")
    
    # Show educational content
    demonstrate_autogpt_risks()
    
    # Confirm user wants to proceed (since this can cost money)
    print(f"🎯 Goal: {goal}")
    print("💰 This demo may cost ~$0.05-0.10 in API calls")
    
    try:
        confirmation = input("Continue? (y/N): ").lower().strip()
        if confirmation != 'y':
            print("Demo cancelled.")
            return
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
        return
    
    # Run the demo
    try:
        agent = AutoGPTStyleAgent(cost_limit=0.10, max_iterations=5)
        result = agent.run_autonomous_loop(goal)
        
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("-" * 30)
        print(f"Goal: {result['goal']}")
        print(f"Iterations completed: {result['iterations']}")
        print(f"Total actions taken: {result['total_actions']}")
        print(f"Estimated cost: ${result['estimated_cost']:.4f}")
        print(f"Goal achieved: {'✅ YES' if result['completed'] else '❌ NO'}")
        
        if result['final_assessment']:
            print(f"Final progress: {result['final_assessment'].get('completion_percentage', 0)}%")
        
        print("\n💡 Key Insights:")
        print("   • Auto-GPT can be powerful but needs careful limits")
        print("   • Memory accumulation is crucial for complex goals")
        print("   • Cost monitoring is essential for production use")
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")


if __name__ == "__main__":
    main()