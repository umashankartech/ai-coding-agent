from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import ollama


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Load our code/document
# -----------------------------

with open("sample_code.txt", "r") as file:
    text = file.read()


# -----------------------------
# 3. Split into chunks
# -----------------------------

sections = ["AUTHENTICATION", "CART", "PRODUCTS"]

chunks = []

for section in sections:

    start = text.find(section)

    if section == "AUTHENTICATION":
        end = text.find("CART")

    elif section == "CART":
        end = text.find("PRODUCTS")

    else:
        end = len(text)

    chunk = text[start:end].strip()

    chunks.append(chunk)


# -----------------------------
# 4. Create embeddings
# -----------------------------

chunk_embeddings = model.encode(chunks)


# -----------------------------
# 5. User question
# -----------------------------

question = "Where is the JWT token verified?"


# -----------------------------
# 6. Embed the question
# -----------------------------

query_embedding = model.encode([question])


# -----------------------------
# 7. Calculate similarity
# -----------------------------

similarity_scores = cosine_similarity(
    query_embedding,
    chunk_embeddings
)[0]


# -----------------------------
# 8. Rank the chunks
# -----------------------------

results = list(zip(chunks, similarity_scores))

results.sort(
    key=lambda x: x[1],
    reverse=True
)


# -----------------------------
# 9. Get Top-K
# -----------------------------

top_k = 1

top_results = results[:top_k]


# -----------------------------
# 10. Build context
# -----------------------------

context = "\n\n".join(
    chunk for chunk, score in top_results
)


print("\nRetrieved context:")
print(context)


# -----------------------------
# 11. Send context to Qwen
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
# 12. Print final answer
# -----------------------------

print("\nAnswer:")
print(response.message.content)