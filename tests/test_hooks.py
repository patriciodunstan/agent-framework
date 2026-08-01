"""Verifica que el generador Claude emita los hooks de contexto y que los scripts
emitidos funcionen de verdad (flujo real end-to-end, no mocks)."""
import json
import subprocess
import sys
from pathlib import Path

from framework.cli import main

ROOT = Path(__file__).parent.parent


def _install_project(tmp_path):
    code = main(["--scope", "project", "--stack", "python-fastapi", "--profile", "work",
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    return tmp_path


def test_project_emits_hooks_and_settings_wiring(tmp_path):
    _install_project(tmp_path)
    hooks = tmp_path / ".claude" / "hooks"
    assert (hooks / "load_context.py").exists()
    assert (hooks / "snapshot_transcript.py").exists()
    settings = json.loads((tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8"))
    assert "SessionStart" in settings["hooks"]
    assert "PreCompact" in settings["hooks"]
    # el comando referencia el script emitido
    cmd = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    assert ".claude/hooks/load_context.py" in cmd


def test_load_context_reinjects_context_files(tmp_path):
    _install_project(tmp_path)
    script = tmp_path / ".claude" / "hooks" / "load_context.py"
    out = subprocess.run([sys.executable, str(script)], capture_output=True,
                         text=True, encoding="utf-8")
    assert out.returncode == 0
    assert "Memoria persistente del proyecto" in out.stdout
    # incluye al menos uno de los archivos de contexto reales
    assert "MEMORY.md" in out.stdout


def test_snapshot_transcript_copies_raw_session(tmp_path):
    _install_project(tmp_path)
    script = tmp_path / ".claude" / "hooks" / "snapshot_transcript.py"
    fake_transcript = tmp_path / "session.jsonl"
    fake_transcript.write_text('{"role":"user"}\n', encoding="utf-8")
    event = json.dumps({"transcript_path": str(fake_transcript),
                        "compaction_trigger": "manual"})
    out = subprocess.run([sys.executable, str(script)], input=event,
                         capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0
    snaps = list((tmp_path / ".claude" / "snapshots").glob("transcript-*-manual.jsonl"))
    assert len(snaps) == 1
    assert snaps[0].read_text(encoding="utf-8") == '{"role":"user"}\n'


def test_snapshot_transcript_no_crash_on_bad_input(tmp_path):
    _install_project(tmp_path)
    script = tmp_path / ".claude" / "hooks" / "snapshot_transcript.py"
    out = subprocess.run([sys.executable, str(script)], input="not-json",
                         capture_output=True, text=True, encoding="utf-8")
    assert out.returncode == 0  # nunca bloquea la compactación
