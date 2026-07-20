import json
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.config import DATA_DIR, CHROMA_DIR

# Embedding model
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Chroma client
client = chromadb.PersistentClient(path=CHROMA_DIR)


def load_data():
    """Load sports facts from JSON."""
    with open(f"{DATA_DIR}/sports_facts.json", "r", encoding="utf-8") as file:
        return json.load(file)


def populate_database():
    """Populate ChromaDB with sports facts."""

    data = load_data()

    # Delete old collection if it exists
    try:
        client.delete_collection("sports_facts")
    except Exception:
        pass

    new_collection = client.get_or_create_collection(
        name="sports_facts",
        embedding_function=embedding_function
    )

    for idx, item in enumerate(data):
        new_collection.add(
            ids=[str(idx)],
            documents=[item["fact"]],
            metadatas=[{"sport": item["sport"]}]
        )

    print("Database created successfully!")

    return new_collection


# Create or load collection
collection = client.get_or_create_collection(
    name="sports_facts",
    embedding_function=embedding_function
)

# Populate automatically if empty
if collection.count() == 0:
    print("ChromaDB is empty. Populating...")
    collection = populate_database()


def search_facts(query, sport=None, n_results=5):
    """Search sports facts."""

    if sport:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"sport": sport}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

    return results