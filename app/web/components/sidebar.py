from __future__ import annotations

import streamlit as st


def show_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Production RAG")
        st.caption("FastAPI + Qdrant + local Hugging Face LLM")

        st.session_state.api_base_url = st.text_input(
            "API Base URL",
            value=st.session_state.get("api_base_url", "http://127.0.0.1:8000"),
            help="Set the FastAPI server location used by the UI.",
        )
        st.session_state.api_key = st.text_input(
            "API Key",
            value=st.session_state.get("api_key", "dev-api-key"),
            type="password",
            help="Matches the X-API-Key expected by the backend.",
        )

        st.markdown("---")

        pages = ["Home", "Chat", "Ingest"]
        selection = st.radio("Navigate", pages, index=pages.index(st.session_state.current_page))
        st.session_state.current_page = selection

        st.markdown("---")
        st.markdown(
            """
            ### Included in the showcase
            - Multi-format ingestion
            - Qdrant vector search
            - CPU-friendly local generation
            - API key protection
            - Feature flags and metrics
            """
        )