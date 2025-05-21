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
    print("Starting Api Handler server...")
    print("Server running at: http://127.0.0.1:5001")
    print("Use ngrok to expose the api: ngrok http 5001")
    apiHandler.run()

if __name__ == "__main__":
    main() 