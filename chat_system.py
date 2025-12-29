# chat_system.py
import streamlit as st
from llm_core import answer_with_constraints

# Set page title
st.set_page_config(page_title="Objective Scientific AI", page_icon="🧪")
st.title("Objective Scientific AI")
st.write("Ask a scientific question and get evidence-based answers with sources.")

# Input field for the scientific question
question = st.text_input("Enter your scientific question:")

# Example evidence chunks for demonstration
# Each dict must have 'text', 'title', 'link'
# Replace with actual evidence retrieval logic
example_evidence = [
    {
        "title": "Fasting and Metabolic Health",
        "link": "https://www.ncbi.nlm.nih.gov/pubmed/123456",
        "text": "Intermittent fasting improves insulin sensitivity and reduces body fat in adults."
    },
    {
        "title": "Effects of Fasting on Longevity",
        "link": "https://www.sciencedirect.com/science/article/pii/7890123",
        "text": "Caloric restriction and fasting may extend lifespan in animal studies, with some translational evidence in humans."
    }
]

if question:
    st.info(f"Fetching evidence for: {question} ...")
    
    # Here you would replace example_evidence with your actual evidence-fetching code
    evidence_chunks = example_evidence

    st.info("Generating summary answer...")
    
    answer = answer_with_constraints(question, evidence_chunks)
    
    st.subheader("Summary Answer")
    st.write(answer)

    st.subheader("Sources")
    if evidence_chunks:
        for idx, ev in enumerate(evidence_chunks, 1):
            title = ev.get("title", "Untitled")
            link = ev.get("link", "#")
            st.markdown(f"{idx}. [{title}]({link})")
    else:
        st.write("No sources available.")

