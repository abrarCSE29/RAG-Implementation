from __future__ import annotations

import streamlit as st

from app.web.components.sidebar import show_sidebar
from app.web.pages.chat import show_chat
from app.web.pages.document_embedding import show_document_embedding
from app.web.pages.home import show_home

st.set_page_config(
    page_title="Production RAG",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    show_sidebar()

    if st.session_state.current_page == "Home":
        show_home()
    elif st.session_state.current_page == "Chat":
        show_chat()
    elif st.session_state.current_page == "Ingest":
        show_document_embedding()


if __name__ == "__main__":
    main()