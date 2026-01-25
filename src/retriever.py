from src.vectorstore import get_vectorstore

def retrieve(query: str, k: int = 5):
    """
    Retrieve top-k relevant chunks from Chroma for a given query.
    Uses MMR to avoid returning many near-duplicate chunks from the same document.
    Returns LangChain Document objects (text + metadata).
    """
    vs = get_vectorstore()

    # MMR improves diversity and helps pull the "right section" from the right doc
    # fetch_k controls how many candidates to consider before selecting top-k diverse results
    fetch_k = max(20, k * 4)

    try:
        return vs.max_marginal_relevance_search(query, k=k, fetch_k=fetch_k)
    except Exception:
        # Fallback for older/alternate vectorstore implementations
        return vs.similarity_search(query, k=k)
