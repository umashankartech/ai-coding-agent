# -----------------------------
# 1. Read the JavaScript file
# -----------------------------

with open("sample_code.js", "r") as file:
    code = file.read()


# -----------------------------
# 2. Fixed-size chunking
# -----------------------------

chunk_size = 300

chunks = []

for i in range(0, len(code), chunk_size):
    chunk = code[i:i + chunk_size]
    chunks.append(chunk)


# -----------------------------
# 3. Display chunks
# -----------------------------

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n" + "=" * 60)
    print(f"CHUNK {i + 1}")
    print("=" * 60)
    print(chunk)