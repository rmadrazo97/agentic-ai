"""
HTTP Request Tool for API integrations and web services
Safe HTTP client with configurable methods and validation
"""

import json
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from langchain.tools import Tool


class HTTPClient:
    """
    Safe HTTP client for API integrations
    """
    
    def __init__(self, timeout: int = 30, max_response_size: int = 1024*1024):  # 1MB limit
        self.timeout = timeout
        self.max_response_size = max_response_size
        
        # Allowed domains (whitelist for security)
        self.allowed_domains = {
            'api.github.com',
            'jsonplaceholder.typicode.com',
            'httpbin.org',
            'api.openweathermap.org',
            'api.exchangerate-api.com',
            'restcountries.com',
            # Add more trusted APIs here
        }
        
        # Default headers
        self.default_headers = {
            'User-Agent': 'LangChain-Agent/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def make_request(self, request_input: str) -> str:
        """
        Make HTTP request based on input specification
        
        Args:
            request_input: HTTP request details in various formats
            
        Returns:
            Formatted response data
        """
        try:
            # Parse request details
            request_data = self._parse_request_input(request_input)
            
            if not request_data:
                return "Error: Invalid request format"
            
            url = request_data.get('url')
            method = request_data.get('method', 'GET').upper()
            headers = request_data.get('headers', {})
            params = request_data.get('params', {})
            data = request_data.get('data')
            
            # Validate URL
            if not self._is_url_allowed(url):
                return f"Error: URL not allowed. Allowed domains: {', '.join(self.allowed_domains)}"
            
            # Validate method
            if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                return f"Error: HTTP method '{method}' not allowed"
            
            # Prepare headers
            final_headers = {**self.default_headers, **headers}
            
            # Make request
            response = self._execute_request(
                method=method,
                url=url,
                headers=final_headers,
                params=params,
                data=data
            )
            
            return self._format_response(response)
            
        except Exception as e:
            return f"HTTP request failed: {str(e)}"
    
    def _parse_request_input(self, request_input: str) -> Dict[str, Any]:
        """
        Parse HTTP request input in various formats
        """
        request_input = request_input.strip()
        
        # Try JSON format first
        try:
            return json.loads(request_input)
        except json.JSONDecodeError:
            pass
        
        # Try structured text format
        request_data = {}
        lines = request_input.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key in ['url', 'method']:
                    request_data[key] = value
                elif key == 'headers':
                    try:
                        request_data['headers'] = json.loads(value)
                    except:
                        # Simple header format "key=value, key2=value2"
                        headers = {}
                        for header_pair in value.split(','):
                            if '=' in header_pair:
                                h_key, h_value = header_pair.split('=', 1)
                                headers[h_key.strip()] = h_value.strip()
                        request_data['headers'] = headers
                elif key == 'params':
                    try:
                        request_data['params'] = json.loads(value)
                    except:
                        # Simple param format "key=value&key2=value2"
                        params = {}
                        for param_pair in value.split('&'):
                            if '=' in param_pair:
                                p_key, p_value = param_pair.split('=', 1)
                                params[p_key.strip()] = p_value.strip()
                        request_data['params'] = params
                elif key in ['data', 'body']:
                    try:
                        request_data['data'] = json.loads(value)
                    except:
                        request_data['data'] = value
        
        # If just a URL is provided, treat as GET request
        if not request_data and request_input.startswith('http'):
            request_data = {'url': request_input, 'method': 'GET'}
        
        return request_data
    
    def _is_url_allowed(self, url: str) -> bool:
        """
        Check if URL is in allowed domains list
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove port if present
            if ':' in domain:
                domain = domain.split(':')[0]
            
            return domain in self.allowed_domains
        except:
            return False
    
    def _execute_request(self, method: str, url: str, headers: Dict, 
                        params: Dict, data: Any) -> requests.Response:
        """
        Execute the HTTP request with safety measures
        """
        # Prepare request kwargs
        kwargs = {
            'timeout': self.timeout,
            'headers': headers,
            'params': params
        }
        
        # Add data for POST/PUT/PATCH requests
        if method in ['POST', 'PUT', 'PATCH'] and data:
            if isinstance(data, dict):
                kwargs['json'] = data
            else:
                kwargs['data'] = data
        
        # Execute request
        response = requests.request(method, url, **kwargs)
        
        # Check response size
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > self.max_response_size:
            raise ValueError(f"Response too large: {content_length} bytes")
        
        return response
    
    def _format_response(self, response: requests.Response) -> str:
        """
        Format HTTP response for agent consumption
        """
        result = [
            f"🌐 HTTP {response.request.method} {response.url}",
            f"Status: {response.status_code} {response.reason}",
            f"Response Time: {response.elapsed.total_seconds():.2f}s",
            ""
        ]
        
        # Add response headers (selected ones)
        important_headers = ['content-type', 'content-length', 'server']
        for header in important_headers:
            if header in response.headers:
                result.append(f"{header.title()}: {response.headers[header]}")
        
        result.append("")
        
        # Add response body
        try:
            # Try to parse as JSON
            json_data = response.json()
            
            # Truncate large JSON responses
            json_str = json.dumps(json_data, indent=2)
            if len(json_str) > 2000:
                # Show structure for large responses
                if isinstance(json_data, list):
                    result.append(f"Response Body (JSON Array with {len(json_data)} items):")
                    result.append(json.dumps(json_data[:3], indent=2))
                    if len(json_data) > 3:
                        result.append(f"... and {len(json_data) - 3} more items")
                elif isinstance(json_data, dict):
                    result.append("Response Body (JSON Object):")
                    # Show first few keys
                    preview_data = dict(list(json_data.items())[:5])
                    result.append(json.dumps(preview_data, indent=2))
                    if len(json_data) > 5:
                        result.append(f"... and {len(json_data) - 5} more fields")
                else:
                    result.append("Response Body (JSON):")
                    result.append(json_str[:1000] + "..." if len(json_str) > 1000 else json_str)
            else:
                result.append("Response Body:")
                result.append(json_str)
                
        except json.JSONDecodeError:
            # Handle non-JSON responses
            text = response.text
            if len(text) > 1000:
                result.append("Response Body (Text, truncated):")
                result.append(text[:1000] + "...")
            else:
                result.append("Response Body:")
                result.append(text)
        
        return "\n".join(result)


def create_http_tool() -> Tool:
    """
    Create an HTTP request tool for API integrations
    
    Returns:
        LangChain Tool object for HTTP requests
    """
    http_client = HTTPClient()
    
    return Tool.from_function(
        name="http_request",
        description="""Make HTTP requests to APIs and web services. Supports GET, POST, PUT, DELETE methods.
        
        Formats:
        - Simple: 'https://api.github.com/users/octocat'
        - Structured: 'url: https://api.example.com/data\\nmethod: GET\\nparams: {"key": "value"}'
        - JSON: '{"url": "https://api.example.com", "method": "POST", "data": {"field": "value"}}'
        
        Allowed domains: api.github.com, jsonplaceholder.typicode.com, httpbin.org, restcountries.com
        
        Use for fetching data from APIs, checking service status, or integrating with external services.""",
        func=http_client.make_request
    )


# Test function
def test_http_tool():
    """Test the HTTP request tool"""
    print("🌐 Testing HTTP Request Tool...")
    
    tool = create_http_tool()
    
    # Test 1: Simple GET request
    print("\nTest 1: Simple GET request")
    result = tool.func("https://jsonplaceholder.typicode.com/posts/1")
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test 2: Structured request
    print("\nTest 2: Structured request with parameters")
    structured_request = """url: https://jsonplaceholder.typicode.com/posts
method: GET
params: {"userId": "1"}"""
    result = tool.func(structured_request)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test 3: POST request (JSON format)
    print("\nTest 3: POST request")
    post_request = {
        "url": "https://jsonplaceholder.typicode.com/posts",
        "method": "POST",
        "data": {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
    }
    result = tool.func(json.dumps(post_request))
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n✅ HTTP tool test completed")


if __name__ == "__main__":
    test_http_tool()