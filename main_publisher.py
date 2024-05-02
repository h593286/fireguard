
import time
from dotenv import load_dotenv
from src.broker.publish_runner import run_scheduling

load_dotenv()

if __name__ == "__main__":
    print("starting scheduler")
    run_scheduling()