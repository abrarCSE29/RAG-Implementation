from __future__ import annotations

import streamlit as st

from app.web.api_client import APIClient


def show_chat() -> None:
    client = APIClient(st.session_state.api_base_url, st.session_state.get("api_key"))

    st.markdown("# Chat with your documents")
    st.caption("Ask questions, inspect retrieved chunks, and show source-backed answers.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about the indexed documents")
    if not question:
        return

    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and generating an answer..."):
            try:
                result = client.query(question)
                answer = result.get("answer", "")
                sources = result.get("sources", [])
                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.markdown(f"**{source['source_name']}**  ")
                            st.code(source.get("text", ""), language="text")
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                st.error(f"Request failed: {exc}")