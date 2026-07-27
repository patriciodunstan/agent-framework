from framework.context import build_context

PRESET_REAL = {
    "stack": "python-fastapi",
    "language": "Python 3.12+",
    "structure": "app/",
    "skills": ["a"],
    "precommit": ["test", "lint"],
    "maturity": "real",
    "commands": {
        "test": "pytest -q",
        "lint": "ruff check app/",
        "typecheck": "mypy app/",
        "build": "",
    },
}
PROFILE_WORK = {
    "profile": "work",
    "agents": ["claude"],
    "git_host": "github",
    "ci": "azure-pipelines",
    "cloud": "azure",
    "ticket_format": "AB#<número>",
    "branch_pattern": "feature/AB#<n>-descripcion",
}


def test_context_has_all_keys():
    ctx = build_context(PRESET_REAL, PROFILE_WORK)
    expected = {
        "stack", "language", "structure", "test_cmd", "lint_cmd", "typecheck_cmd",
        "build_cmd", "precommit_steps", "profile", "git_host", "ci", "cloud",
        "ticket_format", "branch_pattern", "maturity_warning",
    }
    assert set(ctx) == expected
    assert all(isinstance(v, str) for v in ctx.values())


def test_precommit_steps_numbered():
    ctx = build_context(PRESET_REAL, PROFILE_WORK)
    assert ctx["precommit_steps"] == "1. `pytest -q`\n2. `ruff check app/`"


def test_maturity_warning_empty_for_real():
    assert build_context(PRESET_REAL, PROFILE_WORK)["maturity_warning"] == ""


def test_maturity_warning_present_for_plantilla():
    preset = {**PRESET_REAL, "maturity": "plantilla-base"}
    assert "sin probar" in build_context(preset, PROFILE_WORK)["maturity_warning"].lower()
