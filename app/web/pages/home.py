from __future__ import annotations

import streamlit as st

from app.web.api_client import APIClient


def show_home() -> None:
    client = APIClient(st.session_state.api_base_url, st.session_state.get("api_key"))

    st.markdown("# Production RAG")
    st.markdown(
        """
        A showcase-ready document intelligence system built for production interviews:
        FastAPI backend, Qdrant vector storage, local Hugging Face generation, and modular feature flags.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Deployment", "Docker-ready")
    with col2:
        st.metric("Input types", "10+ formats")
    with col3:
        st.metric("Auth", "API key")

    try:
        health = client.health()
        features = health.get("features", {})
        st.success(f"Backend online: {health.get('app_name', 'RAG')} ({health.get('environment', 'unknown')})")
        feature_cols = st.columns(3)
        feature_names = ["ingestion", "rag", "reranking", "citations", "api_key_auth", "ocr"]
        for index, name in enumerate(feature_names):
            with feature_cols[index % 3]:
                st.write(f"**{name.replace('_', ' ').title()}**: {'on' if features.get(name) else 'off'}")

        try:
            metrics = client.metrics()
            metric_cols = st.columns(4)
            metric_values = [
                ("Requests", metrics.get("requests_total", 0)),
                ("Queries", metrics.get("queries_total", 0)),
                ("Ingestions", metrics.get("ingestions_total", 0)),
                ("Last latency ms", metrics.get("last_request_ms", 0.0)),
            ]
            for column, (label, value) in zip(metric_cols, metric_values, strict=True):
                with column:
                    st.metric(label, value)
        except Exception:
            st.info("Metrics are available after the first authenticated request.")
    except Exception as exc:
        st.warning(f"Backend not reachable yet: {exc}")

    st.markdown("---")
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Why this version stands out")
        st.write(
            """
            - Handles mixed document formats including office files, text, tables, and structured data.
            - Uses deterministic IDs for de-duplication when enabled.
            - Supports turning capabilities on and off from config without code changes.
            - Ships with tests, Docker, and a generated demo corpus for interviewing.
            """
        )
    with right:
        st.subheader("Suggested demo flow")
        st.write(
            """
            1. Start the API and Qdrant.
            2. Upload the sample corpus or your own docs.
            3. Ask a question and inspect sources.
            4. Show the metrics endpoint and feature flags.
            """
        )