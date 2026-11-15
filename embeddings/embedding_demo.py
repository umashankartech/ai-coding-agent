from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Our documents
documents = [
    "JWT tokens are verified in the authentication middleware.",
    "The login controller creates an access token after validating credentials.",
    "Products are filtered according to the selected category.",
    "PostgreSQL stores user information in the database.",
    "The application verifies the user's authentication token."
]

# 3. The user's question
query = "Where is the authentication token checked?"

# 4. Convert documents and query into vectors
document_embeddings = model.encode(documents)
query_embedding = model.encode([query])

# 5. Calculate similarity between the query and every document
similarity_scores = cosine_similarity(
    query_embedding,
    document_embeddings
)[0]

# 6. Combine documents with their scores
results = list(zip(documents, similarity_scores))

# 7. Sort from most similar to least similar
results.sort(key=lambda x: x[1], reverse=True)

# 8. Display the results
print("\nQuery:")
print(query)

print("\nSimilarity results:")
top_k = 2

for document, score in results[:top_k]:
    print(f"{score:.4f} -> {document}")