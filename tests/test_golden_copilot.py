from pathlib import Path

from framework.cli import main
from framework.render import find_unresolved

ROOT = Path(__file__).parent.parent


def _no_unresolved(root: Path):
    for f in root.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".json"}:
            assert find_unresolved(f.read_text(encoding="utf-8")) == [], f


def test_copilot_project_emits_github_tree(tmp_path):
    code = main(["--scope", "project", "--agent", "copilot", "--stack", "python-fastapi",
                 "--profile", "work", "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    instr = tmp_path / ".github" / "copilot-instructions.md"
    assert instr.exists()
    assert (tmp_path / "AGENTS.md").exists()
    # los 6 prompts existen
    prompts = tmp_path / ".github" / "prompts"
    for name in ["new-ticket", "run-tests", "review-pr", "finish-ticket",
                 "update-context", "compact-context"]:
        pf = prompts / f"{name}.prompt.md"
        assert pf.exists(), pf
        assert "description:" in pf.read_text(encoding="utf-8")  # frontmatter Copilot
    # contexto del profile work presente
    assert "AB#" in instr.read_text(encoding="utf-8")
    # NO se generó config de Claude ni se tocó .gitignore con .claude/
    assert not (tmp_path / ".claude").exists()
    _no_unresolved(tmp_path)


def test_copilot_project_emits_path_instructions_and_agents(tmp_path):
    code = main(["--scope", "project", "--agent", "copilot", "--stack", "python-fastapi",
                 "--profile", "work", "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    # path-specific instructions con applyTo del stack
    conv = tmp_path / ".github" / "instructions" / "conventions.instructions.md"
    assert conv.exists()
    body = conv.read_text(encoding="utf-8")
    assert "applyTo: '**/*.py'" in body  # glob del preset python-fastapi
    # custom agents (.agent.md) emitidos
    agents = tmp_path / ".github" / "agents"
    assert (agents / "validator-reviewer.agent.md").exists()
    assert (agents / "pipeline-debugger.agent.md").exists()
    _no_unresolved(tmp_path)


def test_copilot_prompts_carry_agent_field(tmp_path):
    code = main(["--scope", "project", "--agent", "copilot", "--stack", "react-vite",
                 "--profile", "personal", "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    prompts = tmp_path / ".github" / "prompts"
    # prompt agéntico y prompt de solo lectura llevan el campo correcto
    assert "agent: 'agent'" in (prompts / "run-tests.prompt.md").read_text(encoding="utf-8")
    assert "agent: 'ask'" in (prompts / "review-pr.prompt.md").read_text(encoding="utf-8")
    # el glob del stack react-vite llega al applyTo
    conv = tmp_path / ".github" / "instructions" / "conventions.instructions.md"
    assert "applyTo: '**/*.ts,**/*.tsx'" in conv.read_text(encoding="utf-8")


def test_copilot_global_emits_copilot_instructions(tmp_path):
    code = main(["--scope", "global", "--agent", "copilot", "--profile", "personal",
                 "--home", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    instr = tmp_path / ".copilot" / "copilot-instructions.md"
    assert instr.exists()
    body = instr.read_text(encoding="utf-8")
    # estándares neutrales: sin ticket de un profile horneado
    assert "AB#" not in body
    _no_unresolved(tmp_path)


def test_default_agent_is_claude(tmp_path):
    # sin --agent, sigue generando Claude (retrocompatibilidad)
    code = main(["--scope", "project", "--stack", "react-vite", "--profile", "personal",
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    assert (tmp_path / ".claude").exists()
    assert not (tmp_path / ".github" / "copilot-instructions.md").exists()
