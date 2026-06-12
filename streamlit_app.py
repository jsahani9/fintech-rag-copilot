import os
import requests
import streamlit as st

# If you change FastAPI host/port later (Docker etc.), you can override via env var
API_URL = os.getenv("API_URL", "http://api:8000/ask")


st.set_page_config(page_title="FinTech RAG Copilot", page_icon="🏦", layout="wide")

st.title("🏦 FinTech RAG Copilot")
st.caption("Ask questions about OSFI documents. Answers are grounded with citations like [1], [2].")

with st.sidebar:
    st.header("Settings")
    k = st.slider("Top-k retrieved chunks", min_value=1, max_value=15, value=8)
    st.text_input("API URL", value=API_URL, key="api_url_help", disabled=True)
    st.markdown("**Tip:** Keep FastAPI running: `uvicorn app.main:app --reload`")

question = st.text_area(
    "Your question",
    placeholder="e.g., Summarize OSFI expectations for cyber risk management.",
    height=120,
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_btn = st.button("Ask", type="primary")
with col2:
    clear_btn = st.button("Clear")

if clear_btn:
    st.session_state.clear()
    st.rerun()

if ask_btn:
    q = (question or "").strip()
    if not q:
        st.warning("Type a question first.")
    else:
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"question": q, "k": k},
                    timeout=180,
                )
                if resp.status_code != 200:
                    st.error(f"API error {resp.status_code}: {resp.text}")
                else:
                    data = resp.json()
                    st.markdown("### Answer")
                    st.markdown(data.get("answer", ""))

                    sources = data.get("sources", [])
                    if sources:
                        with st.expander("Sources"):
                            for s in sources:
                                st.write(f"- **{s.get('source', 'unknown')}** (page {s.get('page', 'unknown')})")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach API at {API_URL}. Is FastAPI running?\n\nDetails: {e}")
