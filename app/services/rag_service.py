from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from app.core.document_loader import DocumentManager
from app.core.embeddings import EmbeddingManager
from app.core.llm import LLMManager

class RAGService:
    def __init__(self):
        self.document_manager = DocumentManager()
        self.embedding_manager = EmbeddingManager()
        self.llm_manager = LLMManager()
        self.vectorstore = None
        self.rag_pipeline = None
        
    def initialize(self, file_paths):
        # Load and process documents
        documents = self.document_manager.load_documents(file_paths)
        chunks = self.document_manager.split_documents(documents)
        
        # Create vector store
        self.vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=self.embedding_manager.model
        )
        
        # Initialize RAG pipeline
        retriever = self.vectorstore.as_retriever()
        self.rag_pipeline = RetrievalQA.from_chain_type(
            llm=self.llm_manager.get_llm(),
            retriever=retriever,
            chain_type="stuff"
        )
    
    def query(self, question):
        if not self.rag_pipeline:
            raise ValueError("RAG pipeline not initialized")
        return self.rag_pipeline.invoke(question)