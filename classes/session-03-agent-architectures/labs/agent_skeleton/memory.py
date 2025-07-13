"""
Simple Memory Store for Agent
Optional for Session 3 - will be used in later sessions for conversation history
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class SimpleMemory:
    """
    Simple JSON-based memory store for agent conversations
    
    In later sessions, this will be expanded to support:
    - Vector embeddings for semantic search
    - Conversation summarization
    - Long-term memory persistence
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load memory from JSON file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Return default structure
        return {
            "conversations": [],
            "facts": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_queries": 0
            }
        }
    
    def _save_memory(self):
        """Save memory to JSON file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save memory: {e}")
    
    def add_conversation(self, question: str, answer: str, tools_used: List[str] = None):
        """
        Add a conversation to memory
        
        Args:
            question: User's question
            answer: Agent's final answer
            tools_used: List of tools that were called
        """
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "tools_used": tools_used or [],
            "id": len(self.memory["conversations"])
        }
        
        self.memory["conversations"].append(conversation)
        self.memory["metadata"]["total_queries"] += 1
        self._save_memory()
    
    def add_fact(self, key: str, value: Any):
        """
        Store a fact for future reference
        
        Args:
            key: Fact identifier
            value: Fact value
        """
        self.memory["facts"][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        self._save_memory()
    
    def get_recent_conversations(self, limit: int = 5) -> List[Dict]:
        """Get recent conversations"""
        return self.memory["conversations"][-limit:]
    
    def search_conversations(self, keyword: str) -> List[Dict]:
        """
        Simple keyword search in conversations
        
        Args:
            keyword: Term to search for
            
        Returns:
            List of matching conversations
        """
        matches = []
        keyword_lower = keyword.lower()
        
        for conv in self.memory["conversations"]:
            if (keyword_lower in conv["question"].lower() or 
                keyword_lower in conv["answer"].lower()):
                matches.append(conv)
        
        return matches
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        conversations = self.memory["conversations"]
        if not conversations:
            return {"total_queries": 0, "most_used_tools": []}
        
        # Count tool usage
        tool_counts = {}
        for conv in conversations:
            for tool in conv.get("tools_used", []):
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        # Sort tools by usage
        most_used_tools = sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_queries": len(conversations),
            "first_query": conversations[0]["timestamp"] if conversations else None,
            "last_query": conversations[-1]["timestamp"] if conversations else None,
            "most_used_tools": most_used_tools[:3],
            "total_facts": len(self.memory["facts"])
        }
    
    def clear_memory(self):
        """Clear all memory (useful for testing)"""
        self.memory = {
            "conversations": [],
            "facts": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_queries": 0
            }
        }
        self._save_memory()


# Example usage for testing
if __name__ == "__main__":
    # Test memory functionality
    memory = SimpleMemory("test_memory.json")
    
    # Add some test conversations
    memory.add_conversation(
        "What is 2+2?", 
        "The answer is 4",
        ["calculator"]
    )
    
    memory.add_conversation(
        "What is the capital of France?",
        "The capital of France is Paris",
        ["web_search"]
    )
    
    # Add a fact
    memory.add_fact("berlin_population", 3700000)
    
    # Print stats
    stats = memory.get_stats()
    print("Memory Stats:")
    print(f"Total queries: {stats['total_queries']}")
    print(f"Most used tools: {stats['most_used_tools']}")
    
    # Search conversations
    matches = memory.search_conversations("France")
    print(f"\nConversations about France: {len(matches)}")
    
    # Clean up test file
    os.remove("test_memory.json")
    print("✅ Memory test completed!")