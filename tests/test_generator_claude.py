from pathlib import Path

from framework.context import build_context
from framework.generators.claude import generate
from framework.loader import load_preset, load_profile
from framework.render import find_unresolved

FIX = Path(__file__).parent / "fixtures"


def _setup():
    preset = load_preset(FIX / "presets", "demo")
    profile = load_profile(FIX / "profiles", "demo")
    ctx = build_context(preset, profile)
    return preset, profile, ctx


def _relpaths(files):
    return {f.relpath for f in files}


def test_global_scope_emits_claude_md_and_global_commands():
    preset, profile, ctx = _setup()
    files = generate(core_dir=FIX / "core", presets_dir=FIX / "presets",
                     addons_dir=FIX / "addons", preset=preset, profile=profile,
                     addons=[], context=ctx, scope="global")
    rel = _relpaths(files)
    assert ".claude/CLAUDE.md" in rel
    assert ".claude/commands/manage-context.md" in rel
    body = next(f.content for f in files if f.relpath == ".claude/CLAUDE.md")
    assert "Lenguaje Demo 1.0." in body  # estándar renderizado
    assert find_unresolved(body) == []


def test_project_scope_emits_expected_tree_and_skills():
    preset, profile, ctx = _setup()
    files = generate(core_dir=FIX / "core", presets_dir=FIX / "presets",
                     addons_dir=FIX / "addons", preset=preset, profile=profile,
                     addons=[], context=ctx, scope="project")
    rel = _relpaths(files)
    assert {"CLAUDE.md", "AGENTS.md", ".claude/settings.json",
            ".claude/commands/new-ticket.md", ".claude/context/MEMORY.md",
            "docs/adr/README.md", ".claude/skills/demo-skill/SKILL.md"} <= rel
    assert all(find_unresolved(f.content) == [] for f in files)
