from pathlib import Path

from framework.cli import main

ROOT = Path(__file__).parent.parent  # raíz real del framework


def _install(tmp_path, stack, profile, addons=""):
    args = ["--scope", "project", "--stack", stack, "--profile", profile,
            "--target", str(tmp_path), "--root", str(ROOT)]
    if addons:
        args += ["--addons", addons]
    return main(args)


def test_python_fastapi_work_installs_clean(tmp_path):
    assert _install(tmp_path, "python-fastapi", "work") == 0
    claude_md = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "AB#" in claude_md  # profile work
    assert "python-fastapi" in claude_md
    assert (tmp_path / ".claude" / "skills" / "fastapi-templates").exists()
    # ningún archivo generado conserva placeholders
    for md in (tmp_path).rglob("*.md"):
        assert "${" not in md.read_text(encoding="utf-8")


def test_react_vite_personal_installs_clean(tmp_path):
    assert _install(tmp_path, "react-vite", "personal") == 0
    assert "#<número>" in (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
