from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config.settings import Config
import os

class DocumentManager:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
    
    def load_documents(self, file_paths):
        documents = []
        for file_path in file_paths:
            # Get file extension
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()
            
            try:
                # Choose loader based on file extension
                if ext == '.pdf':
                    loader = PyPDFLoader(file_path)
                elif ext == '.txt':
                    loader = TextLoader(file_path)
                else:
                    raise ValueError(f"Unsupported file format: {ext}")
                
                documents.extend(loader.load())
            except Exception as e:
                raise Exception(f"Error loading {file_path}: {str(e)}")
                
        return documents
    
    def split_documents(self, documents):
        return self.text_splitter.split_documents(documents)