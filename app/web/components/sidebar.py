import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.title("Navigation")
        
        # Navigation buttons
        if st.button("🏠 Home"):
            st.session_state.current_page = "Home"
        if st.button("💬 Chat"):
            st.session_state.current_page = "Chat"
        
        st.markdown("---")
        st.markdown("""
        ### About
        This RAG system uses:
        - LangChain for document processing
        - FAISS for vector storage
        - Gemini Pro for text generation
        """)