# python -m tests.gemini_agent_test

from dotenv import load_dotenv
from src.infrastructure.gemini_text_agent import GeminiTextAgent

# Load environment variables
load_dotenv("./env/.env")

# Initialize agent with empty tools list
agent = GeminiTextAgent()

# Set a custom thread ID
agent.set_thread_id("test_thread_123")

# Start interactive session
agent.interactive_session()