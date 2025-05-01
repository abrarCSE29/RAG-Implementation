from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.settings import Config

class DocumentManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def load_documents(self, file_paths):
        documents = []
        for file_path in file_paths:
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        return documents
    
    def split_documents(self, documents):
        return self.text_splitter.split_documents(documents)