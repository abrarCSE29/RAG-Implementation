from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA  # Updated import
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# Load documents
file_paths = [
    "data/doc1.txt",
    "data/doc2.txt",
    "data/doc3.txt",
]

documents = []
for file_path in file_paths:
    loader = TextLoader(file_path)
    documents.extend(loader.load())

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Generate embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(documents=chunks, embedding=embedding_model)

from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize the retriever and language model
retriever = vectorstore.as_retriever()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)

# Create a RetrievalQA chain using the new method
rag_pipeline = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"  # You can adjust the chain type as needed
)

# Ask a question
response = rag_pipeline.invoke("Who is Rafsan?")
print(response)