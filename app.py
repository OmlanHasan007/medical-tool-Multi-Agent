"""
Streamlit Web UI for the Multi-Tool Medical Agent.
Run with: streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="Multi-Tool Medical Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

from main_agent import build_agent, run_with_memory
from utils.pdf_report import generate_report

st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; }
    .sidebar-title { font-size: 1.3rem; font-weight: 700; color: #1a6b9a; }
    .tool-badge {
        display: inline-block;
        background: #e8f4fd;
        color: #1a6b9a;
        border-radius: 8px;
        padding: 2px 8px;
        font-size: 0.75rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "agent" not in st.session_state:
    with st.spinner("Initialising agent..."):
        st.session_state.agent = build_agent(verbose=False)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "raw_history" not in st.session_state:
    st.session_state.raw_history = []

# Sidebar
with st.sidebar:
    st.markdown('<p class="sidebar-title">🧠 Medical Agent</p>', unsafe_allow_html=True)
    st.caption("Powered by Claude 3.5 Sonnet · LangChain")
    st.divider()

    st.markdown("**Available Tools**")
    tools = [
        ("🫀", "Heart Disease DB"),
        ("🎗️", "Cancer DB"),
        ("🩸", "Diabetes DB"),
        ("🌬️", "Asthma DB"),
        ("🫘", "Kidney Disease DB"),
        ("🌐", "Medical Web Search"),
    ]
    for icon, name in tools:
        st.markdown(f'<span class="tool-badge">{icon} {name}</span>', unsafe_allow_html=True)

    st.divider()

    st.markdown("**Export Session**")
    if st.button("📄 Download PDF Report", use_container_width=True):
        if not st.session_state.raw_history:
            st.warning("No conversation to export yet.")
        else:
            with st.spinner("Generating PDF..."):
                try:
                    summary_result = run_with_memory(
                        st.session_state.agent,
                        "Please provide a 2-3 sentence summary of our conversation so far, focusing on the medical topics discussed and key findings.",
                        st.session_state.chat_history
                    )
                except Exception:
                    summary_result = ""

                pdf_path = generate_report(
                    chat_history=st.session_state.raw_history,
                    session_summary=summary_result,
                )

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Save PDF",
                    data=f.read(),
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    use_container_width=True,
                )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.raw_history = []
        st.session_state.agent = build_agent(verbose=False)
        st.rerun()

    st.divider()
    st.caption("⚠️ **Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice.")

# Main chat
st.title("🧠 Multi-Tool Medical Agent")
st.caption("Ask questions about Heart Disease, Cancer, Diabetes, Asthma, Kidney Disease datasets or general medical topics.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def handle_query(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.raw_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = run_with_memory(
                    st.session_state.agent,
                    prompt,
                    st.session_state.chat_history
                )
                # Update LangChain chat history
                st.session_state.chat_history.append(HumanMessage(content=prompt))
                st.session_state.chat_history.append(AIMessage(content=response))
                # Keep last 20 messages
                if len(st.session_state.chat_history) > 20:
                    st.session_state.chat_history = st.session_state.chat_history[-20:]
            except Exception as e:
                response = f"⚠️ Error: {e}"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.raw_history.append({"role": "assistant", "content": response})

if prompt := st.chat_input("Ask a medical question..."):
    handle_query(prompt)

# Example queries when chat is empty
if not st.session_state.messages:
    st.divider()
    st.subheader("💡 Example Queries")
    examples = [
        ("🫀 Heart",   "Show the average age and cholesterol of heart disease patients."),
        ("🎗️ Cancer",  "What percentage of cancer patients are female?"),
        ("🩸 Diabetes","What is the average glucose level of diabetic patients?"),
        ("🌬️ Asthma",  "How many asthma patients are in the dataset?"),
        ("🫘 Kidney",  "What is the distribution of kidney disease diagnoses?"),
        ("🌐 Web",     "What are the symptoms and treatments for hypertension?"),
    ]
    cols = st.columns(2)
    for i, (label, query) in enumerate(examples):
        with cols[i % 2]:
            if st.button(f"{label}: {query}", key=f"ex_{i}", use_container_width=True):
                handle_query(query)
                st.rerun()