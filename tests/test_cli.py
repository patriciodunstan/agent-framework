from pathlib import Path

from framework.cli import main

ROOT = Path(__file__).parent / "fixtures"


def test_cli_project_scope_writes_files(tmp_path, capsys):
    code = main(["--scope", "project", "--stack", "demo", "--profile", "demo",
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "commands" / "new-ticket.md").exists()
    assert ".claude/" in (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert "Creados" in capsys.readouterr().out


def test_cli_global_scope_uses_home(tmp_path):
    code = main(["--scope", "global", "--profile", "demo",
                 "--home", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()


def test_cli_unknown_stack_returns_2(capsys):
    code = main(["--scope", "project", "--stack", "noexiste", "--profile", "demo",
                 "--target", ".", "--root", str(ROOT)])
    assert code == 2
    assert "no existe" in capsys.readouterr().err


def test_cli_unknown_addon_returns_2(tmp_path, capsys):
    code = main(["--scope", "project", "--stack", "demo", "--profile", "demo",
                 "--addons", "noexiste", "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 2
    assert "addon" in capsys.readouterr().err.lower()
