import streamlit as st
import requests



def show_chat():
    st.title("💬 Chat with Your Documents")
    
    # Initialize message history if not in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # # File uploader
    # uploaded_files = st.file_uploader(
    #     "Upload your documents", 
    #     accept_multiple_files=True,
    #     type=['txt', 'pdf']
    # )
    
    # if uploaded_files:
    #     if st.button("Process Documents"):
    #         with st.spinner("Processing documents..."):
    #             try:
    #                 files = [('files', file) for file in uploaded_files]
    #                 response = requests.post('http://127.0.0.1:5000/api/upload', files=files)
    #                 if response.status_code == 200:
    #                     st.success("Documents processed successfully!")
    #                 else:
    #                     st.error(f"Error processing documents: {response.json().get('error')}")
    #             except Exception as e:
    #                 st.error(f"Error uploading documents: {str(e)}")
    
    # Chat interface
    if "messages" in st.session_state:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
    
    if prompt := st.chat_input("Ask a question about your documents"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response through API call
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        'http://127.0.0.1:5000/api/query',
                        json={'question': prompt},
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        answer = response.json().get('response', '')
                        st.write(answer["result"])
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer["result"]
                        })
                    else:
                        st.error(f"Error: {response.json().get('error')}")
                except Exception as e:
                    st.error(f"Error communicating with server: {str(e)}")