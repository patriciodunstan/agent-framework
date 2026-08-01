#!/usr/bin/env python3
"""PreCompact hook: guarda un snapshot del transcript antes de compactar, para nunca
perder la sesión cruda. NO resume (eso lo hace /compact-context con el modelo).
Lee el JSON del evento por stdin. Cero dependencias."""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    src = event.get("transcript_path")
    if not src or not Path(src).is_file():
        return 0
    dest_dir = Path(__file__).resolve().parent.parent / "snapshots"
    dest_dir.mkdir(parents=True, exist_ok=True)
    trigger = event.get("compaction_trigger", "?")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = dest_dir / f"transcript-{stamp}-{trigger}.jsonl"
    shutil.copy2(src, dest)
    print(f"[agent-framework] Snapshot de sesion guardado: {dest.name}. "
          f"Corre /compact-context si queres un resumen semantico.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
