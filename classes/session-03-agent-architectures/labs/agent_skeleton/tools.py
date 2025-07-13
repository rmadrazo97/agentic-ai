"""
Agent Tools - Search and Math capabilities
Students extend this file to add custom tools for their projects
"""

from langchain.tools import Tool
from typing import List
import math
import re
import requests
from duckduckgo_search import DDGS


def web_search_tool(query: str) -> str:
    """
    Search the web using DuckDuckGo
    
    Args:
        query: Search terms to look for
        
    Returns:
        String with search results summary
    """
    try:
        # Use DuckDuckGo search (no API key required)
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        if not results:
            return f"No search results found for: {query}"
        
        # Format results
        formatted_results = []
        for i, result in enumerate(results[:3], 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description')
            # Truncate long snippets
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            formatted_results.append(f"{i}. {title}: {snippet}")
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"Search error: {str(e)}. Try rephrasing your query."


def math_calculator_tool(expression: str) -> str:
    """
    Safe calculator for mathematical expressions
    
    Args:
        expression: Math expression to evaluate (supports +, -, *, /, sqrt, etc.)
        
    Returns:
        String with calculation result
    """
    try:
        # Clean the expression
        expression = expression.strip()
        
        # Handle square root specially
        if "sqrt" in expression.lower():
            # Extract number from expressions like "sqrt(3700000)" or "sqrt 3700000"
            match = re.search(r'sqrt\s*\(?(\d+\.?\d*)\)?', expression.lower())
            if match:
                number = float(match.group(1))
                result = math.sqrt(number)
                return f"√{number} = {result:.2f}"
        
        # Handle basic arithmetic (safe eval with whitelist)
        allowed_chars = set('0123456789+-*/.() ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"{expression} = {result}"
        else:
            return "Error: Only basic math operations (+, -, *, /, sqrt) are supported"
            
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Math error: {str(e)}. Please check your expression."


def get_current_date_tool(query: str = "") -> str:
    """
    Get current date and time information
    
    Args:
        query: Optional specific date query
        
    Returns:
        Current date/time information
    """
    from datetime import datetime
    
    now = datetime.now()
    
    if "time" in query.lower():
        return f"Current time: {now.strftime('%H:%M:%S')}"
    elif "year" in query.lower():
        return f"Current year: {now.year}"
    else:
        return f"Current date: {now.strftime('%Y-%m-%d')} (Time: {now.strftime('%H:%M')})"


# Define the tools that will be available to the agent
TOOLS = [
    Tool.from_function(
        name="web_search",
        description="Search the web for current information. Use this when you need to find facts, news, or recent data about people, places, events, etc.",
        func=web_search_tool
    ),
    Tool.from_function(
        name="calculator", 
        description="Perform mathematical calculations including basic arithmetic (+, -, *, /) and square roots. Examples: '25 + 17', 'sqrt(3700000)', '15 * 23'",
        func=math_calculator_tool
    ),
    Tool.from_function(
        name="current_date",
        description="Get the current date and time. Useful when you need to know what day it is or the current year.",
        func=get_current_date_tool
    )
]


# TODO: Custom Tool Ideas for Your Project
# Students add their ideas here as TODO comments

# Example format:
# TODO: For our [EdTech/FinTech/DevOps/etc.] agent, we need a tool that:
# - Purpose: [What specific task it accomplishes]
# - Input: [What parameters it takes]
# - Output: [What it returns]
# - Implementation: [What API/library/service we'll use]

# TODO: Add your custom tool idea here!
# Delete this line and add your team's tool idea:

"""
Example custom tool ideas by domain:

📚 EDTECH TOOLS:
- quiz_generator: Generate practice questions from text
- grade_calculator: Calculate GPA and grade statistics  
- learning_path: Suggest study sequence for topics

💰 FINTECH TOOLS:
- stock_price: Get current stock prices and market data
- currency_converter: Convert between currencies
- financial_calculator: Calculate loans, investments, etc.

🛠️ DEVOPS TOOLS:
- github_analyzer: Analyze repo statistics and issues
- deploy_status: Check deployment and service health
- log_analyzer: Parse and summarize application logs

🏥 HEALTHTECH TOOLS:
- symptom_checker: Basic health information lookup
- medication_info: Drug interaction and dosage info
- appointment_scheduler: Calendar integration

📈 PRODUCTIVITY TOOLS:
- email_parser: Extract action items from emails
- meeting_summarizer: Summarize meeting transcripts
- task_prioritizer: Sort tasks by urgency/importance
"""


def test_tools():
    """Test all tools to make sure they work"""
    print("🧪 Testing all tools...\n")
    
    # Test search
    print("1. Testing web search...")
    search_result = web_search_tool("Berlin population 2024")
    print(f"Result: {search_result[:100]}...\n")
    
    # Test calculator
    print("2. Testing calculator...")
    calc_result = math_calculator_tool("25 + 17")
    print(f"Result: {calc_result}\n")
    
    # Test sqrt
    print("3. Testing square root...")
    sqrt_result = math_calculator_tool("sqrt(100)")
    print(f"Result: {sqrt_result}\n")
    
    # Test date
    print("4. Testing current date...")
    date_result = get_current_date_tool()
    print(f"Result: {date_result}\n")
    
    print("✅ All tools tested!")


if __name__ == "__main__":
    test_tools()