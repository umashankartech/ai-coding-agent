from sentence_transformers import SentenceTransformer
import json


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Read document
with open("sample_code.txt", "r") as file:
    text = file.read()


# Split into sections
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


# Create embeddings
embeddings = model.encode(chunks)


# Prepare data for storage
data = []

for chunk, embedding in zip(chunks, embeddings):

    data.append({
        "text": chunk,
        "embedding": embedding.tolist()
    })


# Save to JSON
with open("vector_store.json", "w") as file:
    json.dump(data, file)


print("Indexed", len(data), "chunks.")
print("Saved embeddings to vector_store.json")