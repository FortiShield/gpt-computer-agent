"""
Basic usage example for the GPT Computer Agent.

This example demonstrates how to create an agent, register tools, and interact with it.
"""
import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from gpt_computer_agent.core.agent import GPTChatAgent, AgentConfig
from gpt_computer_agent.core.tools import tool, ToolRegistry
from gpt_computer_agent.config.settings import settings
from gpt_computer_agent.utils.common import setup_logging

# Configure logging
setup_logging(log_level="DEBUG")

# Define some example tools
@tool
def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """
    Search the web for information.
    
    Args:
        query: The search query.
        max_results: Maximum number of results to return.
        
    Returns:
        List of search results with 'title', 'url', and 'snippet'.
    """
    # In a real implementation, this would call a search API
    print(f"Searching for: {query} (max results: {max_results})")
    return [
        {
            "title": f"Result {i+1} for '{query}'",
            "url": f"https://example.com/result/{i+1}",
            "snippet": f"This is a sample result for '{query}'. This would contain a snippet of the search result."
        }
        for i in range(min(max_results, 3))
    ]

@tool
def calculate(expression: str) -> float:
    """
    Evaluate a mathematical expression.
    
    Args:
        expression: The mathematical expression to evaluate.
        
    Returns:
        The result of the evaluation.
    """
    # In a real implementation, use a safe evaluation
    print(f"Calculating: {expression}")
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_weather(location: str, unit: str = "celsius") -> Dict[str, str]:
    """
    Get the current weather for a location.
    
    Args:
        location: The city or location to get weather for.
        unit: Temperature unit ('celsius' or 'fahrenheit').
        
    Returns:
        Weather information.
    """
    print(f"Getting weather for {location} in {unit}")
    return {
        "location": location,
        "temperature": 22.5 if unit == "celsius" else 72.5,
        "unit": unit,
        "condition": "sunny",
        "humidity": 45,
        "wind_speed": 10.2,
        "forecast": "clear skies"
    }

async def main():
    # Configure the agent
    config = AgentConfig(
        name="Demo Agent",
        description="A demo agent with web search, calculator, and weather tools.",
        llm_provider=settings.LLM_PROVIDER,
        temperature=0.7,
        verbose=True
    )
    
    # Create the agent
    agent = GPTChatAgent(config)
    
    # Register tools
    agent.tool_registry.register(search_web)
    agent.tool_registry.register(calculate)
    agent.tool_registry.register(get_weather)
    
    # Example conversation
    print("Demo GPT Computer Agent")
    print("Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Get agent response
            print("\nAgent is thinking...")
            response = await agent.run(user_input)
            
            # Display response
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())
