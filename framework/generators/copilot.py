"""Generador para GitHub Copilot: (core + preset + profile) -> archivos.

Emite, según el scope:
- global  -> `.copilot/copilot-instructions.md` (header + estándares neutrales)
- project -> `.github/copilot-instructions.md`, `AGENTS.md`, `.github/prompts/*.prompt.md`,
             `.github/instructions/*`, `.github/agents/*`, `.github/skills/<skill>/*`,
             `docs/context/*` (memoria del proyecto) y `docs/adr/*` (paridad con Claude).

Reutiliza la fuente neutral `core/` (standards, agents-md, context-templates, adr, skills de
preset/addon) y los templates con forma Copilot en `core/copilot/`. Agent Skills es un
estándar abierto: los skills se reutilizan verbatim (mismo `SKILL.md`).
"""
from __future__ import annotations

from pathlib import Path

from framework.generators.common import read_text, rendered, skill_dirs, standards_body
from framework.model import OutputFile
from framework.render import render


def _prompt_files(core_dir: Path, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "copilot" / "prompts").glob("*.prompt.md")):
        out.append(rendered(f, context, f".github/prompts/{f.name}"))
    return out


def _context_files(core_dir: Path, context: dict[str, str]) -> list[OutputFile]:
    """Memoria del proyecto en docs/context/: MEMORY.md con forma Copilot + el resto
    de los templates neutrales de core/context-templates/."""
    out = [rendered(core_dir / "copilot" / "context" / "MEMORY.md", context,
                    "docs/context/MEMORY.md")]
    for f in sorted((core_dir / "context-templates").glob("*.md")):
        if f.name == "MEMORY.md":
            continue
        out.append(rendered(f, context, f"docs/context/{f.name}"))
    return out


def _instruction_files(core_dir: Path, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "copilot" / "instructions").glob("*.instructions.md")):
        out.append(rendered(f, context, f".github/instructions/{f.name}"))
    return out


def _agent_files(core_dir: Path, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "copilot" / "agents").glob("*.agent.md")):
        out.append(rendered(f, context, f".github/agents/{f.name}"))
    return out


def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
             preset: dict, profile: dict, addons: list[dict],
             context: dict[str, str], scope: str) -> list[OutputFile]:
    if scope == "global":
        header = render(read_text(core_dir / "copilot" / "instructions-global-header.md"),
                        context, source="core/copilot/instructions-global-header.md")
        std_body = standards_body(core_dir, context)
        files = [OutputFile(".copilot/copilot-instructions.md", header + "\n" + std_body)]
        # Para VS Code Copilot Chat: estándares globales como instructions folder + prompts
        # globales (stack-agnósticos). Se activan apuntando settings a ~/.copilot/ (ver README).
        std_instr = ("---\ndescription: Estándares de ingeniería (global)\n"
                     "applyTo: '**'\n---\n\n" + std_body)
        files.append(OutputFile(".copilot/instructions/standards.instructions.md", std_instr))
        for f in sorted((core_dir / "copilot" / "global-prompts").glob("*.prompt.md")):
            files.append(rendered(f, context, f".copilot/prompts/{f.name}"))
        files.append(rendered(core_dir / "copilot" / "global-readme.md", context,
                              ".copilot/README-vscode.md"))
        return files

    if scope == "project":
        files: list[OutputFile] = [
            rendered(core_dir / "copilot" / "instructions-project.md", context,
                     ".github/copilot-instructions.md"),
            rendered(core_dir / "agents-md.md", context, "AGENTS.md"),
        ]
        files += _prompt_files(core_dir, context)
        files += _instruction_files(core_dir, context)
        files += _agent_files(core_dir, context)
        files += _context_files(core_dir, context)
        # ADR (docs neutrales, paridad con Claude)
        files.append(rendered(core_dir / "adr" / "README.md", context, "docs/adr/README.md"))
        files.append(rendered(core_dir / "adr" / "template.md", context, "docs/adr/template.md"))
        # Skills de stack y addons (Agent Skills, mismo SKILL.md que Claude)
        files += skill_dirs(presets_dir / preset["stack"] / "skills",
                            preset["skills"], context, ".github/skills")
        for addon in addons:
            files += skill_dirs(addons_dir / addon["addon"] / "skills",
                                addon["skills"], context, ".github/skills")
        return files

    raise ValueError(f"scope desconocido: {scope}")
