import re
import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Load embedding model
# -----------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Read JavaScript file
# -----------------------------

with open("sample_code.js", "r") as file:
    code = file.read()


# -----------------------------
# 3. Code-aware chunking
# -----------------------------

pattern = r"async function\s+\w+\([^)]*\)\s*\{.*?\n\}"

matches = re.findall(pattern, code, re.DOTALL)


# -----------------------------
# 4. Extract function names
# -----------------------------

chunks = []
function_names = []

for chunk in matches:
    match = re.search(r"async function\s+(\w+)", chunk)

    if match:
        function_name = match.group(1)

        chunks.append(chunk)
        function_names.append(function_name)


# -----------------------------
# 5. Create embeddings
# -----------------------------

embeddings = model.encode(chunks)


# -----------------------------
# 6. Connect to Chroma
# -----------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="javascript_codebase"
)


# -----------------------------
# 7. Store chunks + metadata
# -----------------------------

ids = []

for i, function_name in enumerate(function_names):
    ids.append(function_name)

collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings.tolist(),
    metadatas=[
        {
            "file": "sample_code.js",
            "function": function_name,
            "language": "javascript",
            "type": "function"
        }
        for function_name in function_names
    ]
)


print("Indexed", len(chunks), "functions.")
print("Functions:", function_names)