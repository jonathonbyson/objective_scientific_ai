import requests

HEADERS = {
    "User-Agent": "ObjectiveScientificAI/1.0"
}

# ---------- PUBMED ----------
def fetch_pubmed(query, max_results=5):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    data = r.json()

    ids = data.get("esearchresult", {}).get("idlist", [])
    if not ids:
        return ""

    return fetch_pubmed_details(ids)


def fetch_pubmed_details(pmids):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.text


# ---------- CROSSREF ----------
def fetch_crossref(query, max_results=5):
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": max_results}

    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()
    items = r.json().get("message", {}).get("items", [])

    texts = []
    for item in items:
        title = item.get("title", [""])[0]
        doi = item.get("DOI", "")
        texts.append(f"Title: {title}\nDOI: {doi}")

    return "\n".join(texts)


# ---------- SEMANTIC SCHOLAR ----------
def fetch_semantic_scholar(query, max_results=5):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,abstract,year,authors,url"
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=10)
    r.raise_for_status()

    data = r.json().get("data", [])
    texts = []
    for paper in data:
        texts.append(
            f"Title: {paper.get('title')}\n"
            f"Year: {paper.get('year')}\n"
            f"URL: {paper.get('url')}\n"
            f"Abstract: {paper.get('abstract')}"
        )

    return "\n\n".join(texts)


# ---------- AGGREGATOR ----------
def fetch_all_evidence(query):
    evidence = []
    try:
        evidence.append(fetch_pubmed(query))
    except:
        pass

    try:
        evidence.append(fetch_crossref(query))
    except:
        pass

    try:
        evidence.append(fetch_semantic_scholar(query))
    except:
        pass

    return "\n\n".join(evidence)

