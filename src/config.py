import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check whether API key exists
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Project folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")