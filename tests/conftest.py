"""Test configuration and fixtures for Aideck"""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from pathlib import Path

# Test configuration
pytest_plugins = ["pytest_asyncio"]

# Test data paths
TEST_DATA_DIR = Path(__file__).parent / "data"
TEST_FIXTURES_DIR = Path(__file__).parent / "fixtures"

# Ensure test directories exist
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_FIXTURES_DIR.mkdir(exist_ok=True)


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir(tmp_path) -> Path:
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def test_config():
    """Basic test configuration."""
    return {
        "debug": False,
        "log_level": "INFO",
        "database_url": "sqlite:///:memory:",
        "secret_key": "test-secret-key-for-unit-tests",
    }


@pytest.fixture
def sample_text():
    """Sample text for testing."""
    return "This is a sample text for testing purposes. It contains multiple sentences and should be long enough for meaningful tests."


@pytest.fixture
def sample_json():
    """Sample JSON data for testing."""
    return {
        "id": "test-123",
        "name": "Test Item",
        "description": "A test item for unit testing",
        "active": True,
        "tags": ["test", "unit", "sample"]
    }
