import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = "gemini-1.5-flash"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50