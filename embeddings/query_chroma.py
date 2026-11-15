import chromadb
from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to persistent Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Get existing collection
collection = client.get_collection(
    name="codebase"
)

# User's question
question = "Where is the JWT token verified?"

# Convert question into embedding
query_embedding = model.encode([question])

# Search Chroma
top_k = 3

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=top_k,
    where={
    "$and": [
        {"section": "authentication"},
        {"language": "text"}
    ]
}
    
)

print("\nTop results:")

for i in range(len(results["ids"][0])):
    document_id = results["ids"][0][i]
    document = results["documents"][0][i]
    distance = results["distances"][0][i]
    metadata = results["metadatas"][0][i]

    print(f"\nRank: {i + 1}")
    print(f"ID: {document_id}")
    print(f"Distance: {distance:.4f}")
    print(f"Metadata: {metadata}")
    print("Document:")
    print(document)

# Use only the best result as context
context = results["documents"][0][0]

prompt = f"""
Answer the question using only the context provided below.

Context:
{context}

Question:
{question}
"""

response = ollama.chat(
    model="qwen3:8b-q4_K_M",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAnswer:")
print(response.message.content)