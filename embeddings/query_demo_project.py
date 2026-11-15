import chromadb
from sentence_transformers import SentenceTransformer

# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Connect to the existing Chroma database
client = chromadb.PersistentClient(path="./chroma_db")

# 3. Open the collection we just indexed
collection = client.get_collection(name="demo_project_codebase")

# 4. Ask a natural-language question
question = "Where is the access token generated?"

# 5. Convert the question into an embedding
query_embedding = model.encode(question).tolist()

# 6. Retrieve the two most relevant code chunks
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,
)

# 7. Display the retrieved code and its source
print("Question:", question)

for i, document in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]

    print("\n" + "=" * 50)
    print("Function:", metadata["function"])
    print("File:", metadata["file"])
    print("Distance:", round(distance, 4))
    print("Retrieved code:")
    print(document)