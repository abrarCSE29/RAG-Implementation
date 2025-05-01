from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import Config

class LLMManager:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            api_key=Config.GEMINI_API_KEY
        )
    
    def get_llm(self):
        return self.llm