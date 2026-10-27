from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

sentences = [
    "A comfortable office chair",
    "A chair for working at a desk",
    "A mobile phone for photography",
]

embeddings = model.encode(
    sentences,
    normalize_embeddings=True,
)

print("Number of sentences:", len(embeddings))
print("Dimensions per vector:", embeddings.shape[1])
print("First vector:", embeddings[0][:5])