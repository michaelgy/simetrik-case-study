# use the console: python -m src.main
# use docker:
# 1. build the docker image: docker build -t flask-app .
# 2. run the docker image: docker run --name simetrik-remediation-agent -p 8080:8080 flask-app
from pathlib import Path
from dotenv import load_dotenv
import logging
from src.application.api_handler import APIHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load environment variables
project_root = Path(__file__).parent.parent
env_path = project_root / "env" / ".env"
load_dotenv(env_path)

# Create API handler and expose the app
apiHandler = APIHandler()
app = apiHandler.app

def main():
    apiHandler.run()

if __name__ == "__main__":
    main()
