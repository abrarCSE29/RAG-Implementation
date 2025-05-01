import streamlit as st
from app.web.pages.home import show_home
from app.web.pages.chat import show_chat
from app.web.components.sidebar import show_sidebar

st.set_page_config(
    page_title="RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Show sidebar
    show_sidebar()
    
    # Display selected page
    if st.session_state.current_page == "Home":
        show_home()
    elif st.session_state.current_page == "Chat":
        show_chat()

if __name__ == "__main__":
    main()