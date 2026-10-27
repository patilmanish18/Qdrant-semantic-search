
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "semantic_demo")
DATA_FILE = Path("data/products.csv")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 32
VECTOR_SIZE = 384


def load_products():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    with DATA_FILE.open("r", encoding="utf-8", newline="") as file:
        products = list(csv.DictReader(file))

    required = {"id", "name", "category", "description"}

    if not products:
        raise ValueError("The product dataset is empty.")

    if not required.issubset(products[0].keys()):
        raise ValueError(f"CSV must contain columns: {sorted(required)}")

    seen_ids = set()

    for product in products:
        for field in required:
            if not product[field].strip():
                raise ValueError(
                    f"Product contains an empty {field}: {product}"
                )

        product["id"] = int(product["id"])

        if product["id"] <= 0 or product["id"] in seen_ids:
            raise ValueError(f"Invalid or duplicate product ID: {product['id']}")

        seen_ids.add(product["id"])

    return products


def main():
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise ValueError("Set QDRANT_URL and QDRANT_API_KEY in .env")

    client = QdrantClient(url=url, api_key=api_key)
    products = load_products()

    if client.collection_exists(COLLECTION_NAME):
        info = client.get_collection(COLLECTION_NAME)
        vector_config = info.config.params.vectors

        if not isinstance(vector_config, models.VectorParams):
            raise ValueError("Expected a single-vector collection.")

        if vector_config.size != VECTOR_SIZE:
            raise ValueError(
                f"Collection uses {vector_config.size} dimensions; "
                f"expected {VECTOR_SIZE}."
            )

        if vector_config.distance != models.Distance.COSINE:
            raise ValueError("Collection must use cosine distance.")
    else:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE,
            ),
        )
        print(f"Created collection: {COLLECTION_NAME}")

    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    for start in range(0, len(products), BATCH_SIZE):
        batch = products[start:start + BATCH_SIZE]
        texts = [
            f"{p['name']}. Category: {p['category']}. {p['description']}"
            for p in batch
        ]

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        points = [
            models.PointStruct(
                id=product["id"],
                vector=embedding.tolist(),
                payload={
                    "name": product["name"],
                    "category": product["category"],
                    "description": product["description"],
                },
            )
            for product, embedding in zip(batch, embeddings)
        ]

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
            wait=True,
        )

        print(
            f"Uploaded {min(start + len(batch), len(products))}"
            f"/{len(products)} products"
        )

    info = client.get_collection(COLLECTION_NAME)
    print("\nIngestion completed.")
    print("Collection:", COLLECTION_NAME)
    print("Dataset records:", len(products))
    print("Total collection points:", info.points_count)


if __name__ == "__main__":
    main()
