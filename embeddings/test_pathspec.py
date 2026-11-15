from pathspec import GitIgnoreSpec

patterns = [
    "node_modules/",
    "dist/",
    "*.log",
    "*.tmp",
    "debug/",
    "!important.log",
]

spec = GitIgnoreSpec.from_lines(patterns)

files = [
    "src/app.js",
    "src/debug.log",
    "important.log",
    "temp.tmp",
    "node_modules/package/index.js",
    "dist/bundle.js",
    "debug/error.js",
]

for file in files:
    ignored = spec.match_file(file)

    print(f"{file:40} -> {'IGNORED' if ignored else 'INCLUDED'}")