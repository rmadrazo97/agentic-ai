"""
Web Search Tool using Tavily API
Fast, reliable web search optimized for LLM agents
"""

import os
from typing import Optional
from langchain.tools import Tool
from tavily import TavilyClient


class WebSearchTool:
    """Web search implementation using Tavily API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError(
                "TAVILY_API_KEY required. Get free key at https://tavily.com"
            )
        
        self.client = TavilyClient(api_key=self.api_key)
    
    def search(self, query: str) -> str:
        """
        Search the web for current information
        
        Args:
            query: Search terms to look for
            
        Returns:
            Formatted search results
        """
        try:
            # Search with Tavily
            response = self.client.search(
                query=query,
                search_depth="basic",  # "basic" or "advanced"
                max_results=5,
                include_answer=True,
                include_raw_content=False
            )
            
            # Format results
            if not response.get('results'):
                return f"No search results found for: {query}"
            
            # Start with direct answer if available
            formatted_results = []
            
            if response.get('answer'):
                formatted_results.append(f"Direct Answer: {response['answer']}\n")
            
            # Add source results
            formatted_results.append("Search Results:")
            for i, result in enumerate(response['results'][:3], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No description')
                url = result.get('url', '')
                
                # Truncate long content
                if len(content) > 200:
                    content = content[:200] + "..."
                
                formatted_results.append(
                    f"{i}. {title}\n   {content}\n   Source: {url}"
                )
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            return f"Search error: {str(e)}. Please try rephrasing your query."


def create_search_tool() -> Tool:
    """
    Create a web search tool instance
    
    Returns:
        LangChain Tool object for web searching
    """
    # Check if API key is available
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        # Return a mock tool if no API key
        def mock_search(query: str) -> str:
            return f"Mock search result for: {query} (Set TAVILY_API_KEY for real search)"
        
        return Tool.from_function(
            name="web_search",
            description="Search the web for current information (MOCK - set TAVILY_API_KEY for real search)",
            func=mock_search
        )
    
    # Create real search tool
    search_tool = WebSearchTool(api_key)
    
    return Tool.from_function(
        name="web_search",
        description="Search the web for current information, news, facts, and recent developments. Use this when you need up-to-date information that might not be in your training data.",
        func=search_tool.search
    )


# Alternative implementation using DuckDuckGo (backup)
def create_duckduckgo_search_tool() -> Tool:
    """
    Fallback search tool using DuckDuckGo (no API key required)
    """
    try:
        from duckduckgo_search import DDGS
        
        def ddg_search(query: str) -> str:
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
                
                if not results:
                    return f"No search results found for: {query}"
                
                formatted_results = []
                for i, result in enumerate(results, 1):
                    title = result.get('title', 'No title')
                    snippet = result.get('body', 'No description')
                    url = result.get('href', '')
                    
                    if len(snippet) > 150:
                        snippet = snippet[:150] + "..."
                    
                    formatted_results.append(f"{i}. {title}: {snippet}")
                
                return "\n".join(formatted_results)
                
            except Exception as e:
                return f"Search error: {str(e)}"
        
        return Tool.from_function(
            name="web_search",
            description="Search the web for current information using DuckDuckGo",
            func=ddg_search
        )
        
    except ImportError:
        # Return mock if DuckDuckGo not available
        def mock_search(query: str) -> str:
            return f"Search functionality unavailable. Install duckduckgo-search or set TAVILY_API_KEY"
        
        return Tool.from_function(
            name="web_search",
            description="Web search (unavailable - missing dependencies)",
            func=mock_search
        )


# Test function
def test_search_tool():
    """Test the search tool functionality"""
    print("🔍 Testing Web Search Tool...")
    
    tool = create_search_tool()
    
    # Test query
    result = tool.func("latest Python programming trends 2024")
    print(f"Search Result: {result[:200]}...")
    
    print("✅ Search tool test completed")


if __name__ == "__main__":
    test_search_tool()