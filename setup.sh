#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up GPT Computer Agent with uv...${NC}"

# Install uv if not already installed
if ! command -v uv &> /dev/null; then
    echo -e "${GREEN}Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add uv to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Ensure Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install the project in development mode with all dependencies
echo -e "${GREEN}Installing dependencies with uv...${NC}"
uv pip install --upgrade pip
uv pip install -e ".[dev]"

# Install rich explicitly
echo -e "${GREEN}Installing rich...${NC}"
uv pip install "rich>=14.0.0"

# Verify installation
echo -e "\n${GREEN}Verifying installation...${NC}"
python -c "from gpt_computer_agent import start; print('Import successful!')"

echo -e "\n${GREEN}Setup complete!${NC}"
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate"