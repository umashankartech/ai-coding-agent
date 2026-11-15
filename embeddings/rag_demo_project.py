import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="demo_project_codebase")

# 3. Ask a question
question = input("Ask about your codebase:  ")

# 4. Convert the question into an embedding
query_embedding = model.encode(question).tolist()

# 5. Retrieve relevant code
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,
)

# 6. Build context with source information
context_parts = []

for i, document in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]

    context_parts.append(
        f"File: {metadata['file']}\n"
        f"Function: {metadata['function']}\n"
        f"Code:\n{document}"
    )

context = "\n\n---\n\n".join(context_parts)

# 7. Ask Qwen to answer using the retrieved code
response = ollama.chat(
    model="qwen3:8b-q4_K_M",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a codebase assistant. Answer using only "
                "the supplied code context. If the code does not "
                "contain enough evidence, say what is unknown. "
                "Clearly distinguish facts from inferences. "
                "Never invent implementation details."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Question: {question}\n\n"
                f"Retrieved code context:\n{context}"
            ),
        },
    ],
)

print("\nAnswer:\n")
print(response["message"]["content"])