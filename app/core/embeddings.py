from langchain_huggingface import HuggingFaceEmbeddings
from app.config.settings import Config

class EmbeddingManager:
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name=Config.EMBEDDING_MODEL
        )
    
    def get_embeddings(self, texts):
        return self.model.embed_documents(texts)