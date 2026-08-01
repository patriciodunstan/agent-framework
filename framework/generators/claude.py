"""Generador para Claude Code: (core + preset + profile + addons) -> archivos."""
from __future__ import annotations

from pathlib import Path

from framework.generators.common import read_text, rendered, standards_body
from framework.model import OutputFile
from framework.render import render


def _copy_command_dir(core_dir: Path, sub: str, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "commands" / sub).glob("*.md")):
        out.append(rendered(f, context, f".claude/commands/{f.name}"))
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
                out.append(rendered(f, context, f".claude/skills/{skill}/{rel}"))
    return out


def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
             preset: dict, profile: dict, addons: list[dict],
             context: dict[str, str], scope: str) -> list[OutputFile]:
    if scope == "global":
        header = render(read_text(core_dir / "claude-md" / "global-header.md"), context,
                        source="core/claude-md/global-header.md")
        body = header + "\n" + standards_body(core_dir, context)
        files = [OutputFile(".claude/CLAUDE.md", body)]
        files += _copy_command_dir(core_dir, "global", context)
        return files

    if scope == "project":
        files: list[OutputFile] = [
            rendered(core_dir / "claude-md" / "project.md", context, "CLAUDE.md"),
            rendered(core_dir / "agents-md.md", context, "AGENTS.md"),
            OutputFile(".claude/settings.json", read_text(core_dir / "settings.json")),
            rendered(core_dir / "adr" / "README.md", context, "docs/adr/README.md"),
            rendered(core_dir / "adr" / "template.md", context, "docs/adr/template.md"),
        ]
        files += _copy_command_dir(core_dir, "project", context)
        for f in sorted((core_dir / "agents").glob("*.md")):
            files.append(rendered(f, context, f".claude/agents/{f.name}"))
        for f in sorted((core_dir / "context-templates").glob("*.md")):
            files.append(rendered(f, context, f".claude/context/{f.name}"))
        files += _copy_skill_dirs(presets_dir / preset["stack"] / "skills",
                                  preset["skills"], context)
        for addon in addons:
            files += _copy_skill_dirs(addons_dir / addon["addon"] / "skills",
                                      addon["skills"], context)
        return files

    raise ValueError(f"scope desconocido: {scope}")
