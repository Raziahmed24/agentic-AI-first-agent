import streamlit as st
import asyncio
from main import run_sync, run_async, run_stream
import io
import sys

# 🌌 Dark theme setup
st.set_page_config(page_title="Agentic AI Interface", layout="centered")

# 💅 Custom CSS for Dark Mode
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .main {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
    }
    .stTextInput>div>div>input {
        background-color: #2e2e2e;
        color: white;
    }
    .stSelectbox>div>div>div {
        background-color: #2e2e2e;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧠 UI Layout
st.title("🤖 Agentic AI Interface")
st.write("Ask a question and choose your preferred mode:")

question = st.text_area("💬 Enter your question here:", "")
mode = st.selectbox("⚙️ Select mode:", ["sync", "async", "stream"])
ask_button = st.button("📤 Ask")

# 🔘 Ask button logic
if ask_button and question:
    with st.spinner("⏳ Thinking..."):
        output = io.StringIO()
        sys.stdout = output

        if mode == "sync":
            st.subheader("🔵 SYNC RESPONSE")
            run_sync(question)

        elif mode == "async":
            st.subheader("🟣 ASYNC RESPONSE")
            asyncio.run(run_async(question))

        elif mode == "stream":
            st.subheader("🟢 STREAM RESPONSE")
            run_stream(question)

        sys.stdout = sys.__stdout__
        # 🧾 Clean multiline response
        result = output.getvalue().strip()
        for paragraph in result.split("\n\n"):
            st.write(paragraph)
