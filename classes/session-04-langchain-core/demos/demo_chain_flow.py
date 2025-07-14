#!/usr/bin/env python3
"""
Chain Flow Demonstration
Shows different LangChain chain types and composition patterns

Usage:
    export ANTHROPIC_API_KEY="sk-ant-your-key"
    python demo_chain_flow.py
"""

import os
import sys
import time
from typing import Dict, List, Any

# Add lab directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'labs', 'agent_swiss_army'))

from langchain.chains import LLMChain, SequentialChain
from langchain.chains.router import MultiPromptChain, LLMRouterChain
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence, RunnableLambda, RunnableParallel
from langchain_anthropic import ChatAnthropic


class ChainFlowDemo:
    """
    Comprehensive demonstration of LangChain chain types and patterns
    """
    
    def __init__(self):
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        
        self.llm = ChatAnthropic(
            model_name="claude-3-haiku-20240307",
            temperature=0.3
        )
    
    def demo_simple_chain(self):
        """
        Demo 1: Simple LLM Chain - Basic prompt → LLM → output
        """
        print("🔗 Demo 1: Simple LLM Chain")
        print("-" * 40)
        
        # Create a simple chain
        prompt = PromptTemplate.from_template(
            "Explain the concept of {topic} in exactly 2 sentences."
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        # Run the chain
        topic = "artificial intelligence"
        print(f"Input: {topic}")
        
        result = chain.run(topic=topic)
        print(f"Output: {result}")
        print()
    
    def demo_sequential_chain(self):
        """
        Demo 2: Sequential Chain - Multi-step processing
        """
        print("🔗 Demo 2: Sequential Chain")
        print("-" * 40)
        
        # Step 1: Generate a story outline
        outline_prompt = PromptTemplate.from_template(
            "Create a brief 3-point outline for a story about {theme}."
        )
        outline_chain = LLMChain(
            llm=self.llm,
            prompt=outline_prompt,
            output_key="outline"
        )
        
        # Step 2: Write the story based on outline
        story_prompt = PromptTemplate.from_template(
            "Write a very short story (2-3 sentences) based on this outline:\n{outline}"
        )
        story_chain = LLMChain(
            llm=self.llm,
            prompt=story_prompt,
            output_key="story"
        )
        
        # Step 3: Create a title
        title_prompt = PromptTemplate.from_template(
            "Create a catchy title for this story:\n{story}"
        )
        title_chain = LLMChain(
            llm=self.llm,
            prompt=title_prompt,
            output_key="title"
        )
        
        # Combine into sequential chain
        sequential_chain = SequentialChain(
            chains=[outline_chain, story_chain, title_chain],
            input_variables=["theme"],
            output_variables=["outline", "story", "title"],
            verbose=True
        )
        
        # Run the chain
        theme = "a robot learning to paint"
        print(f"Input theme: {theme}")
        print("\nProcessing through chain...")
        
        result = sequential_chain({"theme": theme})
        
        print(f"\nFinal Results:")
        print(f"Title: {result['title']}")
        print(f"Story: {result['story']}")
        print()
    
    def demo_router_chain(self):
        """
        Demo 3: Router Chain - Intelligent routing to specialized chains
        """
        print("🔗 Demo 3: Router Chain")
        print("-" * 40)
        
        # Create specialized chains
        math_prompt = PromptTemplate.from_template(
            "Solve this math problem step by step: {input}"
        )
        math_chain = LLMChain(llm=self.llm, prompt=math_prompt)
        
        writing_prompt = PromptTemplate.from_template(
            "Write a creative piece about: {input}"
        )
        writing_chain = LLMChain(llm=self.llm, prompt=writing_prompt)
        
        science_prompt = PromptTemplate.from_template(
            "Explain this scientific concept clearly: {input}"
        )
        science_chain = LLMChain(llm=self.llm, prompt=science_prompt)
        
        # Create destination chains
        destination_chains = {
            "math": math_chain,
            "writing": writing_chain,
            "science": science_chain
        }
        
        # Create router prompt
        router_template = """Given a user input, choose which expert should handle it:

math: for mathematical problems, calculations, equations
writing: for creative writing, stories, poetry, essays  
science: for scientific explanations, concepts, phenomena

Input: {input}
Destination:"""
        
        router_prompt = PromptTemplate.from_template(router_template)
        router_chain = LLMRouterChain.from_llm(self.llm, router_prompt)
        
        # Create multi-prompt chain
        multi_prompt_chain = MultiPromptChain(
            router_chain=router_chain,
            destination_chains=destination_chains,
            default_chain=writing_chain,
            verbose=True
        )
        
        # Test different inputs
        test_inputs = [
            "What is the square root of 144?",
            "Write a haiku about autumn",
            "How does photosynthesis work?"
        ]
        
        for test_input in test_inputs:
            print(f"\nInput: {test_input}")
            result = multi_prompt_chain.run(test_input)
            print(f"Output: {result[:100]}...")
        
        print()
    
    def demo_runnable_sequence(self):
        """
        Demo 4: Modern Runnable Sequence - New LangChain pattern
        """
        print("🔗 Demo 4: Runnable Sequence (Modern Pattern)")
        print("-" * 40)
        
        # Create preprocessing function
        def preprocess(inputs: Dict) -> Dict:
            text = inputs["text"]
            # Clean and prepare text
            cleaned = text.strip().lower()
            return {"cleaned_text": cleaned, "original": text}
        
        # Create postprocessing function
        def postprocess(inputs: Dict) -> Dict:
            response = inputs["response"]
            # Add formatting
            formatted = f"✨ {response.strip()} ✨"
            return {"formatted_response": formatted}
        
        # Create prompt
        prompt = PromptTemplate.from_template(
            "Summarize this text in one sentence: {cleaned_text}"
        )
        
        # Create the sequence
        sequence = RunnableSequence(
            RunnableLambda(preprocess),
            prompt,
            self.llm,
            RunnableLambda(lambda x: {"response": x.content}),
            RunnableLambda(postprocess)
        )
        
        # Run the sequence
        input_text = "The weather today is quite nice with sunshine and mild temperatures perfect for outdoor activities."
        print(f"Input: {input_text}")
        
        result = sequence.invoke({"text": input_text})
        print(f"Output: {result['formatted_response']}")
        print()
    
    def demo_parallel_execution(self):
        """
        Demo 5: Parallel Execution - Run multiple chains simultaneously
        """
        print("🔗 Demo 5: Parallel Execution")
        print("-" * 40)
        
        # Create different analysis chains
        sentiment_prompt = PromptTemplate.from_template(
            "What is the sentiment of this text (positive/negative/neutral)? {text}"
        )
        sentiment_chain = sentiment_prompt | self.llm
        
        length_prompt = PromptTemplate.from_template(
            "How would you categorize the length of this text (short/medium/long)? {text}"
        )
        length_chain = length_prompt | self.llm
        
        topic_prompt = PromptTemplate.from_template(
            "What is the main topic of this text in one word? {text}"
        )
        topic_chain = topic_prompt | self.llm
        
        # Create parallel execution
        parallel_chain = RunnableParallel({
            "sentiment": sentiment_chain,
            "length": length_chain,
            "topic": topic_chain
        })
        
        # Test text
        test_text = "I absolutely love the new features in this software update! The interface is so much cleaner and the performance improvements are remarkable."
        
        print(f"Analyzing text: {test_text[:50]}...")
        print("\nRunning parallel analysis...")
        
        start_time = time.time()
        results = parallel_chain.invoke({"text": test_text})
        end_time = time.time()
        
        print(f"\nResults (completed in {end_time - start_time:.2f}s):")
        for analysis_type, result in results.items():
            content = result.content if hasattr(result, 'content') else str(result)
            print(f"  {analysis_type.title()}: {content.strip()}")
        
        print()
    
    def demo_streaming_chain(self):
        """
        Demo 6: Streaming Chain - Process responses as they arrive
        """
        print("🔗 Demo 6: Streaming Chain")
        print("-" * 40)
        
        # Create streaming LLM
        streaming_llm = ChatAnthropic(
            model_name="claude-3-haiku-20240307",
            temperature=0.7,
            streaming=True
        )
        
        # Create simple chain for streaming
        prompt = PromptTemplate.from_template(
            "Write a short paragraph about {topic}. Make it engaging and informative."
        )
        
        chain = prompt | streaming_llm
        
        topic = "the future of space exploration"
        print(f"Topic: {topic}")
        print("Streaming response: ", end="", flush=True)
        
        # Stream the response
        try:
            for chunk in chain.stream({"topic": topic}):
                if hasattr(chunk, 'content'):
                    print(chunk.content, end="", flush=True)
                else:
                    print(str(chunk), end="", flush=True)
        except Exception as e:
            print(f"\nStreaming not available: {e}")
            # Fallback to regular execution
            result = chain.invoke({"topic": topic})
            print(result.content if hasattr(result, 'content') else str(result))
        
        print("\n")
    
    def run_all_demos(self):
        """
        Run all chain demonstrations
        """
        print("🎬 LangChain Chain Flow Demonstrations")
        print("=" * 60)
        print()
        
        demos = [
            self.demo_simple_chain,
            self.demo_sequential_chain,
            self.demo_router_chain,
            self.demo_runnable_sequence,
            self.demo_parallel_execution,
            self.demo_streaming_chain
        ]
        
        for i, demo in enumerate(demos, 1):
            try:
                demo()
                if i < len(demos):
                    input("Press Enter to continue to next demo...")
                    print()
            except KeyboardInterrupt:
                print("\nDemo interrupted by user")
                break
            except Exception as e:
                print(f"Demo failed: {str(e)}")
                continue
        
        print("✅ All demonstrations completed!")


def main():
    """Main demo function"""
    try:
        demo = ChainFlowDemo()
        demo.run_all_demos()
    except ValueError as e:
        print(f"❌ Setup error: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()