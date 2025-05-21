# python -m src.main

from pathlib import Path
from dotenv import load_dotenv
from src.application.api_handler import APIHandler

def main():
    # Get the absolute path to the project root directory
    project_root = Path(__file__).parent.parent
    
    # Load environment variables using absolute path
    env_path = project_root / "env" / ".env"
    load_dotenv(env_path)
    
    # Create and run apiHandler handler
    apiHandler = APIHandler()
    apiHandler.run()

if __name__ == "__main__":
    main() 