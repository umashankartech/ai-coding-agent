import re


# Read JavaScript file
with open("sample_code.js", "r") as file:
    code = file.read()


# Find async function blocks
pattern = r"async function\s+\w+\([^)]*\)\s*\{.*?\n\}"

matches = re.findall(pattern, code, re.DOTALL)


print("Number of chunks:", len(matches))

for i, chunk in enumerate(matches):
    print("\n" + "=" * 60)
    print(f"CHUNK {i + 1}")
    print("=" * 60)
    print(chunk)