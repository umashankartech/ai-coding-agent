import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Create Chroma client
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# -----------------------------
# 3. Create collection
# -----------------------------

collection = client.get_or_create_collection(
    name="codebase"
)


# -----------------------------
# 4. Read our code/document
# -----------------------------

with open("sample_code.txt", "r") as file:
    text = file.read()


# -----------------------------
# 5. Split into chunks
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
# 6. Create embeddings
# -----------------------------

embeddings = model.encode(chunks)


# -----------------------------
# 7. Store in Chroma
# -----------------------------

collection.add(
    ids=["auth", "cart", "products"],
    documents=chunks,
    embeddings=embeddings.tolist()
)


print("Indexed", len(chunks), "chunks into Chroma.")