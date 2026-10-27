
import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "semantic_demo")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5


def main():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise ValueError("Set QDRANT_URL and QDRANT_API_KEY in .env")

    client = QdrantClient(url=url, api_key=api_key)

    if not client.collection_exists(COLLECTION_NAME):
        raise ValueError(
            f"Collection '{COLLECTION_NAME}' does not exist. "
            "Run setup_semantic_search.py first."
        )

    info = client.get_collection(COLLECTION_NAME)

    if info.points_count == 0:
        raise ValueError("The collection contains no products.")

    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print(f"\nSemantic Search | {COLLECTION_NAME}")
    print("Enter a natural-language query, or type 'exit' to quit.")

    while True:
        query = input("\nSearch: ").strip()

        if query.lower() == "exit":
            print("Search session ended.")
            break

        if not query:
            print("Please enter a search query.")
            continue

        query_vector = model.encode(
            query,
            normalize_embeddings=True,
        ).tolist()

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=TOP_K,
            with_payload=True,
            with_vectors=False,
        )

        results = response.points

        if not results:
            print("No matching products found.")
            continue

        print(f"\nTop {len(results)} results for: {query}")
        print("-" * 60)

        for rank, result in enumerate(results, start=1):
            product = result.payload or {}

            print(f"\n{rank}. {product.get('name', 'Unnamed product')}")
            print(f"   Category: {product.get('category', 'N/A')}")
            print(f"   Description: {product.get('description', 'N/A')}")
            print(f"   Similarity score: {result.score:.4f}")

        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
