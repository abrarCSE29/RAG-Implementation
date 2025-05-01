import streamlit as st

def show_home():
    st.title("🤖 RAG System")
    
    st.markdown("""
    ### Welcome to the RAG (Retrieval-Augmented Generation) System
    
    This system allows you to:
    - Query documents using natural language
    - Get AI-powered responses based on your document context
    - Explore the power of retrieval-augmented generation
    
    To get started:
    1. Upload your documents in the chat section
    2. Ask questions about your documents
    3. Get accurate, context-aware responses
    """)