#!/usr/bin/env python3
"""SessionStart hook: reinyecta la memoria persistente del proyecto (.claude/context/)
tras compactar/iniciar/reanudar. stdout -> contexto de Claude. Cero dependencias.

Divulgación progresiva para no gastar contexto: MEMORY.md entra completo (es la
memoria que se lee siempre); del resto solo se inyecta un índice de una línea por
archivo, y Claude los lee bajo demanda. Reutiliza los archivos que /update-context
y /compact-context mantienen."""
from __future__ import annotations

import sys
from pathlib import Path

SIEMPRE = "MEMORY.md"  # único archivo que se inyecta entero


def _titulo(texto: str) -> str:
    """Primer encabezado del archivo, como descriptor para el índice."""
    for linea in texto.splitlines():
        if linea.startswith("#"):
            return linea.lstrip("#").strip()
    return ""


def main() -> int:
    # En Windows la consola por defecto es cp1252: sin esto los acentos y las rayas
    # llegan a Claude como mojibake.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ctx_dir = Path(__file__).resolve().parent.parent / "context"
    if not ctx_dir.is_dir():
        return 0
    archivos = [(f, f.read_text(encoding="utf-8").strip()) for f in sorted(ctx_dir.glob("*.md"))]
    archivos = [(f, t) for f, t in archivos if t]
    if not archivos:
        return 0

    memoria = [(f, t) for f, t in archivos if f.name == SIEMPRE]
    resto = [(f, t) for f, t in archivos if f.name != SIEMPRE]

    print("## Memoria persistente del proyecto (.claude/context/) — recargada automáticamente\n")
    for f, texto in memoria:
        print(f"### {f.name}\n\n{texto}\n")
    if resto:
        print("### Contexto disponible bajo demanda\n")
        print("Leer con `Read` solo el que corresponda al módulo en que se trabaje:\n")
        for f, texto in resto:
            desc = _titulo(texto)
            lineas = len(texto.splitlines())
            sufijo = f" — {desc}" if desc else ""
            print(f"- `.claude/context/{f.name}`{sufijo} ({lineas} líneas)")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
