import json
import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def embed(api_key: str, text: str):
    openai.api_key = api_key
    emb = openai.Embedding.create(model="text-embedding-3-small", input=text)
    return np.array(emb["data"][0]["embedding"])


def similarity(query_vec, vectors):
    return cosine_similarity([query_vec], vectors)[0]
