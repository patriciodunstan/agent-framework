"""Generador para Claude Code: (core + preset + profile + addons) -> archivos."""
from __future__ import annotations

from pathlib import Path

from framework.model import OutputFile
from framework.render import render


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rendered(path: Path, context: dict[str, str], relpath: str) -> OutputFile:
    return OutputFile(relpath, render(_read(path), context, source=str(path)))


def _standards_body(core_dir: Path, context: dict[str, str]) -> str:
    fragments = sorted((core_dir / "standards").glob("*.md"))
    joined = "\n".join(_read(f) for f in fragments)
    return render(joined, context, source="core/standards/*")


def _copy_command_dir(core_dir: Path, sub: str, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "commands" / sub).glob("*.md")):
        out.append(_rendered(f, context, f".claude/commands/{f.name}"))
    return out


def _copy_skill_dirs(base: Path, skills: list[str], context: dict[str, str]) -> list[OutputFile]:
    out = []
    for skill in skills:
        skill_dir = base / skill
        if not skill_dir.exists():
            continue
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(skill_dir).as_posix()
                out.append(_rendered(f, context, f".claude/skills/{skill}/{rel}"))
    return out


def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
             preset: dict, profile: dict, addons: list[dict],
             context: dict[str, str], scope: str) -> list[OutputFile]:
    if scope == "global":
        header = render(_read(core_dir / "claude-md" / "global-header.md"), context,
                        source="core/claude-md/global-header.md")
        body = header + "\n" + _standards_body(core_dir, context)
        files = [OutputFile(".claude/CLAUDE.md", body)]
        files += _copy_command_dir(core_dir, "global", context)
        return files

    if scope == "project":
        files: list[OutputFile] = [
            _rendered(core_dir / "claude-md" / "project.md", context, "CLAUDE.md"),
            _rendered(core_dir / "agents-md.md", context, "AGENTS.md"),
            OutputFile(".claude/settings.json", _read(core_dir / "settings.json")),
            _rendered(core_dir / "adr" / "README.md", context, "docs/adr/README.md"),
            _rendered(core_dir / "adr" / "template.md", context, "docs/adr/template.md"),
        ]
        files += _copy_command_dir(core_dir, "project", context)
        for f in sorted((core_dir / "agents").glob("*.md")):
            files.append(_rendered(f, context, f".claude/agents/{f.name}"))
        for f in sorted((core_dir / "context-templates").glob("*.md")):
            files.append(_rendered(f, context, f".claude/context/{f.name}"))
        files += _copy_skill_dirs(presets_dir / preset["stack"] / "skills",
                                  preset["skills"], context)
        for addon in addons:
            files += _copy_skill_dirs(addons_dir / addon["addon"] / "skills",
                                      addon["skills"], context)
        return files

    raise ValueError(f"scope desconocido: {scope}")
