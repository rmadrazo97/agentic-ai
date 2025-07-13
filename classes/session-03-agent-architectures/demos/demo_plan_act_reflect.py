#!/usr/bin/env python3
"""
Plan-Act-Reflect Pattern Demo
Demonstrates three-role architecture: Planner → Executor → Critic

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key-here"
    python demo_plan_act_reflect.py "Calculate the average population of the top 3 largest cities in Europe"
"""

import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs.agent_skeleton.tools import TOOLS
from langchain_anthropic import ChatAnthropic


class PlanActReflectAgent:
    """
    Demonstrates Plan-Act-Reflect architecture with three distinct roles
    """
    
    def __init__(self):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=0.1
        )
        self.tools = {tool.name: tool for tool in TOOLS}
    
    def plan(self, goal: str) -> list:
        """
        PLANNER ROLE: Create a step-by-step plan to achieve the goal
        """
        print("📋 PLANNER ROLE: Creating execution plan...")
        
        planning_prompt = f"""
You are a strategic planner. Break down this goal into clear, executable steps.

Goal: {goal}

Create a numbered plan with specific, actionable steps. Each step should be something that can be executed with available tools (web_search, calculator, current_date).

Return your plan as a JSON list of steps:
{{"steps": ["step 1 description", "step 2 description", ...]}}

Make each step specific and focused on a single action.
"""
        
        messages = [{"role": "user", "content": planning_prompt}]
        response = self.llm.invoke(messages)
        
        try:
            # Extract JSON from response
            response_text = response.content
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0]
            else:
                json_text = response_text
            
            plan_data = json.loads(json_text)
            steps = plan_data.get("steps", [])
            
            print("Generated Plan:")
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step}")
            print()
            
            return steps
            
        except (json.JSONDecodeError, KeyError):
            # Fallback to manual parsing
            print("⚠️  JSON parsing failed, using fallback plan")
            return [
                "Search for information about the largest cities in Europe",
                "Extract population data for the top 3 cities",
                "Calculate the average of these three populations"
            ]
    
    def execute_step(self, step: str, step_number: int) -> dict:
        """
        EXECUTOR ROLE: Execute a single step using available tools
        """
        print(f"⚡ EXECUTOR ROLE: Executing step {step_number}")
        print(f"   Task: {step}")
        
        # Use simple reasoning to choose appropriate tool
        step_lower = step.lower()
        
        try:
            if any(keyword in step_lower for keyword in ["search", "find", "look up", "information about"]):
                # Use web search
                tool = self.tools["web_search"]
                result = tool.func(step)
                
            elif any(keyword in step_lower for keyword in ["calculate", "average", "math", "sum"]):
                # Use calculator
                tool = self.tools["calculator"]
                # Extract math expression or use step as-is
                result = tool.func(step)
                
            elif any(keyword in step_lower for keyword in ["date", "time", "current", "today"]):
                # Use date tool
                tool = self.tools["current_date"]
                result = tool.func(step)
                
            else:
                # Default to search for factual information
                tool = self.tools["web_search"]
                result = tool.func(step)
            
            print(f"   Tool used: {tool.name}")
            print(f"   Result: {result[:200]}{'...' if len(result) > 200 else ''}")
            print()
            
            return {
                "step": step,
                "tool_used": tool.name,
                "result": result,
                "success": True
            }
            
        except Exception as e:
            print(f"   ❌ Execution failed: {str(e)}")
            return {
                "step": step,
                "tool_used": None,
                "result": f"Error: {str(e)}",
                "success": False
            }
    
    def reflect(self, goal: str, plan: list, execution_results: list) -> dict:
        """
        CRITIC ROLE: Evaluate results and determine if goal was achieved
        """
        print("🎯 CRITIC ROLE: Evaluating results...")
        
        # Prepare execution summary
        results_summary = []
        for i, result in enumerate(execution_results, 1):
            status = "✅" if result["success"] else "❌"
            results_summary.append(f"Step {i}: {status} {result['step']}")
            results_summary.append(f"  Result: {result['result'][:100]}...")
        
        reflection_prompt = f"""
You are a critical evaluator. Assess whether the goal was successfully achieved.

Goal: {goal}

Planned Steps:
{chr(10).join([f"{i}. {step}" for i, step in enumerate(plan, 1)])}

Execution Results:
{chr(10).join(results_summary)}

Evaluate:
1. Was the goal achieved? (YES/NO)
2. What information is missing or incorrect?
3. What should be done differently?

Provide your assessment as JSON:
{{"goal_achieved": true/false, "confidence": 0-100, "missing_info": "description", "recommendations": "suggestions"}}
"""
        
        messages = [{"role": "user", "content": reflection_prompt}]
        response = self.llm.invoke(messages)
        
        try:
            response_text = response.content
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0]
            else:
                json_text = response_text
            
            reflection = json.loads(json_text)
            
            print("Reflection Results:")
            print(f"  Goal Achieved: {'✅ YES' if reflection.get('goal_achieved') else '❌ NO'}")
            print(f"  Confidence: {reflection.get('confidence', 'N/A')}%")
            print(f"  Missing Info: {reflection.get('missing_info', 'None')}")
            print(f"  Recommendations: {reflection.get('recommendations', 'None')}")
            print()
            
            return reflection
            
        except (json.JSONDecodeError, KeyError):
            print("⚠️  Reflection parsing failed, using default assessment")
            return {
                "goal_achieved": False,
                "confidence": 50,
                "missing_info": "Unable to properly evaluate results",
                "recommendations": "Retry with simpler steps"
            }
    
    def run(self, goal: str, max_iterations: int = 2) -> dict:
        """
        Run the complete Plan-Act-Reflect cycle
        """
        print("🏗️  Starting Plan-Act-Reflect Process")
        print("=" * 60)
        print(f"Goal: {goal}\n")
        
        for iteration in range(max_iterations):
            print(f"🔄 ITERATION {iteration + 1}")
            print("-" * 30)
            
            # 1. PLAN
            plan = self.plan(goal)
            
            # 2. ACT (Execute each step)
            execution_results = []
            for i, step in enumerate(plan):
                result = self.execute_step(step, i + 1)
                execution_results.append(result)
            
            # 3. REFLECT
            reflection = self.reflect(goal, plan, execution_results)
            
            # Check if goal achieved
            if reflection.get("goal_achieved", False):
                print("🎉 SUCCESS: Goal achieved!")
                break
            else:
                print("⚠️  Goal not fully achieved, would retry with revised plan...")
                if iteration < max_iterations - 1:
                    print("   (In a real implementation, we'd revise the plan based on reflection)")
        
        return {
            "goal": goal,
            "final_plan": plan,
            "execution_results": execution_results,
            "reflection": reflection,
            "iterations": iteration + 1
        }


