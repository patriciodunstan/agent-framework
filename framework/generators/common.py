"""Helpers compartidos por los generadores de agentes."""
from __future__ import annotations

import re
from pathlib import Path

from framework.model import OutputFile
from framework.render import render

# Comentarios de procedencia (`<!-- origen: ... -->`): valor para quien mantiene el
# framework, coste de tokens en el contexto de cada sesión. Se quedan en el repo,
# no en lo generado.
_PROCEDENCIA_RE = re.compile(r"^[ \t]*<!--.*?-->[ \t]*\r?\n?", re.MULTILINE)

# Skills que comparten varios stacks: una sola copia, resuelta por fallback.
SHARED_SKILLS = "_shared/skills"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_provenance(text: str) -> str:
    """Elimina los comentarios HTML de una línea y normaliza el cierre del archivo."""
    return _PROCEDENCIA_RE.sub("", text).rstrip() + "\n"


def rendered(path: Path, context: dict[str, str], relpath: str) -> OutputFile:
    """Lee un archivo, resuelve sus placeholders y lo empaqueta como OutputFile."""
    text = render(read_text(path), context, source=str(path))
    if relpath.endswith(".md"):
        text = strip_provenance(text)
    return OutputFile(relpath, text)


def standards_body(core_dir: Path, context: dict[str, str]) -> str:
    """Concatena y renderiza los fragmentos neutrales de core/standards/."""
    fragments = sorted((core_dir / "standards").glob("*.md"))
    joined = "\n".join(read_text(f) for f in fragments)
    return strip_provenance(render(joined, context, source="core/standards/*"))


def skill_dirs(base: Path, skills: list[str], context: dict[str, str],
               dest_prefix: str, *, fallback: Path | None = None) -> list[OutputFile]:
    """Copia (renderizando) los skills declarados bajo `base` a `<dest_prefix>/<skill>/…`.
    Formato SKILL.md común a Claude y Copilot (Agent Skills es estándar abierto).
    Los skills que no viven en `base` se buscan en `fallback` (skills compartidos por
    varios stacks, para no mantener copias divergentes)."""
    out = []
    for skill in skills:
        skill_dir = base / skill
        if not skill_dir.exists() and fallback is not None:
            skill_dir = fallback / skill
        if not skill_dir.exists():
            continue
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(skill_dir).as_posix()
                out.append(rendered(f, context, f"{dest_prefix}/{skill}/{rel}"))
    return out
