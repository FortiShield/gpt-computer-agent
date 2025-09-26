#!/usr/bin/env python3
"""Simple test script to verify Aideck setup"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from aideck import __version__
    print(f"✅ Aideck version: {__version__}")

    # Test basic imports
    from aideck.start import start
    print("✅ Core module imports successful")

    from aideck.agentic import Agent
    print("✅ Agent module imports successful")

    from aideck.classes import BaseClass
    print("✅ Classes module imports successful")

    print("\n🎉 All basic imports successful!")
    print("🚀 You can now run: python -m aideck")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run: ./setup.sh")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