def demonstrate_architecture():
    """
    Show the three-role architecture conceptually
    """
    print("🏗️  Plan-Act-Reflect Architecture")
    print("=" * 50)
    print()
    print("📋 PLANNER:")
    print("   • Breaks down complex goals into steps")
    print("   • Creates detailed execution plan")
    print("   • Considers available tools and constraints")
    print()
    print("⚡ EXECUTOR:")
    print("   • Carries out each step in the plan")
    print("   • Uses appropriate tools for each task")
    print("   • Records results and any errors")
    print()
    print("🎯 CRITIC:")
    print("   • Evaluates whether goal was achieved")
    print("   • Identifies missing or incorrect information")
    print("   • Suggests improvements for next iteration")
    print()
    print("🔄 WORKFLOW:")
    print("   Goal → Plan → Execute → Reflect → (Revise if needed)")
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
        goal = "Calculate the average population of the top 3 largest cities in Europe"
        print(f"No goal provided, using default: {goal}")
    
    # Show architecture explanation
    demonstrate_architecture()
    
    # Run the demo
    try:
        agent = PlanActReflectAgent()
        result = agent.run(goal)
        
        print("\n" + "=" * 60)
        print("📊 FINAL SUMMARY")
        print("-" * 30)
        print(f"Goal: {result['goal']}")
        print(f"Iterations: {result['iterations']}")
        print(f"Steps in final plan: {len(result['final_plan'])}")
        
        success_rate = sum(1 for r in result['execution_results'] if r['success']) / len(result['execution_results'])
        print(f"Execution success rate: {success_rate:.1%}")
        
        if result['reflection']['goal_achieved']:
            print("✅ Goal achieved successfully!")
        else:
            print("⚠️  Goal partially achieved - would need more iterations")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")


if __name__ == "__main__":
    main()