from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer


# 1. Locate the demo project
project_path = Path("demo_project")

# 2. Discover JavaScript files
files = sorted(project_path.rglob("*.js"))

# 3. Prepare the function extraction pattern
pattern = r"async function\s+(\w+)\([^)]*\)\s*\{.*?\n\}"

all_chunks = []

# 4. Extract functions and metadata
for file in files:
    with open(file, "r") as f:
        code = f.read()

    matches = re.finditer(pattern, code, re.DOTALL)

    for match in matches:
        function_name = match.group(1)

        all_chunks.append({
            "id": f"{file}:{function_name}",
            "text": match.group(0),
            "metadata": {
                "file": str(file),
                "function": function_name,
                "language": "javascript",
                "type": "function",
            },
        })


# 5. Generate embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [chunk["text"] for chunk in all_chunks]

embeddings = model.encode(documents).tolist()


# 6. Create a separate persistent Chroma collection
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="demo_project_codebase"
)


# 7. Store code, embeddings, and metadata
collection.upsert(
    ids=[chunk["id"] for chunk in all_chunks],
    documents=documents,
    embeddings=embeddings,
    metadatas=[chunk["metadata"] for chunk in all_chunks],
)


# 8. Print indexing results
print("Files discovered:", len(files))
print("Functions indexed:", len(all_chunks))
print("Chroma collection:", collection.name)

for chunk in all_chunks:
    print(
        f"- {chunk['metadata']['function']} "
        f"-> {chunk['metadata']['file']}"
    )