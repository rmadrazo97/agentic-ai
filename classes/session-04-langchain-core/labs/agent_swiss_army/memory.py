"""
Memory Management for Swiss Army Agent
Implements conversation memory with summarization and persistence options
"""

import os
import json
from typing import Optional, Dict, List, Any
from datetime import datetime

from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain.memory.chat_message_histories import (
    ChatMessageHistory,
    FileChatMessageHistory,
    RedisChatMessageHistory
)
from langchain_anthropic import ChatAnthropic


class MemoryManager:
    """
    Centralized memory management with multiple strategies and persistence
    """
    
    def __init__(self, strategy: str = "summary_buffer", session_id: str = "default"):
        self.strategy = strategy
        self.session_id = session_id
        self.llm = ChatAnthropic(model_name="claude-3-haiku-20240307", temperature=0)
        
        # Create memory based on strategy
        self.memory = self._create_memory()
    
    def _create_memory(self):
        """
        Create memory instance based on strategy
        """
        # Choose persistence backend
        chat_history = self._create_chat_history()
        
        if self.strategy == "buffer":
            return ConversationBufferMemory(
                chat_memory=chat_history,
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        
        elif self.strategy == "summary":
            return ConversationSummaryMemory(
                llm=self.llm,
                chat_memory=chat_history,
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        
        elif self.strategy == "window":
            return ConversationBufferWindowMemory(
                k=10,  # Keep last 10 messages
                chat_memory=chat_history,
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        
        elif self.strategy == "summary_buffer":
            return ConversationSummaryBufferMemory(
                llm=self.llm,
                chat_memory=chat_history,
                max_token_limit=4000,  # 4K token limit before summarization
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        
        else:
            raise ValueError(f"Unknown memory strategy: {self.strategy}")
    
    def _create_chat_history(self):
        """
        Create chat history with persistence
        """
        # Try Redis first (for production)
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                return RedisChatMessageHistory(
                    session_id=self.session_id,
                    url=redis_url
                )
            except ImportError:
                print("⚠️  Redis not available, falling back to file storage")
        
        # Fallback to file-based storage
        memory_dir = "outputs/memory"
        os.makedirs(memory_dir, exist_ok=True)
        
        file_path = os.path.join(memory_dir, f"chat_history_{self.session_id}.json")
        return FileChatMessageHistory(file_path=file_path)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about current memory usage
        """
        messages = self.memory.chat_memory.messages
        
        # Count tokens (rough estimate)
        total_tokens = sum(len(msg.content) // 4 for msg in messages)
        
        # Message counts by type
        human_messages = sum(1 for msg in messages if hasattr(msg, 'type') and msg.type == 'human')
        ai_messages = sum(1 for msg in messages if hasattr(msg, 'type') and msg.type == 'ai')
        
        return {
            "strategy": self.strategy,
            "session_id": self.session_id,
            "total_messages": len(messages),
            "human_messages": human_messages,
            "ai_messages": ai_messages,
            "estimated_tokens": total_tokens,
            "memory_key": self.memory.memory_key
        }
    
    def get_conversation_summary(self) -> str:
        """
        Get a summary of the conversation so far
        """
        if hasattr(self.memory, 'predict_new_summary'):
            # For summary-based memories
            messages = self.memory.chat_memory.messages
            if messages:
                return self.memory.predict_new_summary(messages, "")
        
        # Fallback: manual summary
        messages = self.memory.chat_memory.messages
        if not messages:
            return "No conversation history"
        
        # Simple summary for other memory types
        recent_messages = messages[-6:]  # Last 3 exchanges
        summary_parts = []
        
        for msg in recent_messages:
            role = "Human" if hasattr(msg, 'type') and msg.type == 'human' else "AI"
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            summary_parts.append(f"{role}: {content}")
        
        return "\n".join(summary_parts)
    
    def clear_memory(self):
        """
        Clear all conversation memory
        """
        self.memory.clear()
    
    def save_memory_snapshot(self, filename: Optional[str] = None) -> str:
        """
        Save current memory state to file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"memory_snapshot_{self.session_id}_{timestamp}.json"
        
        snapshot_dir = "outputs/memory_snapshots"
        os.makedirs(snapshot_dir, exist_ok=True)
        filepath = os.path.join(snapshot_dir, filename)
        
        # Prepare snapshot data
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "strategy": self.strategy,
            "stats": self.get_memory_stats(),
            "summary": self.get_conversation_summary(),
            "messages": []
        }
        
        # Add messages
        for msg in self.memory.chat_memory.messages:
            snapshot["messages"].append({
                "type": getattr(msg, 'type', 'unknown'),
                "content": msg.content,
                "timestamp": getattr(msg, 'timestamp', None)
            })
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        return f"Memory snapshot saved to: {filepath}"


def build_memory(strategy: str = "summary_buffer", session_id: str = "default"):
    """
    Factory function to build memory with specified strategy
    
    Args:
        strategy: Memory strategy ("buffer", "summary", "window", "summary_buffer")
        session_id: Unique identifier for this conversation session
        
    Returns:
        Configured memory instance
    """
    manager = MemoryManager(strategy=strategy, session_id=session_id)
    return manager.memory


def create_memory_for_session(session_id: str, user_preferences: Dict[str, Any] = None):
    """
    Create memory tailored to user preferences and session requirements
    
    Args:
        session_id: Unique session identifier
        user_preferences: Dict with preferences like max_cost, conversation_length, etc.
        
    Returns:
        Configured memory instance
    """
    preferences = user_preferences or {}
    
    # Determine strategy based on preferences
    max_cost = preferences.get("max_cost", 0.10)  # Default $0.10 budget
    expected_length = preferences.get("conversation_length", "medium")
    
    if expected_length == "short" or max_cost < 0.05:
        strategy = "window"  # Cheapest option
    elif expected_length == "long" or max_cost > 0.20:
        strategy = "summary"  # Best for long conversations
    else:
        strategy = "summary_buffer"  # Balanced approach
    
    return build_memory(strategy=strategy, session_id=session_id)


def get_memory_recommendation(conversation_history: List[str]) -> str:
    """
    Recommend memory strategy based on conversation history
    
    Args:
        conversation_history: List of previous messages
        
    Returns:
        Recommended memory strategy
    """
    message_count = len(conversation_history)
    total_length = sum(len(msg) for msg in conversation_history)
    
    if message_count < 10 and total_length < 5000:
        return "buffer"  # Small conversations
    elif message_count > 50 or total_length > 20000:
        return "summary"  # Large conversations
    elif message_count > 20:
        return "window"  # Medium conversations
    else:
        return "summary_buffer"  # Default balanced approach


# Test function
def test_memory():
    """Test memory functionality"""
    print("🧠 Testing Memory Management...")
    
    # Test different strategies
    strategies = ["buffer", "summary_buffer", "window"]
    
    for strategy in strategies:
        print(f"\n--- Testing {strategy} strategy ---")
        
        manager = MemoryManager(strategy=strategy, session_id=f"test_{strategy}")
        memory = manager.memory
        
        # Simulate conversation
        memory.save_context(
            {"input": "Hello, my name is Alice"},
            {"output": "Hello Alice! Nice to meet you."}
        )
        
        memory.save_context(
            {"input": "What's my name?"},
            {"output": "Your name is Alice."}
        )
        
        # Get memory variables
        memory_vars = memory.load_memory_variables({})
        print(f"Memory variables: {list(memory_vars.keys())}")
        
        # Get stats
        stats = manager.get_memory_stats()
        print(f"Stats: {stats}")
        
        # Get summary
        summary = manager.get_conversation_summary()
        print(f"Summary: {summary[:100]}...")
        
        # Clear for next test
        manager.clear_memory()
    
    print("\n✅ Memory test completed")


if __name__ == "__main__":
    test_memory()