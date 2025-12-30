import streamlit as st
from evidence import fetch_all_evidence
from llm_core import answer_with_constraints

st.set_page_config(page_title="Objective Scientific AI", layout="centered")

# Pastel colors + force-remove avatars completely
st.markdown("""
<style>
    .stApp { background-color: white; }
    
    /* Bubble styling */
    div[data-testid="stChatMessage"] {
        width: fit-content;
        max-width: 80%;
        padding: 12px 18px;
        border-radius: 20px;
        margin: 8px 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    div[data-testid="stChatMessage"][data-testid="chat-message-user"] {
        background-color: #B0D0FF;  /* pastel blue */
        color: #1e3a8a;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }
    div[data-testid="stChatMessage"][data-testid="chat-message-assistant"] {
        background-color: #E8E8E8;  /* pastel grey */
        color: #333333;
        margin-right: auto;
        border-bottom-left-radius: 4px;
    }
    
    /* Remove avatars completely */
    [data-testid="stChatMessage"] > div:first-child > div:first-child,
    [data-testid="stChatMessage"] img,
    [data-testid="avatar"] {
        display: none !important;
    }
    
    /* Ensure message content takes full width */
    [data-testid="stChatMessage"] > div:nth-child(2) {
        width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Objective Scientific AI")
st.caption("Evidence-based answers only. No speculation.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Enter a scientific question")

if question:
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    try:
        with st.spinner("Gathering evidence..."):
            evidence = fetch_all_evidence(question)
        with st.spinner("Analyzing evidence..."):
            answer = answer_with_constraints(question, evidence)
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    
    except Exception:
        error_msg = "Sorry — I don’t have enough information to give you a solid conclusion."
        with st.chat_message("assistant"):
            st.markdown(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
