"""Helpers compartidos por los generadores de agentes."""
from __future__ import annotations

from pathlib import Path

from framework.model import OutputFile
from framework.render import render


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rendered(path: Path, context: dict[str, str], relpath: str) -> OutputFile:
    """Lee un archivo, resuelve sus placeholders y lo empaqueta como OutputFile."""
    return OutputFile(relpath, render(read_text(path), context, source=str(path)))


def standards_body(core_dir: Path, context: dict[str, str]) -> str:
    """Concatena y renderiza los fragmentos neutrales de core/standards/."""
    fragments = sorted((core_dir / "standards").glob("*.md"))
    joined = "\n".join(read_text(f) for f in fragments)
    return render(joined, context, source="core/standards/*")


def skill_dirs(base: Path, skills: list[str], context: dict[str, str],
               dest_prefix: str) -> list[OutputFile]:
    """Copia (renderizando) los skills declarados bajo `base` a `<dest_prefix>/<skill>/…`.
    Formato SKILL.md común a Claude y Copilot (Agent Skills es estándar abierto)."""
    out = []
    for skill in skills:
        skill_dir = base / skill
        if not skill_dir.exists():
            continue
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(skill_dir).as_posix()
                out.append(rendered(f, context, f"{dest_prefix}/{skill}/{rel}"))
    return out
