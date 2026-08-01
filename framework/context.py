"""Construye el diccionario de variables de contexto para el render de plantillas."""
from __future__ import annotations

_COMMAND_KEYS = {
    "test": "test_cmd",
    "lint": "lint_cmd",
    "typecheck": "typecheck_cmd",
    "build": "build_cmd",
}

_MATURITY_WARNING = (
    "> ⚠️ **Preset sin probar en proyecto real todavía.** Es una plantilla base: "
    "revisá y endurecé las convenciones antes de confiar en ella.\n"
)


def _precommit_steps(preset: dict) -> str:
    cmds = preset["commands"]
    lines = []
    for i, key in enumerate(preset["precommit"], start=1):
        lines.append(f"{i}. `{cmds.get(key, '')}`")
    return "\n".join(lines)


def build_context(preset: dict, profile: dict) -> dict[str, str]:
    ctx: dict[str, str] = {
        "stack": preset["stack"],
        "language": preset["language"],
        "code_globs": preset.get("code_globs", "**"),
        "structure": preset["structure"],
        "precommit_steps": _precommit_steps(preset),
        "profile": profile["profile"],
        "git_host": profile["git_host"],
        "ci": profile["ci"],
        "cloud": profile.get("cloud", ""),
        "ticket_format": profile["ticket_format"],
        "branch_pattern": profile["branch_pattern"],
        "maturity_warning": _MATURITY_WARNING if preset["maturity"] == "plantilla-base" else "",
    }
    for src, dst in _COMMAND_KEYS.items():
        ctx[dst] = preset["commands"].get(src) or ""
    return {k: str(v) for k, v in ctx.items()}
