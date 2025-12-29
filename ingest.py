import arxiv
import os


def fetch_papers(topic: str, limit: int = 5, out_dir: str = "data/papers"):
    os.makedirs(out_dir, exist_ok=True)

    search = arxiv.Search(
        query=topic,
        max_results=limit,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    papers = []
    for result in search.results():
        pdf_path = os.path.join(out_dir, result.entry_id.split("/")[-1] + ".pdf")
        result.download_pdf(filename=pdf_path)
        papers.append(pdf_path)

    return papers
