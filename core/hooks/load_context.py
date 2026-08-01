#!/usr/bin/env python3
"""SessionStart hook: reinyecta la memoria persistente del proyecto (.claude/context/)
tras compactar/iniciar/reanudar. stdout -> contexto de Claude. Cero dependencias.
Reutiliza los archivos que /update-context y /compact-context mantienen."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    ctx_dir = Path(__file__).resolve().parent.parent / "context"
    if not ctx_dir.is_dir():
        return 0
    files = sorted(ctx_dir.glob("*.md"))
    bodies = [(f.name, f.read_text(encoding="utf-8").strip()) for f in files]
    bodies = [(n, t) for n, t in bodies if t]
    if not bodies:
        return 0
    print("## Memoria persistente del proyecto (.claude/context/) — recargada automáticamente\n")
    for name, text in bodies:
        print(f"### {name}\n\n{text}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
