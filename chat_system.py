import streamlit as st
from evidence import fetch_all_evidence
from llm_core import answer_with_constraints

st.set_page_config(page_title="Objective Scientific AI")

st.title("Objective Scientific AI")
st.caption("Evidence-based answers only. No speculation.")

question = st.text_input("Enter a scientific question")

if st.button("Ask") and question:
    try:
        with st.spinner("Gathering evidence..."):
            evidence = fetch_all_evidence(question)

        with st.spinner("Analyzing evidence..."):
            answer = answer_with_constraints(question, evidence)

        st.markdown(answer)

    except Exception:
        st.error(
            "Sorry — I don’t have enough information to give you a solid conclusion."
        )

