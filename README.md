# RAG System

This project implements a **Retrieval-Augmented Generation (RAG)** system using the LangChain framework. The system combines document retrieval with generative AI to answer user queries based on a set of documents. It leverages state-of-the-art models and tools for document loading, text splitting, vector storage, and generative AI.

## Features

- **Document Loading**: Load text documents from local files.
- **Text Splitting**: Split documents into manageable chunks for efficient processing.
- **Vector Storage**: Use FAISS for storing and retrieving document embeddings.
- **Generative AI**: Use a generative language model to answer user queries based on retrieved documents.

---

## Frameworks and Libraries Used

### 1. **LangChain**
   - **Document Loaders**: [`TextLoader`](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
   - **Text Splitter**: [`RecursiveCharacterTextSplitter`](https://python.langchain.com/docs/modules/data_connection/text_splitters/)
   - **Vector Store**: [`FAISS`](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
   - **Chains**: [`RetrievalQA`](https://python.langchain.com/docs/modules/chains/)

### 2. **Hugging Face**
   - **Embeddings**: [`HuggingFaceEmbeddings`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) using the `sentence-transformers/all-MiniLM-L6-v2` model.

### 3. **Google Generative AI**
   - **Language Model**: [`ChatGoogleGenerativeAI`](https://cloud.google.com/generative-ai) using the `gemini-1.5-flash` model.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abrarCSE29/RAG-Implementation.git
   cd RAG-Implementation
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Run server :
   ```bash
   python3 run.py
   ```

4. Run streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
  
