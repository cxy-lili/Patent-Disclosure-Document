from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.install import CLIENTS, destination_for, install_skill


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        (self.source / "references").mkdir(parents=True)
        (self.source / "SKILL.md").write_text("---\nname: patent-disclosure\n---\n", encoding="utf-8")
        (self.source / "references" / "example.md").write_text("公式与实施例", encoding="utf-8")
        self.target = self.root / "目标项目" / "patent-disclosure"

    def test_each_client_has_distinct_user_and_project_locations(self):
        for client in CLIENTS:
            with self.subTest(client=client):
                user = destination_for(client, "user", home=self.root / "home")
                project = destination_for(client, "project", project=self.root / "project")
                self.assertTrue(user.is_relative_to(self.root / "home"))
                self.assertTrue(project.is_relative_to(self.root / "project"))
                self.assertEqual(user.name, "patent-disclosure")
                self.assertEqual(project.name, "patent-disclosure")
        self.assertEqual(destination_for("copilot", "project", self.root).parts[-3:], (".github", "skills", "patent-disclosure"))

    def test_install_copies_nested_resources_and_preserves_source(self):
        install_skill(self.target, source=self.source)
        self.assertEqual((self.target / "references" / "example.md").read_bytes(), (self.source / "references" / "example.md").read_bytes())

    def test_existing_install_is_untouched_without_replace(self):
        install_skill(self.target, source=self.source)
        marker = self.target / "local-note.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            install_skill(self.target, source=self.source)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_replace_retains_old_install_in_backup(self):
        install_skill(self.target, source=self.source)
        (self.target / "old-note.txt").write_text("keep", encoding="utf-8")
        result = install_skill(self.target, source=self.source, replace=True)
        self.assertEqual((Path(result["backup"]) / "old-note.txt").read_text(encoding="utf-8"), "keep")
        self.assertFalse(Path(result["backup"]).is_relative_to(self.target.parent))
        self.assertFalse((self.target / "old-note.txt").exists())

    def test_dry_run_has_no_filesystem_side_effects(self):
        result = install_skill(self.target, source=self.source, dry_run=True)
        self.assertEqual(result["status"], "dry-run")
        self.assertFalse(self.target.parent.exists())

    def test_source_destination_overlap_is_rejected(self):
        for destination in [self.source, self.source / "nested", self.root]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                install_skill(destination, source=self.source, replace=True)

    def test_unrelated_existing_directory_is_not_replaced(self):
        self.target.mkdir(parents=True)
        (self.target / "notes.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError):
            install_skill(self.target, source=self.source, replace=True)
        self.assertTrue((self.target / "notes.txt").exists())

    def test_failed_replacement_restores_original_install(self):
        install_skill(self.target, source=self.source)
        (self.target / "old-note.txt").write_text("keep", encoding="utf-8")
        native_rename = Path.rename

        def fail_staged_rename(path, target):
            if path.parent.name.startswith(".patent-disclosure-install-"):
                raise PermissionError("simulated blocked destination")
            return native_rename(path, target)

        with patch.object(Path, "rename", fail_staged_rename), self.assertRaises(PermissionError):
            install_skill(self.target, source=self.source, replace=True)
        self.assertEqual((self.target / "old-note.txt").read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
