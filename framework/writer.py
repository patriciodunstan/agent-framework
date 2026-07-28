"""Escritura idempotente de árboles de archivos y líneas en archivos existentes."""
from __future__ import annotations

from pathlib import Path

from framework.model import InstallReport, OutputFile


def write_tree(target: Path, files: list[OutputFile], report: InstallReport) -> InstallReport:
    for f in files:
        dest = target / f.relpath
        if dest.exists():
            report.skipped.append(f.relpath)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f.content, encoding="utf-8")
        report.created.append(f.relpath)
    return report


def ensure_line(path: Path, line: str, report: InstallReport) -> None:
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    if line in existing:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    new_content = ("\n".join([*existing, line]) + "\n") if existing else line + "\n"
    path.write_text(new_content, encoding="utf-8")
    report.warnings.append(f"añadida línea '{line}' a {path.name}")
