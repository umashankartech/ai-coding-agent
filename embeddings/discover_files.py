from pathlib import Path

project_path = Path("demo_project")

files = list(project_path.rglob("*.js"))

print("JavaScript files found:", len(files))

for file in files:
    print("\n" + "=" * 60)
    print("FILE:", file)
    print("=" * 60)

    with open(file, "r") as f:
        code = f.read()

    print(code)