"""Generador para GitHub Copilot: (core + preset + profile) -> archivos.

Emite, según el scope:
- global  -> `.copilot/copilot-instructions.md` (header + estándares neutrales)
- project -> `.github/copilot-instructions.md`, `AGENTS.md`, `.github/prompts/*.prompt.md`

Reutiliza la fuente neutral `core/` (standards, agents-md) y los templates con forma
Copilot en `core/copilot/`. Los addons no aplican a Copilot en v2.
"""
from __future__ import annotations

from pathlib import Path

from framework.generators.common import read_text, rendered, standards_body
from framework.model import OutputFile
from framework.render import render


def _prompt_files(core_dir: Path, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "copilot" / "prompts").glob("*.prompt.md")):
        out.append(rendered(f, context, f".github/prompts/{f.name}"))
    return out


def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
             preset: dict, profile: dict, addons: list[dict],
             context: dict[str, str], scope: str) -> list[OutputFile]:
    if scope == "global":
        header = render(read_text(core_dir / "copilot" / "instructions-global-header.md"),
                        context, source="core/copilot/instructions-global-header.md")
        body = header + "\n" + standards_body(core_dir, context)
        return [OutputFile(".copilot/copilot-instructions.md", body)]

    if scope == "project":
        files: list[OutputFile] = [
            rendered(core_dir / "copilot" / "instructions-project.md", context,
                     ".github/copilot-instructions.md"),
            rendered(core_dir / "agents-md.md", context, "AGENTS.md"),
        ]
        files += _prompt_files(core_dir, context)
        return files

    raise ValueError(f"scope desconocido: {scope}")
