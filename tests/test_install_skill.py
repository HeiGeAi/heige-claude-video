import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SCRIPT = REPO_ROOT / "scripts" / "install_skill.py"
STYLES_SCRIPT = REPO_ROOT / "skills" / "code-animation-prompts" / "scripts" / "styles.py"
CATALOG_ROOT = REPO_ROOT / "skills" / "code-animation-prompts"


class InstallSkillTests(unittest.TestCase):
    def run_install(self, home: Path, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, "-B", str(INSTALL_SCRIPT), *args],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_install_both_targets_and_skip_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first = self.run_install(home, "--target", "both", "--only", "heige-claude-video")
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((home / ".claude" / "skills" / "heige-claude-video" / "SKILL.md").is_file())
            self.assertTrue((home / ".agents" / "skills" / "heige-claude-video" / "SKILL.md").is_file())

            second = self.run_install(home, "--target", "claude", "--only", "heige-claude-video")
            self.assertEqual(second.returncode, 1)
            self.assertIn("已存在", second.stdout)

    def test_dangling_symlink_does_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            skills_dir = home / ".agents" / "skills"
            skills_dir.mkdir(parents=True)
            (skills_dir / "heige-claude-video").symlink_to(home / "missing-target")

            res = self.run_install(home, "--target", "codex", "--only", "heige-claude-video")
            self.assertEqual(res.returncode, 1)
            self.assertIn("已存在", res.stdout)
            self.assertNotIn("Traceback", res.stderr)
            self.assertTrue((skills_dir / "heige-claude-video").is_symlink())

    def test_partial_unknown_only_is_rejected_without_partial_install(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            res = self.run_install(
                home,
                "--target",
                "claude",
                "--only",
                "heige-claude-video",
                "--only",
                "nonexistent-skill",
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("nonexistent-skill", res.stderr)
            self.assertFalse((home / ".claude" / "skills" / "heige-claude-video").exists())

    def test_install_one_ignores_pycache_and_ds_store(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("install_skill", INSTALL_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "src" / "demo-skill"
            (src / "__pycache__").mkdir(parents=True)
            (src / "SKILL.md").write_text("# demo\n", encoding="utf-8")
            (src / ".DS_Store").write_bytes(b"junk")
            (src / "__pycache__" / "demo.cpython-314.pyc").write_bytes(b"pyc")
            target_base = Path(tmp) / "dest"
            rc = mod.install_one(src, target_base)
            self.assertEqual(rc, 0)
            installed = target_base / "demo-skill"
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertFalse((installed / "__pycache__").exists())
            self.assertFalse((installed / ".DS_Store").exists())

    def test_catalog_and_styles_cli_integrity(self) -> None:
        data = json.loads((CATALOG_ROOT / "references" / "catalog.json").read_text(encoding="utf-8"))
        entries = data["entries"]
        self.assertEqual(len(entries), 341)
        for entry in entries:
            self.assertTrue((CATALOG_ROOT / entry["file"]).is_file(), f"missing file: {entry['file']}")
            if entry.get("image"):
                self.assertTrue((CATALOG_ROOT / entry["image"]).is_file(), f"missing image: {entry['image']}")

        res = subprocess.run(
            [sys.executable, "-B", str(STYLES_SCRIPT), "show", "B3"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("# B3", res.stdout)


if __name__ == "__main__":
    unittest.main()
