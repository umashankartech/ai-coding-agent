import chromadb
from sentence_transformers import SentenceTransformer
import ollama


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Connect to Chroma
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="javascript_codebase"
)


# -----------------------------
# 3. User question
# -----------------------------

question = "Where is the access token generated?"


# -----------------------------
# 4. Create query embedding
# -----------------------------

query_embedding = model.encode([question])


# -----------------------------
# 5. Retrieve relevant code
# -----------------------------

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=1,
    where={
        "$and": [
            {"language": "javascript"},
            {"type": "function"}
        ]
    }
)


retrieved_code = "\n\n".join(results["documents"][0])
metadata = results["metadatas"][0]


print("\nRetrieved code:")
print(retrieved_code)

print("\nMetadata:")
print(metadata)


# -----------------------------
# 6. Build LLM prompt
# -----------------------------

prompt = f"""
You are a coding assistant.

Answer the user's question using only the provided code.

Code:
{retrieved_code}

Question:
{question}

Explain where the relevant logic is and what it does.
"""


# -----------------------------
# 7. Ask local LLM
# -----------------------------

response = ollama.chat(
    model="qwen3:8b-q4_K_M",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# -----------------------------
# 8. Display answer
# -----------------------------

print("\nAnswer:")
print(response.message.content)