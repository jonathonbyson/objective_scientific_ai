import streamlit as st
from evidence import fetch_all_evidence
from llm_core import answer_with_constraints

st.set_page_config(page_title="Objective Scientific AI", layout="centered")
st.markdown("<h1 style='text-align: center;'>Objective Scientific AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Evidence-based answers only. No speculation.</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    content = msg["content"]
    
    # Clean bolding without asterisks
    content = content.replace("**1. Evidence-based summary**", "<b>1. Evidence-based summary</b>")
    content = content.replace("**2. Bullet-point conclusions**", "<b>2. Bullet-point conclusions</b>")
    content = content.replace("**3. Explicit sources with links**", "<b>3. Explicit sources with links</b>")
    content = content.replace("**4. A confidence score**", "<b>4. A confidence score</b>")
    
    if msg["role"] == "user":
        st.markdown(
            f"<div style='text-align: right; margin: 15px 10px;'>"
            f"<span style='background:#B0D0FF; color:#1e3a8a; padding:14px 20px; border-radius:20px; "
            f"border-bottom-right-radius:4px; display:inline-block; max-width:80%; "
            f"box-shadow:0 2px 5px rgba(0,0,0,0.1); font-size:16px;'>{content}</span>"
            f"</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='text-align: left; margin: 15px 10px;'>"
            f"<span style='background:#E8E8E8; color:#333; padding:14px 20px; border-radius:20px; "
            f"border-bottom-left-radius:4px; display:inline-block; max-width:90%; "
            f"box-shadow:0 2px 5px rgba(0,0,0,0.1); font-size:16px;'>{content}</span>"
            f"</div>", unsafe_allow_html=True)

question = st.chat_input("Enter a scientific question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    q = st.session_state.messages[-1]["content"]
    with st.spinner("Gathering evidence..."):
        evidence = fetch_all_evidence(q)
    with st.spinner("Analyzing..."):
        answer = answer_with_constraints(q, evidence)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
