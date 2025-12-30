import streamlit as st
from llm_core import answer_with_constraints

# Example dummy LLM function (replace with your Nebius call)
def call_llm(prompt: str) -> str:
    # Replace this with the actual API call to Nebius
    # This is a placeholder to test the app
    return f"""Answer: This is a dummy answer for the prompt: {prompt}

Actionable:
- Follow instructions carefully.
- Review sources provided.

Sources:
Dummy Source: https://example.com
"""

# ------------------------
# Streamlit App
# ------------------------
st.set_page_config(page_title="Facet-Based LLM Assistant", layout="wide")
st.title("Facet-Based LLM Assistant")

# Sidebar input
with st.sidebar:
    user_input = st.text_input("Enter topic or question:", "")
    st.markdown("### Optional Context")
    context = st.text_area("Provide additional context (optional):", "")

# Example sources (replace with real sources)
sources = [
    {"name": "Health Source", "url": "https://www.healthsource.com"},
    {"name": "Science Journal", "url": "https://www.sciencejournal.org"},
]

if user_input:
    st.info("Generating answer...")

    # Call llm_core
    output = answer_with_constraints(user_input, context, sources, 
call_llm)

    st.subheader("Answer")
    st.markdown(output["answer"])

    st.subheader("Actionable Tips")
    if output["actionable_summary"] and output["actionable_summary"] != 
"No actionable advice.":
        for line in output["actionable_summary"].splitlines():
            with st.expander(line.strip("- ")):
                st.write(line)
    else:
        st.write("No actionable advice.")

    st.subheader("Sources Used")
    if output["sources"] and output["sources"] != "None used.":
        for src in output["sources"].splitlines():
            st.write(f"- {src}")
    else:
        st.write("No sources used.")

