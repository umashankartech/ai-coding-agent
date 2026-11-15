import chromadb


# Connect to existing Chroma database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Get existing collection
collection = client.get_collection(
    name="codebase"
)


# Add metadata to existing chunks
collection.update(
    ids=["auth", "cart", "products"],
    metadatas=[
        {
            "section": "authentication",
            "file": "sample_code.txt",
            "language": "text"
        },
        {
            "section": "cart",
            "file": "sample_code.txt",
            "language": "text"
        },
        {
            "section": "products",
            "file": "sample_code.txt",
            "language": "text"
        }
    ]
)


print("Metadata updated successfully.")