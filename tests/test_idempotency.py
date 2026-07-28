from pathlib import Path

import pytest

from framework.cli import main
from framework.render import find_unresolved

ROOT = Path(__file__).parent.parent
STACKS = ["python-fastapi", "react-vite", "java-springboot", "dotnet", "aws-lambda"]
PROFILES = ["personal", "work"]


@pytest.mark.parametrize("stack", STACKS)
@pytest.mark.parametrize("profile", PROFILES)
def test_matrix_installs_without_leftover_placeholders(tmp_path, stack, profile):
    code = main(["--scope", "project", "--stack", stack, "--profile", profile,
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    for f in tmp_path.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".json"}:
            assert find_unresolved(f.read_text(encoding="utf-8")) == [], f


def test_second_run_creates_nothing(tmp_path, capsys):
    args = ["--scope", "project", "--stack", "python-fastapi", "--profile", "work",
            "--target", str(tmp_path), "--root", str(ROOT)]
    main(args)
    capsys.readouterr()
    main(args)
    out = capsys.readouterr().out
    assert "Creados (0)" in out


def test_global_scope_matrix(tmp_path):
    for profile in PROFILES:
        code = main(["--scope", "global", "--profile", profile,
                     "--home", str(tmp_path / profile), "--root", str(ROOT)])
        assert code == 0
        assert (tmp_path / profile / ".claude" / "CLAUDE.md").exists()


def test_global_standards_are_profile_neutral(tmp_path):
    """El CLAUDE.md global (por máquina) no debe hornear convenciones de un
    profile ni dejar secciones vacías: los estándares son principios portables."""
    bodies = {}
    for profile in PROFILES:
        code = main(["--scope", "global", "--profile", profile,
                     "--home", str(tmp_path / profile), "--root", str(ROOT)])
        assert code == 0
        bodies[profile] = (tmp_path / profile / ".claude" / "CLAUDE.md").read_text(
            encoding="utf-8"
        )
        # sin placeholders sin resolver
        assert find_unresolved(bodies[profile]) == []
        # sin sección pre-commit vacía (encabezado seguido de vacío)
        assert "SIEMPRE:\n\n" not in bodies[profile]

    # el ticket_format de 'work' (AB#) NO debe quedar horneado en el global
    assert "AB#" not in bodies["work"]
    assert "AB#" not in bodies["personal"]
