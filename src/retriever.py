from src.vectorstore import get_vectorstore

def retrieve(query: str, k: int = 8):
    vs = get_vectorstore()
    fetch_k = max(30, k * 6)
    try:
        return vs.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k, lambda_mult=0.7)
    except Exception:
        return vs.similarity_search(query, k=k)
