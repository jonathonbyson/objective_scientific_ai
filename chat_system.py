# chat_system.py
import os
import streamlit as st
import requests
from llm_core import answer_with_constraints
from xml.etree import ElementTree as ET

st.set_page_config(page_title="Objective Scientific AI", layout="wide")
st.title("Objective Scientific AI")
st.write("Ask a scientific question and get evidence-based answers with sources.")

question = st.text_input("Enter your scientific question:")

if question:
    st.info(f"Fetching top evidence for: '{question}' ...")
    
    try:
        # Fetch top 5 PubMed article IDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": question,
            "retmode": "json",
            "retmax": 5
        }
        search_resp = requests.get(search_url, params=search_params)
        search_data = search_resp.json()
        pmids = search_data["esearchresult"]["idlist"]
        
        evidence_texts = []
        sources = []
        
        for pmid in pmids:
            fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {"db": "pubmed", "id": pmid, "retmode": "xml"}
            fetch_resp = requests.get(fetch_url, params=fetch_params)
            
            # Parse XML to extract abstract
            root = ET.fromstring(fetch_resp.text)
            abstract_texts = []
            for abstract in root.findall(".//AbstractText"):
                abstract_texts.append("".join(abstract.itertext()))
            combined_abstract = "\n".join(abstract_texts)
            
            if combined_abstract.strip():
                evidence_texts.append(combined_abstract)
                sources.append(f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
        
        combined_evidence = "\n\n".join(evidence_texts)
        
        st.info("Generating evidence-based answer...")
        answer = answer_with_constraints(question, combined_evidence)
        
        st.subheader("Answer:")
        st.write(answer)
        
        st.subheader("Sources:")
        for link in sources:
            st.write(f"[{link}]({link})")
            
    except Exception as e:
        st.error(f"Error fetching evidence or generating answer: {e}")

