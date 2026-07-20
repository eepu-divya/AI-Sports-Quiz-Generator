"""
search.py
Handles Retrieval-Augmented Generation (RAG) search using ChromaDB.
"""

from src.database import collection


def search_context(query: str, top_k: int = 3):
    """
    Retrieve the most relevant documents from ChromaDB.

    Args:
        query (str): Search query.
        top_k (int): Number of documents to retrieve.

    Returns:
        str: Combined context.
    """

    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results.get("documents", [])

        if documents and len(documents[0]) > 0:
            return "\n".join(documents[0])

        return ""

    except Exception as e:
        print("Search Error:", e)
        return ""