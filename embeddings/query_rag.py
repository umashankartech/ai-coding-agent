from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import ollama


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Load stored vector data
# -----------------------------

with open("vector_store.json", "r") as file:
    data = json.load(file)


# -----------------------------
# 3. Extract stored embeddings
# -----------------------------

stored_embeddings = [
    item["embedding"]
    for item in data
]


# -----------------------------
# 4. User question
# -----------------------------

question = "Where is the JWT token verified?"


# -----------------------------
# 5. Create question embedding
# -----------------------------

query_embedding = model.encode([question])


# -----------------------------
# 6. Search stored embeddings
# -----------------------------

similarity_scores = cosine_similarity(
    query_embedding,
    stored_embeddings
)[0]


# -----------------------------
# 7. Rank results
# -----------------------------

results = list(zip(data, similarity_scores))

results.sort(
    key=lambda x: x[1],
    reverse=True
)


# -----------------------------
# 8. Select Top-K
# -----------------------------

top_k = 1

top_results = results[:top_k]


# -----------------------------
# 9. Build context
# -----------------------------

context = "\n\n".join(
    item["text"]
    for item, score in top_results
)


print("\nRetrieved context:")
print(context)


# -----------------------------
# 10. Send context to Qwen
# -----------------------------

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


# -----------------------------
# 11. Final answer
# -----------------------------

print("\nAnswer:")
print(response.message.content)