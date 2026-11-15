
from pathlib import Path
from pathspec import GitIgnoreSpec


# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".json",
}

# Directories we don't want to scan
EXCLUDED_DIRECTORIES = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".venv",
    "__pycache__",
}

# Files we never want to index
EXCLUDED_FILES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    ".env.test",
    ".env.staging",
    "id_rsa",
    "id_ed25519",
}


def is_secret_file(filename):
    if filename.startswith(".env"):
        return True

    if filename.endswith((".pem", ".key", ".p12", ".pfx")):
        return True

    return filename in EXCLUDED_FILES


def load_gitignore(project_path):
    gitignore_path = project_path / ".gitignore"

    if not gitignore_path.is_file():
        return None

    patterns = gitignore_path.read_text(encoding="utf-8").splitlines()

    return GitIgnoreSpec.from_lines(patterns)


def discover_project_files(project_path):
    project_path = Path(project_path).resolve()

    if not project_path.is_dir():
        raise ValueError(f"Invalid project directory: {project_path}")

    gitignore_spec = load_gitignore(project_path)

    project_files = []

    for file in project_path.rglob("*"):

        if not file.is_file():
            continue

        # Use paths relative to the project root
        relative_path = file.relative_to(project_path)

        # Exclude unwanted directories inside the project
        if any(part in EXCLUDED_DIRECTORIES for part in relative_path.parts):
            continue

        # Always exclude sensitive files
        if is_secret_file(file.name):
            continue

        # Apply root .gitignore rules
        if gitignore_spec and gitignore_spec.match_file(relative_path.as_posix()):
            continue

        # Only include supported file types
        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        project_files.append(relative_path)

    return sorted(project_files)


# Run directly when this file is executed
if __name__ == "__main__":

    project_files = discover_project_files("demo_project")

    print("Total project files discovered:", len(project_files))

    for file in project_files:
        print(file)
