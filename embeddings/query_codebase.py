import chromadb
from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to Chroma
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="javascript_codebase"
)


# User's question
question = "Where is the access token generated?"


# Convert question into embedding
query_embedding = model.encode([question])


# Search Chroma
results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=2
)


# Display results
print("\nTop results:")

for i in range(len(results["ids"][0])):

    print("\n" + "=" * 60)

    print(f"Rank: {i + 1}")

    print("ID:", results["ids"][0][i])

    print("Distance:", results["distances"][0][i])

    print("Metadata:", results["metadatas"][0][i])

    print("Code:")
    print(results["documents"][0][i])