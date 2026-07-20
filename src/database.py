import json
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from src.config import DATA_DIR, CHROMA_DIR

# Embedding model
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create Chroma client
client = chromadb.PersistentClient(path=CHROMA_DIR)

# Create collection
collection = client.get_or_create_collection(
    name="sports_facts",
    embedding_function=embedding_function
)

if collection.count() == 0:
    print("ChromaDB is empty. Populating...")
    collection = populate_database()

def load_data():
    """Load sports facts from JSON file."""

    with open(f"{DATA_DIR}/sports_facts.json", "r", encoding="utf-8") as file:
        return json.load(file)


def populate_database():
    """Insert facts into ChromaDB."""

    data = load_data()

    # Remove old data
    try:
        client.delete_collection("sports_facts")
    except:
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

    global collection
    collection = new_collection

    print("Database created successfully!")

    return collection

def search_facts(query, sport=None, n_results=5):
    """
    Search the vector database for relevant facts.
    """

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