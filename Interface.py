import streamlit as st
from ai_agent_llama import tool_calling
from streamlit_chat import message  # Optional, adds nice chat bubbles
import pkg_resources
import streamlit as st


st.set_page_config(page_title="Stock Market Assistant", page_icon="📈", layout="wide")

# ---- Sidebar Branding ----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910791.png", width=80)
    st.markdown("### 💹 Stock Analyst AI")
    st.markdown("Ask anything about stocks, companies, or market data.")
    st.markdown("---")
    st.markdown("Built with 💙 using LLaMA-3 + Together AI")

# ---- Main Header ----
st.title("📊 Stock Market Assistant")
st.caption("AI-Powered Answers for Live Stock Data & Company Insights")

# ---- Session State Setup ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- Display Chat History ----
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    message(msg["content"], is_user=is_user, key=str(i))

# ---- Chat Input ----
with st.container():
    st.markdown("### 💬 Ask a question")
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Type your query here...", key="user_input", label_visibility="collapsed")
    with col2:
        submit = st.button("Send")

# ---- Handle Input ----
if submit and user_input:
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Construct full conversation history (convert "bot" to "assistant" if needed)
    conversation_history = [
        {"role": msg["role"] if msg["role"] != "bot" else "assistant", "content": msg["content"]}
        for msg in st.session_state.messages
    ]

    with st.spinner("Thinking..."):
        reply = tool_calling(user_input, memory=conversation_history)  # Pass memory context

    # Add assistant reply to session
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
