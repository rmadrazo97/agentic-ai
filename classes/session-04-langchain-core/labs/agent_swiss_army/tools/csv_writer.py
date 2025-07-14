"""
CSV Writer Tool for data persistence and structured output
Handles creation and manipulation of CSV files
"""

import os
import csv
import json
import pandas as pd
from typing import List, Dict, Any, Union
from langchain.tools import Tool
from datetime import datetime


class CSVManager:
    """
    CSV file management with validation and formatting
    """
    
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def write_csv(self, data_input: str) -> str:
        """
        Write data to CSV file with intelligent parsing
        
        Args:
            data_input: Data in various formats (JSON, table format, etc.)
            
        Returns:
            Success message with file path
        """
        try:
            # Parse the input data
            data, filename = self._parse_input(data_input)
            
            if not data:
                return "Error: No valid data found to write to CSV"
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"data_export_{timestamp}.csv"
            
            # Ensure .csv extension
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            filepath = os.path.join(self.output_dir, filename)
            
            # Write to CSV using pandas for better handling
            if isinstance(data, list) and data:
                if isinstance(data[0], dict):
                    # List of dictionaries - standard format
                    df = pd.DataFrame(data)
                else:
                    # List of lists or simple list
                    df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Single record or data with multiple columns
                df = pd.DataFrame([data])
            else:
                return f"Error: Unsupported data format: {type(data)}"
            
            # Write to CSV
            df.to_csv(filepath, index=False)
            
            # Return success message with stats
            rows, cols = df.shape
            return f"✅ CSV file created successfully!\nFile: {filepath}\nRows: {rows}, Columns: {cols}\nColumns: {list(df.columns)}"
            
        except Exception as e:
            return f"Error creating CSV: {str(e)}"
    
    def _parse_input(self, data_input: str) -> tuple:
        """
        Parse various input formats to extract data and filename
        
        Returns:
            tuple: (data, filename)
        """
        data_input = data_input.strip()
        
        # Try to extract filename from input
        filename = None
        if "filename:" in data_input.lower():
            lines = data_input.split('\n')
            for line in lines:
                if line.lower().startswith('filename:'):
                    filename = line.split(':', 1)[1].strip()
                    data_input = data_input.replace(line, '').strip()
                    break
        
        # Try parsing as JSON first
        try:
            data = json.loads(data_input)
            return data, filename
        except json.JSONDecodeError:
            pass
        
        # Try parsing as table format (pipe-separated or comma-separated)
        if '|' in data_input or ',' in data_input:
            return self._parse_table_format(data_input), filename
        
        # Try parsing as key-value pairs
        if ':' in data_input and '\n' in data_input:
            return self._parse_key_value_format(data_input), filename
        
        # Default: treat as simple list
        items = [item.strip() for item in data_input.split('\n') if item.strip()]
        if items:
            return [{"item": item} for item in items], filename
        
        return None, filename
    
    def _parse_table_format(self, text: str) -> List[Dict]:
        """
        Parse table format (pipe or comma separated)
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return []
        
        # Determine separator
        separator = '|' if '|' in lines[0] else ','
        
        # Parse header
        headers = [h.strip() for h in lines[0].split(separator)]
        
        # Parse data rows
        data = []
        for line in lines[1:]:
            if separator == '|' and ('---' in line or '===' in line):
                continue  # Skip separator lines in markdown tables
            
            values = [v.strip() for v in line.split(separator)]
            if len(values) == len(headers):
                row_dict = dict(zip(headers, values))
                data.append(row_dict)
        
        return data
    
    def _parse_key_value_format(self, text: str) -> List[Dict]:
        """
        Parse key-value format (key: value pairs)
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        data = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        return [data] if data else []
    
    def read_csv(self, filename: str) -> str:
        """
        Read and display CSV file contents
        
        Args:
            filename: Name of the CSV file to read
            
        Returns:
            Formatted string representation of the CSV data
        """
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            if not os.path.exists(filepath):
                return f"Error: File '{filename}' not found in {self.output_dir}"
            
            df = pd.read_csv(filepath)
            
            # Format output
            rows, cols = df.shape
            result = [
                f"📊 CSV File: {filename}",
                f"Dimensions: {rows} rows × {cols} columns",
                f"Columns: {list(df.columns)}",
                "",
                "Data preview (first 5 rows):",
                df.head().to_string(index=False)
            ]
            
            if rows > 5:
                result.append(f"\n... and {rows - 5} more rows")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error reading CSV: {str(e)}"
    
    def list_csv_files(self) -> str:
        """
        List all CSV files in the output directory
        
        Returns:
            Formatted list of CSV files
        """
        try:
            csv_files = [f for f in os.listdir(self.output_dir) if f.endswith('.csv')]
            
            if not csv_files:
                return f"No CSV files found in {self.output_dir}"
            
            result = [f"📁 CSV files in {self.output_dir}:"]
            for i, filename in enumerate(sorted(csv_files), 1):
                filepath = os.path.join(self.output_dir, filename)
                size = os.path.getsize(filepath)
                modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                result.append(f"  {i}. {filename} ({size} bytes, modified: {modified.strftime('%Y-%m-%d %H:%M')})")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error listing CSV files: {str(e)}"


def create_csv_tool() -> Tool:
    """
    Create a CSV writer tool for data persistence
    
    Returns:
        LangChain Tool object for CSV operations
    """
    csv_manager = CSVManager()
    
    def csv_operations(operation_input: str) -> str:
        """
        Handle CSV operations (write, read, list)
        
        Format examples:
        - Write: "write: [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]"
        - Write with filename: "filename: people.csv\nwrite: [data...]"
        - Read: "read: filename.csv"
        - List: "list"
        """
        operation_input = operation_input.strip()
        
        # Parse operation type
        if operation_input.lower().startswith('read:'):
            filename = operation_input[5:].strip()
            return csv_manager.read_csv(filename)
        
        elif operation_input.lower() == 'list':
            return csv_manager.list_csv_files()
        
        elif operation_input.lower().startswith('write:'):
            data_part = operation_input[6:].strip()
            return csv_manager.write_csv(data_part)
        
        else:
            # Default to write operation
            return csv_manager.write_csv(operation_input)
    
    return Tool.from_function(
        name="csv_writer",
        description="""Create, read, and manage CSV files for data storage. 
        Operations:
        - Write data: Provide data as JSON list/dict, table format, or key-value pairs
        - Read file: "read: filename.csv" 
        - List files: "list"
        
        Examples:
        - '[{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]'
        - 'Name | Age\\nAlice | 25\\nBob | 30'
        - 'filename: report.csv\\n[data here]'""",
        func=csv_operations
    )


# Test function
def test_csv_tool():
    """Test the CSV writer tool"""
    print("📊 Testing CSV Writer Tool...")
    
    tool = create_csv_tool()
    
    # Test 1: Write JSON data
    print("\nTest 1: Write JSON data")
    json_data = '[{"name": "Alice", "age": 25, "city": "New York"}, {"name": "Bob", "age": 30, "city": "Los Angeles"}]'
    result = tool.func(json_data)
    print(result)
    
    # Test 2: Write table format
    print("\nTest 2: Write table format")
    table_data = """Name | Age | Department
Alice | 25 | Engineering
Bob | 30 | Marketing
Charlie | 28 | Sales"""
    result = tool.func(f"filename: employees.csv\nwrite: {table_data}")
    print(result)
    
    # Test 3: List files
    print("\nTest 3: List CSV files")
    result = tool.func("list")
    print(result)
    
    print("\n✅ CSV tool test completed")


if __name__ == "__main__":
    test_csv_tool()