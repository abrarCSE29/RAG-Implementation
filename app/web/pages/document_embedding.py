from __future__ import annotations

import streamlit as st

from app.web.api_client import APIClient


def show_document_embedding() -> None:
    client = APIClient(st.session_state.api_base_url, st.session_state.get("api_key"))

    st.markdown("# Document ingestion")
    st.caption("Upload mixed-format documents and inspect the indexed corpus.")

    uploaded_files = st.file_uploader(
        "Choose documents",
        accept_multiple_files=True,
        type=["txt", "md", "rst", "rtf", "pdf", "docx", "pptx", "html", "htm", "csv", "json", "xml"],
    )

    if uploaded_files:
        st.write(f"{len(uploaded_files)} file(s) ready for ingestion")
        if st.button("Upload to API", type="primary"):
            try:
                with st.spinner("Uploading and indexing..."):
                    result = client.upload(uploaded_files)
                    st.success(f"Indexed {result.get('document_count', 0)} document(s) and {result.get('chunk_count', 0)} chunks.")
                    st.json(result)
            except Exception as exc:
                st.error(f"Upload failed: {exc}")

    st.markdown("---")
    st.subheader("Indexed documents")
    try:
        documents = client.documents().get("documents", [])
        if documents:
            document_options = {document["source_name"]: document["document_id"] for document in documents}
            selected_source = st.selectbox("Filter chunks by document", ["All documents", *document_options.keys()])
            selected_document_id = document_options.get(selected_source)

            chunks_response = client.chunks(selected_document_id)
            chunks = chunks_response.get("chunks", [])

            for document in documents:
                with st.expander(f"{document['source_name']} ({document['chunk_count']} chunks)"):
                    st.json(document)

            st.subheader("Chunk browser")
            if chunks:
                for chunk in chunks:
                    chunk_label = f"{chunk['source_name']} | Chunk {chunk.get('chunk_index', '?')} | {chunk['chunk_id']}"
                    with st.expander(chunk_label):
                        st.write(chunk.get("text", ""))
                        st.json({k: v for k, v in chunk.items() if k != "text"})
            else:
                st.info("No chunks found for the selected document.")
        else:
            st.info("No documents are indexed yet.")
    except Exception as exc:
        st.error(f"Could not load the document list: {exc}")

    st.markdown("---")
    st.subheader("Demo corpus")
    st.write("Use the generated 10-file sample corpus for a reliable showcase dataset of about 11 MB.")
