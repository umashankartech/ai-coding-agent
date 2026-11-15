from pathlib import Path
import re


# 1. Locate the demo project
project_path = Path("demo_project")

# 2. Discover JavaScript files
files = list(project_path.rglob("*.js"))

all_chunks = []


# 3. Read each file and extract async functions
pattern = r"async function\s+(\w+)\([^)]*\)\s*\{.*?\n\}"


for file in files:
    with open(file, "r") as f:
        code = f.read()

    matches = re.finditer(pattern, code, re.DOTALL)

    for match in matches:
        function_name = match.group(1)
        function_code = match.group(0)

        all_chunks.append({
            "text": function_code,
            "metadata": {
                "file": str(file),
                "function": function_name,
                "language": "javascript",
                "type": "function"
            }
        })


# 4. Display extracted chunks
print("Total functions extracted:", len(all_chunks))

for i, chunk in enumerate(all_chunks, start=1):
    print("\n" + "=" * 60)
    print(f"CHUNK {i}")
    print("=" * 60)

    print("Function:", chunk["metadata"]["function"])
    print("File:", chunk["metadata"]["file"])
    print("Metadata:", chunk["metadata"])
    print("Code:")
    print(chunk["text"])