"""CLI del framework: parsea flags, orquesta la generación y reporta."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from framework.context import build_context
from framework.generators.claude import generate
from framework.loader import load_addon, load_preset, load_profile
from framework.model import ConfigError, InstallReport
from framework.writer import ensure_line, write_tree


def _parse(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="install.py", description="Configurador de agentes")
    p.add_argument("--scope", required=True, choices=["global", "project"])
    p.add_argument("--stack")
    p.add_argument("--profile", required=True)
    p.add_argument("--addons", default="")
    p.add_argument("--target")
    p.add_argument("--home")
    p.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse(argv)
    root = Path(args.root)
    try:
        profile = load_profile(root / "profiles", args.profile)
        addon_names = [a for a in args.addons.split(",") if a]
        addons = [load_addon(root / "addons", a) for a in addon_names]

        if args.scope == "project":
            if not args.stack or not args.target:
                raise ConfigError("scope project requiere --stack y --target")
            preset = load_preset(root / "presets", args.stack)
            target = Path(args.target)
        else:
            # scope global: preset ficticio mínimo (no se usa stack en global)
            preset = {"stack": "-", "language": "-", "structure": "-", "skills": [],
                      "precommit": [], "maturity": "real",
                      "commands": {"test": "", "lint": "", "typecheck": "", "build": ""}}
            home = Path(args.home) if args.home else Path.home()
            target = home
    except ConfigError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    context = build_context(preset, profile)
    files = generate(core_dir=root / "core", presets_dir=root / "presets",
                     addons_dir=root / "addons", preset=preset, profile=profile,
                     addons=addons, context=context, scope=args.scope)

    report = InstallReport()
    write_tree(target, files, report)
    if preset["maturity"] == "plantilla-base":
        report.warnings.append(f"preset '{preset['stack']}' es plantilla-base, sin probar")
    if args.scope == "project":
        ensure_line(target / ".gitignore", ".claude/", report)

    print(f"Creados ({len(report.created)}): {', '.join(report.created) or '—'}")
    print(f"Ya existían ({len(report.skipped)}): {', '.join(report.skipped) or '—'}")
    for w in report.warnings:
        print(f"aviso: {w}")
    return 0
