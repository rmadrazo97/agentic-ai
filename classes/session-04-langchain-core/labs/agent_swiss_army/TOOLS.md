# Tools Documentation 🔧

This document lists all available tools in the Swiss Army Agent, organized by category with use cases and implementation details.

## 🔍 Search Tools

### web_search
- **Category**: Search  
- **Implementation**: Tavily API (fallback to DuckDuckGo)
- **Use Case**: Search the web for current information, news, facts, and recent developments
- **Input**: Search query string
- **Output**: Formatted search results with titles, snippets, and sources
- **Example**: `"latest Python programming trends 2024"`

## 💻 Compute Tools

### python_repl
- **Category**: Compute
- **Implementation**: Safe Python execution environment with whitelisted modules
- **Use Case**: Execute Python code for data processing, calculations, and analysis  
- **Input**: Python code string
- **Output**: Execution result or error message
- **Available Modules**: pandas, numpy, json, math, datetime, collections, re
- **Example**: `"pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [25, 30]}).mean()"`

### calculator
- **Category**: Compute
- **Implementation**: Safe mathematical expression evaluator
- **Use Case**: Perform mathematical calculations and functions
- **Input**: Mathematical expression
- **Output**: Numerical result
- **Supported**: Basic arithmetic (+, -, *, /), sqrt, log, sin, cos, tan, exp, pow
- **Example**: `"sqrt(25) + 10 * 2"`

## 📊 Data I/O Tools

### csv_writer
- **Category**: Data I/O
- **Implementation**: CSV file management with pandas
- **Use Case**: Create, read, and manage CSV files for data storage and export
- **Input**: Data in JSON, table format, or key-value pairs; operations (read, write, list)
- **Output**: Success message with file details or file contents
- **Features**: Auto-formatting, filename specification, data validation
- **Example**: `"[{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]"`

## 📢 Communication Tools

### email_sender
- **Category**: Communication
- **Implementation**: Mock email system (saves to files in outputs/email_outbox/)
- **Use Case**: Send email notifications and reports (development/demo mode)
- **Input**: Email details (to, subject, body) in structured text or JSON format
- **Output**: Confirmation message with email details
- **Features**: Multiple format support, outbox management, email history
- **Example**: `"to: user@example.com\nsubject: Report Ready\nbody: Your analysis is complete."`

## 🌐 API Tools

### http_request
- **Category**: API Integration
- **Implementation**: Safe HTTP client with domain whitelist
- **Use Case**: Make HTTP requests to APIs and web services for data integration
- **Input**: HTTP request details (URL, method, headers, params, data)
- **Output**: Formatted HTTP response with status, headers, and body
- **Allowed Domains**: api.github.com, jsonplaceholder.typicode.com, httpbin.org, restcountries.com
- **Methods**: GET, POST, PUT, DELETE, PATCH
- **Example**: `"https://api.github.com/users/octocat"`

## 🕒 Utility Tools

### current_date
- **Category**: Utility
- **Implementation**: Python datetime module
- **Use Case**: Get current date and time information
- **Input**: Optional query for specific date/time info
- **Output**: Current date/time in requested format
- **Features**: Date, time, year queries
- **Example**: `"current date"` or `"what time is it"`

## 🔧 Tool Usage Statistics

Run `python tools/__init__.py` to see current tool availability:

```
📊 Tool Summary:
   Total tools: 6
   Search: 1/1 available
   Compute: 2/2 available  
   Data: 1/1 available
   Communication: 1/1 available
   API: 1/1 available

🔧 Available Tools:
   • web_search: Search the web for current information...
   • python_repl: Execute Python code for data processing...
   • calculator: Perform mathematical calculations...
   • csv_writer: Create, read, and manage CSV files...
   • email_sender: Send emails and manage outbox...
   • http_request: Make HTTP requests to APIs...
```

## 🛡️ Safety Features

### Python REPL Safety
- **Whitelisted modules only**: pandas, numpy, json, math, datetime, collections, re
- **Blocked dangerous functions**: eval, exec, open, import, globals, etc.
- **AST parsing**: Code is analyzed before execution
- **Output capture**: Safe stdout/stderr redirection
- **Timeout protection**: Prevents infinite loops

### HTTP Request Safety  
- **Domain whitelist**: Only trusted domains allowed
- **Method restrictions**: Limited to safe HTTP methods
- **Response size limits**: Maximum 1MB response size
- **Timeout protection**: 30-second request timeout
- **Header validation**: Controlled request headers

### File Operations Safety
- **Sandboxed directories**: All file operations in `outputs/` directory
- **Filename validation**: Safe filename generation and validation
- **Size limits**: Reasonable file size restrictions
- **Format validation**: Input validation for different data formats

## 📈 Performance Characteristics

| Tool | Avg Runtime | Cost Impact | Reliability |
|------|-------------|-------------|-------------|
| web_search | 2-5 seconds | None (external API) | High |
| python_repl | <1 second | None | Very High |
| calculator | <0.1 seconds | None | Very High |
| csv_writer | <0.5 seconds | None | Very High |
| email_sender | <0.1 seconds | None | Very High |
| http_request | 1-3 seconds | None (external API) | High |

## 🚀 Extending the Tool Suite

### Adding Custom Tools

1. **Create tool module** in `tools/` directory:
```python
# tools/my_tool.py
from langchain.tools import Tool

def my_function(input_str: str) -> str:
    # Implementation here
    return result

def create_my_tool() -> Tool:
    return Tool.from_function(
        name="my_tool",
        description="Clear description for LLM",
        func=my_function
    )
```

2. **Register in tool registry** (`tools/__init__.py`):
```python
from .my_tool import create_my_tool

def get_all_tools():
    tools = [
        # ... existing tools
        create_my_tool(),
    ]
    return tools
```

3. **Update this documentation** with tool details

### Tool Design Best Practices

- **Stateless functions**: No side effects or global state
- **Clear descriptions**: Help LLM understand when to use the tool
- **Error handling**: Graceful failure with helpful error messages  
- **Input validation**: Validate and sanitize all inputs
- **Output formatting**: Consistent, readable output format
- **Performance**: Complete operations in <10 seconds when possible

## 🔍 Debugging Tools

### Tool Testing
```bash
# Test individual tools
python tools/search.py
python tools/compute.py  
python tools/csv_writer.py

# Test tool registry
python tools/__init__.py
```

### Tool Monitoring
```bash
# Check tool usage in metrics
python driver.py --interactive
> stats

# View detailed tool metrics
cat outputs/metrics.json | grep "tool_"
```

---

**Note**: This tool suite is designed for educational and development purposes. In production environments, additional security measures, monitoring, and configuration management would be required.