
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sentence_transformers import SentenceTransformer

load_dotenv()

URL = os.getenv("QDRANT_URL")
API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "semantic_demo"

if not URL or not API_KEY:
    raise ValueError("Check QDRANT_URL and QDRANT_API_KEY in .env")

# Load a pretrained text embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = QdrantClient(url=URL, api_key=API_KEY)

# Create a collection with the model's vector dimension
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )
    print("Created collection:", COLLECTION_NAME)
else:
    print("Collection already exists:", COLLECTION_NAME)

print("Setup complete!")
