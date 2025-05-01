import streamlit as st
import requests
from pathlib import Path

def show_document_embedding():
    st.title("📚 Document Embedding")
    
    # Document upload section
    st.header("Upload Documents")
    st.markdown("""
    Upload your documents to embed them into the system. 
    Supported formats: `.txt`, `.pdf`
    """)
    
    uploaded_files = st.file_uploader(
        "Choose documents to embed",
        accept_multiple_files=True,
        type=['txt', 'pdf']
    )
    
    if uploaded_files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📁 {len(uploaded_files)} files selected")
        with col2:
            if st.button("Embed Documents", type="primary"):
                with st.spinner("Processing and embedding documents..."):
                    try:
                        # Prepare files for upload
                        files = [('files', file) for file in uploaded_files]
                        
                        # Make API request to embed documents
                        response = requests.post(
                            'http://127.0.0.1:5000/api/embed',
                            files=files
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"✅ Successfully embedded {len(uploaded_files)} documents!")
                            
                            # Show embedding details
                            with st.expander("View Details"):
                                st.json(result)
                        else:
                            st.error(f"❌ Error: {response.json().get('error', 'Unknown error occurred')}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Show existing embedded documents
    st.header("Embedded Documents")
    try:
        response = requests.get('http://127.0.0.1:5000/api/documents')
        if response.status_code == 200:
            documents = response.json().get('documents', [])
            if documents:
                st.write(f"Found {len(documents)} embedded documents:")
                for doc in documents:
                    st.text(f"📄 {doc}")
            else:
                st.info("No documents have been embedded yet.")
        else:
            st.warning("Unable to fetch embedded documents.")
    except Exception as e:
        st.error(f"Error fetching document list: {str(e)}")

    # Add some helpful information
    st.markdown("""
    ---
    ### About Document Embedding
    
    Document embedding converts your text documents into vector representations 
    that can be efficiently searched and queried. The process:
    
    1. Uploads documents to the system
    2. Processes and splits documents into chunks
    3. Generates embeddings using advanced language models
    4. Stores vectors for quick retrieval
    
    Your embedded documents will be available for querying in the chat interface.
    """)
