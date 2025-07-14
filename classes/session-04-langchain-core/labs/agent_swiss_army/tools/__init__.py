"""
Tool Registry for Swiss Army Agent
Consolidates all available tools in one place for easy management
"""

from .search import create_search_tool
from .compute import create_python_tool
from .csv_writer import create_csv_tool
from .email import create_email_tool
from .http_tool import create_http_tool

# Import any additional tools here
# from .custom_tool import create_custom_tool


def get_all_tools():
    """
    Get all available tools for the agent
    
    Returns:
        List of LangChain Tool objects
    """
    tools = []
    
    # Core tools (always included)
    tools.extend([
        create_search_tool(),
        create_python_tool(), 
        create_csv_tool(),
    ])
    
    # Optional tools (comment out if not needed)
    try:
        tools.append(create_email_tool())
    except Exception as e:
        print(f"⚠️  Email tool unavailable: {e}")
    
    try:
        tools.append(create_http_tool())
    except Exception as e:
        print(f"⚠️  HTTP tool unavailable: {e}")
    
    # Add custom tools here
    # tools.append(create_custom_tool())
    
    return tools


# Main export
ALL_TOOLS = get_all_tools()

# Tool categories for reference
TOOL_CATEGORIES = {
    "search": ["web_search"],
    "compute": ["python_repl"],
    "data": ["csv_writer"],
    "communication": ["email_sender"],
    "api": ["http_request"],
}

# Quick stats
def print_tool_stats():
    """Print summary of available tools"""
    print(f"📊 Tool Summary:")
    print(f"   Total tools: {len(ALL_TOOLS)}")
    
    for category, tool_names in TOOL_CATEGORIES.items():
        available = [t for t in ALL_TOOLS if t.name in tool_names]
        print(f"   {category.title()}: {len(available)}/{len(tool_names)} available")
    
    print(f"\n🔧 Available Tools:")
    for tool in ALL_TOOLS:
        print(f"   • {tool.name}: {tool.description[:50]}...")


if __name__ == "__main__":
    print_tool_stats()