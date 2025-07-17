# GPT Computer Agent

<div align="center">
  <p>
    <a href="https://github.com/KhulnaSoft/gpt-computer-agent">
      <img src="https://img.shields.io/github/stars/KhulnaSoft/gpt-computer-agent?style=social" alt="GitHub stars">
    </a>
    <a href="https://pypi.org/project/gpt-computer-agent/">
      <img src="https://img.shields.io/pypi/v/gpt-computer-agent" alt="PyPI">
    </a>
    <a href="https://github.com/KhulnaSoft/gpt-computer-agent/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/KhulnaSoft/gpt-computer-agent" alt="License">
    </a>
    <a href="https://discord.gg/qApFmWMt8x">
      <img src="https://img.shields.io/discord/1234567890?logo=discord" alt="Discord">
    </a>
  </p>

  <p>
    <strong>An extensible framework for building and deploying AI agents with web interface and tool integration.</strong>
  </p>
</div>

## Features

- 🚀 **Web Interface**: Modern, responsive web UI for interacting with AI agents
- 🛠️ **Tool Integration**: Easily extend with custom tools and functions
- 💾 **Persistence**: Conversation history and agent state management
- 🤖 **Multi-Model Support**: Works with OpenAI, Anthropic, and other LLM providers
- 🔌 **API & WebSocket**: Programmatic access and real-time updates
- 🧩 **Modular Architecture**: Clean, maintainable codebase with clear separation of concerns

## Quick Start

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- OpenAI API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KhulnaSoft/gpt-computer-agent.git
   cd gpt-computer-agent
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

### Running the Web Interface

```bash
uvicorn gpt_computer_agent.api.app:app --reload
```

Then open your browser to [http://localhost:8000](http://localhost:8000)

### Example Usage

```python
from gpt_computer_agent.core.agent import GPTChatAgent, AgentConfig
from gpt_computer_agent.core.tools import tool

# Define a custom tool
@tool
def calculate(expression: str) -> float:
    """Evaluate a mathematical expression."""
    return eval(expression)

# Configure and create agent
config = AgentConfig(
    name="MathAgent",
    description="An agent that helps with mathematical calculations",
    temperature=0.7
)

agent = GPTChatAgent(config)
agent.tool_registry.register(calculate)

# Run the agent
response = await agent.run("What is 2 + 2?")
print(response)
```

## Project Structure

```
gpt-computer-agent/
├── src/
│   └── gpt_computer_agent/
│       ├── api/                 # Web API and interface
│       │   ├── static/          # Static files (JS, CSS, images)
│       │   └── templates/       # HTML templates
│       ├── config/              # Configuration management
│       │   ├── __init__.py
│       │   ├── settings.py      # Application settings
│       │   └── logging.py       # Logging configuration
│       ├── core/                # Core functionality
│       │   ├── __init__.py
│       │   ├── agent.py         # Base agent implementation
│       │   └── tools.py         # Tool system
│       └── utils/               # Utility modules
│           ├── __init__.py
│           ├── storage.py       # Data persistence
│           └── common.py        # Common utilities
├── tests/                      # Test files
├── examples/                   # Example scripts
├── .env.example               # Example environment variables
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## Adding Custom Tools

You can extend the agent's capabilities by adding custom tools:

```python
from gpt_computer_agent.core.tools import tool

@tool
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather for a location.
    
    Args:
        location: The city or location to get weather for
        unit: Temperature unit ('celsius' or 'fahrenheit')
        
    Returns:
        Dictionary containing weather information
    """
    # Implementation here
    return {
        "location": location,
        "temperature": 22.5 if unit == "celsius" else 72.5,
        "unit": unit,
        "condition": "sunny"
    }

# Register the tool with your agent
agent.tool_registry.register(get_weather)
```

## API Documentation

The web interface includes interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) when running locally.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ by the KhulnaSoft team
- Inspired by the latest advancements in AI and language models
- Special thanks to all contributors and users
