
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from discover_project_files import discover_project_files


class TestProjectFileScanner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.project_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_discovers_supported_files(self):
        (self.project_path / "app.js").touch()
        (self.project_path / "component.jsx").touch()
        (self.project_path / "main.py").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 3)

    def test_returns_relative_paths(self):
        (self.project_path / "controllers").mkdir()
        (self.project_path / "controllers" / "auth.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(
            files[0],
            Path("controllers/auth.js")
        )

    def test_excludes_unwanted_directories(self):
        excluded_dir = self.project_path / "node_modules"
        excluded_dir.mkdir()

        (excluded_dir / "library.js").touch()
        (self.project_path / "app.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "app.js")

    def test_excludes_secret_files(self):
        (self.project_path / ".env").touch()
        (self.project_path / ".env.development.local").touch()
        (self.project_path / "private.pem").touch()
        (self.project_path / "app.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "app.js")

    def test_ignores_unsupported_files(self):
        (self.project_path / "README.md").touch()
        (self.project_path / "image.png").touch()
        (self.project_path / "app.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 1)

    def test_discovers_all_supported_extensions(self):
        extensions = [".js", ".jsx", ".ts", ".tsx", ".py", ".json"]

        for extension in extensions:
            (self.project_path / f"file{extension}").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 6)

    def test_discovers_nested_files(self):
        nested_dir = self.project_path / "src" / "components"
        nested_dir.mkdir(parents=True)

        (nested_dir / "Button.jsx").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "Button.jsx")

    def test_invalid_directory_raises_error(self):
        invalid_path = self.project_path / "missing"

        with self.assertRaises(ValueError):
            discover_project_files(invalid_path)

    def test_does_not_exclude_parent_directories(self):
        project = self.project_path / "build" / "my-project"
        project.mkdir(parents=True)

        (project / "app.js").touch()

        files = discover_project_files(project)

        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], Path("app.js"))

    
    def test_respects_gitignore_file_patterns(self):
        (self.project_path / ".gitignore").write_text(
            "*.log\n*.tmp\n",
            encoding="utf-8"
        )

        (self.project_path / "app.js").touch()
        (self.project_path / "debug.log").touch()
        (self.project_path / "cache.tmp").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(
            files,
            [Path("app.js")]
        )

    def test_respects_gitignore_directory_patterns(self):
        (self.project_path / ".gitignore").write_text(
            "debug/\n",
            encoding="utf-8"
        )

        debug_dir = self.project_path / "debug"
        debug_dir.mkdir()

        (debug_dir / "error.js").touch()
        (self.project_path / "app.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(
            files,
            [Path("app.js")]
        )

    def test_respects_gitignore_negation_patterns(self):
        (self.project_path / ".gitignore").write_text(
            "*.js\n!important.js\n",
            encoding="utf-8"
        )

        (self.project_path / "debug.js").touch()
        (self.project_path / "important.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(
            files,
            [Path("important.js")]
        )

    def test_gitignore_cannot_override_secret_exclusions(self):
        (self.project_path / ".gitignore").write_text(
            "!.env\n",
            encoding="utf-8"
        )

        (self.project_path / ".env").touch()
        (self.project_path / "app.js").touch()

        files = discover_project_files(self.project_path)

        self.assertEqual(
            files,
            [Path("app.js")]
        )



if __name__ == "__main__":
    unittest.main()
