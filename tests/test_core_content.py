from pathlib import Path

ROOT = Path(__file__).parent.parent
CORE = ROOT / "core"


def test_core_expected_files_exist():
    expected = [
        "standards/01-adr.md", "standards/09-testing.md",
        "claude-md/global-header.md", "claude-md/project.md", "agents-md.md",
        "commands/global/setup-standards.md", "commands/project/new-ticket.md",
        "commands/project/finish-ticket.md", "commands/project/run-tests.md",
        "commands/project/review-pr.md", "commands/project/compact-context.md",
        "commands/project/update-context.md",
        "agents/validator-reviewer.md", "context-templates/MEMORY.md",
        "adr/README.md", "adr/template.md", "settings.json",
    ]
    missing = [p for p in expected if not (CORE / p).exists()]
    assert missing == [], f"faltan archivos de core: {missing}"


def test_core_standards_have_at_least_nine_fragments():
    assert len(list((CORE / "standards").glob("*.md"))) >= 9


def test_core_renders_with_full_context():
    from framework.context import build_context
    from framework.render import render
    preset = {"stack": "demo", "language": "Demo", "structure": "app/",
              "skills": [], "precommit": ["test"], "maturity": "real",
              "commands": {"test": "t", "lint": "l", "typecheck": "tc", "build": ""}}
    profile = {"profile": "demo", "agents": ["claude"], "git_host": "github",
               "ci": "gha", "cloud": "aws", "ticket_format": "#n",
               "branch_pattern": "feature/n"}
    ctx = build_context(preset, profile)
    for md in CORE.rglob("*.md"):
        render(md.read_text(encoding="utf-8"), ctx, source=str(md))
