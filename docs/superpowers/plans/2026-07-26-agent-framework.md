# Agent Framework — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir `agent-framework`: un repo que estampa configuración de agentes (Claude Code) en dos niveles (global `~/.claude/` y proyecto) a partir de una fuente única neutral, parametrizada por `stack`, `profile` y `addons`.

**Architecture:** Un motor Python sin dependencias lee datos (`presets/*.toml`, `profiles/*.toml`, `addons/*/addon.toml`), construye un contexto de variables, y un generador por agente (`generators/claude.py`) renderiza plantillas neutrales de `core/` en una lista de archivos que un escritor idempotente vuelca en el destino. El CLI (`install.py`) orquesta.

**Tech Stack:** Python 3.11+ (stdlib únicamente: `tomllib`, `string.Template`, `argparse`, `pathlib`, `dataclasses`), `pytest` para tests, `ruff` para lint.

## Global Constraints

- **Python 3.11+** — obligatorio (usamos `tomllib`, stdlib solo-lectura de TOML).
- **Cero dependencias de runtime** — solo stdlib. `pytest` y `ruff` son dev-only.
- **Formato de datos:** presets/profiles/addons en **TOML**. Nada de YAML/PyYAML.
- **Templating:** `string.Template` con placeholders `${nombre}`. El `$` literal en contenido se escapa como `$$`.
- **Idempotencia:** el instalador nunca pisa un archivo existente; agrega lo que falta y reporta.
- **Falla dura ante placeholder sin resolver:** jamás se escribe un archivo con `${...}` residual.
- **Convención de commits:** `tipo(scope): descripción`; cada commit termina con `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **Extracción, no invención:** el contenido de `core/` se genera desde las configs reales (`C:\Users\patriciods\lambda-scanner\UDLA_backend_ssh` sobre todo) y el `~/.claude/CLAUDE.md`. Cada archivo de `core/` documenta su origen.
- **Idioma:** todo el contenido de usuario (plantillas, docs, mensajes del CLI) en español, igual que las configs de origen.

---

## Estructura de archivos

```
agent-framework/
├── install.py                      # CLI fino → framework.cli.main()
├── pyproject.toml                  # metadata + config de ruff (sin deps de runtime)
├── framework/
│   ├── __init__.py
│   ├── model.py                    # OutputFile, InstallReport, ConfigError
│   ├── render.py                   # render(), find_unresolved(), UnresolvedPlaceholderError
│   ├── loader.py                   # load_preset/profile/addon + validación (tomllib)
│   ├── context.py                  # build_context(preset, profile) -> dict[str,str]
│   ├── writer.py                   # write_tree(), ensure_line() idempotentes
│   ├── cli.py                      # argparse + orquestación + impresión de reporte
│   └── generators/
│       ├── __init__.py
│       └── claude.py               # generate(...) -> list[OutputFile]
├── core/                           # contenido NEUTRAL (Task 8)
│   ├── standards/                  # 0N-*.md fragmentos ordenados
│   ├── commands/{global,project}/  # commands como plantillas
│   ├── agents/                     # subagents neutrales
│   ├── context-templates/          # MEMORY.md, architecture.md, ...
│   ├── adr/                        # README.md, template.md
│   ├── claude-md/                  # global-header.md, project.md
│   ├── agents-md.md                # plantilla AGENTS.md
│   └── settings.json               # settings.json base de proyecto
├── presets/<stack>/preset.toml (+ skills/)   # Tasks 9,10
├── profiles/{personal,work}.toml             # Task 9
├── addons/{docker,k8s}/addon.toml (+ skills/) # Task 11
├── tests/
│   ├── fixtures/                   # core/preset/profile/addon mínimos para tests de motor
│   ├── test_render.py
│   ├── test_loader.py
│   ├── test_context.py
│   ├── test_writer.py
│   ├── test_generator_claude.py
│   ├── test_cli.py
│   ├── test_golden.py             # golden-master scope×stack×profile(+addons)
│   └── test_idempotency.py
├── docs/
│   ├── adr/                        # ADRs del propio framework (Task 13)
│   ├── superpowers/specs/2026-07-26-agent-framework-design.md
│   └── superpowers/plans/2026-07-26-agent-framework.md
└── README.md
```

### Contrato de variables de contexto (usado por todas las plantillas)

`build_context` produce exactamente estas claves string:

| Variable | Origen | Ejemplo |
|----------|--------|---------|
| `${stack}` | preset.stack | `python-fastapi` |
| `${language}` | preset.language | `Python 3.12+` |
| `${structure}` | preset.structure | (bloque de árbol) |
| `${test_cmd}` | preset.commands.test | `pytest tests/ -q` |
| `${lint_cmd}` | preset.commands.lint | `ruff check app/` |
| `${typecheck_cmd}` | preset.commands.typecheck | `mypy app/` |
| `${build_cmd}` | preset.commands.build (o `""`) | `` |
| `${precommit_steps}` | derivado de preset.precommit | `1. \`pytest tests/ -q\`\n2. \`ruff check app/\`` |
| `${profile}` | profile.profile | `work` |
| `${git_host}` | profile.git_host | `github` |
| `${ci}` | profile.ci | `azure-pipelines` |
| `${cloud}` | profile.cloud (o `""`) | `azure` |
| `${ticket_format}` | profile.ticket_format | `AB#<número>` |
| `${branch_pattern}` | profile.branch_pattern | `feature/AB#<n>-descripcion` |
| `${maturity_warning}` | preset.maturity | `""` (real) o bloque de aviso |

Las listas `preset.skills` y `addon.skills` NO son variables de texto: el generador las usa para decidir qué carpetas de `skills/` copiar.

---

## Task 1: Andamiaje del repo y arnés de tests

**Files:**
- Create: `pyproject.toml`
- Create: `framework/__init__.py` (vacío)
- Create: `framework/model.py`
- Create: `tests/test_smoke.py`
- Create: `.gitignore` (ya existe con `.claude/`, `__pycache__/`, etc. — verificar)

**Interfaces:**
- Produces: `framework.model.OutputFile(relpath: str, content: str)` (frozen dataclass); `framework.model.InstallReport` con listas `created`, `skipped`, `warnings`; `framework.model.ConfigError(Exception)`.

- [ ] **Step 1: Crear `pyproject.toml`**

```toml
[project]
name = "agent-framework"
version = "0.1.0"
description = "Configurador portable de agentes de IA (Claude Code)"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: Crear `framework/model.py`**

```python
"""Tipos compartidos por el motor del framework."""
from __future__ import annotations

from dataclasses import dataclass, field


class ConfigError(Exception):
    """Error de configuración de entrada (stack/profile/addon inválido o incompleto)."""


@dataclass(frozen=True)
class OutputFile:
    """Un archivo a escribir, con ruta relativa al destino de instalación."""

    relpath: str
    content: str


@dataclass
class InstallReport:
    """Resultado de una instalación idempotente."""

    created: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
```

- [ ] **Step 3: Crear `framework/__init__.py` y `tests/test_smoke.py`**

`framework/__init__.py`: archivo vacío.

`tests/test_smoke.py`:
```python
from framework.model import ConfigError, InstallReport, OutputFile


def test_outputfile_is_frozen():
    f = OutputFile("CLAUDE.md", "hola")
    assert f.relpath == "CLAUDE.md"
    assert f.content == "hola"


def test_installreport_defaults_empty():
    r = InstallReport()
    assert r.created == [] and r.skipped == [] and r.warnings == []


def test_configerror_is_exception():
    assert issubclass(ConfigError, Exception)
```

- [ ] **Step 4: Correr tests y lint**

Run: `python -m pytest tests/test_smoke.py -v && python -m ruff check .`
Expected: 3 passed; ruff sin errores.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml framework/ tests/test_smoke.py .gitignore
git commit -m "chore(scaffold): estructura del motor y arnés de tests

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Motor de render (`render.py`)

**Files:**
- Create: `framework/render.py`
- Test: `tests/test_render.py`

**Interfaces:**
- Consumes: nada.
- Produces: `render(text: str, context: dict[str, str], *, source: str = "<texto>") -> str`; `find_unresolved(text: str) -> list[str]`; `UnresolvedPlaceholderError(Exception)` con atributos `.placeholders: list[str]` y `.source: str`.

- [ ] **Step 1: Escribir el test que falla — `tests/test_render.py`**

```python
import pytest

from framework.render import (
    UnresolvedPlaceholderError,
    find_unresolved,
    render,
)


def test_render_substitutes_known_placeholders():
    out = render("Lenguaje: ${language}", {"language": "Python 3.12+"})
    assert out == "Lenguaje: Python 3.12+"


def test_render_escaped_dollar_is_literal():
    out = render("usa $$HOME en shell", {})
    assert out == "usa $HOME en shell"


def test_find_unresolved_lists_missing():
    assert find_unresolved("a ${x} b ${y} ${x}") == ["x", "y"]


def test_render_raises_on_unresolved():
    with pytest.raises(UnresolvedPlaceholderError) as exc:
        render("hola ${falta}", {}, source="core/x.md")
    assert exc.value.placeholders == ["falta"]
    assert exc.value.source == "core/x.md"
```

- [ ] **Step 2: Correr para ver que falla**

Run: `python -m pytest tests/test_render.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.render`.

- [ ] **Step 3: Implementar `framework/render.py`**

```python
"""Render de plantillas con string.Template y detección de placeholders sin resolver."""
from __future__ import annotations

import re
from string import Template

_PLACEHOLDER_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


class UnresolvedPlaceholderError(Exception):
    def __init__(self, placeholders: list[str], source: str) -> None:
        self.placeholders = placeholders
        self.source = source
        super().__init__(
            f"Placeholders sin resolver en {source}: {', '.join(placeholders)}"
        )


def find_unresolved(text: str) -> list[str]:
    """Devuelve los nombres de placeholders ${...} presentes, ordenados y únicos."""
    return sorted(set(_PLACEHOLDER_RE.findall(text)))


def render(text: str, context: dict[str, str], *, source: str = "<texto>") -> str:
    """Sustituye ${var}; falla si queda algún ${...} sin resolver."""
    result = Template(text).safe_substitute(context)
    unresolved = find_unresolved(result)
    if unresolved:
        raise UnresolvedPlaceholderError(unresolved, source)
    return result
```

- [ ] **Step 4: Correr para ver que pasa**

Run: `python -m pytest tests/test_render.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add framework/render.py tests/test_render.py
git commit -m "feat(render): motor de plantillas con detección de placeholders sin resolver

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Carga y validación de datos (`loader.py`)

**Files:**
- Create: `framework/loader.py`
- Create: `tests/fixtures/presets/demo/preset.toml`
- Create: `tests/fixtures/profiles/demo.toml`
- Create: `tests/fixtures/addons/demo/addon.toml`
- Test: `tests/test_loader.py`

**Interfaces:**
- Consumes: `framework.model.ConfigError`.
- Produces:
  - `load_preset(presets_dir: Path, stack: str) -> dict`
  - `load_profile(profiles_dir: Path, name: str) -> dict`
  - `load_addon(addons_dir: Path, name: str) -> dict`
  - `available(dir: Path) -> list[str]` (subdirectorios ordenados)

  Claves requeridas: preset → `{stack, language, commands, structure, skills, precommit, maturity}` con `maturity ∈ {real, plantilla-base}`; profile → `{profile, agents, git_host, ci, ticket_format, branch_pattern}`; addon → `{addon, skills}`.

- [ ] **Step 1: Crear fixtures**

`tests/fixtures/presets/demo/preset.toml`:
```toml
stack = "demo"
language = "Demo 1.0"
structure = "app/"
skills = ["demo-skill"]
precommit = ["test"]
maturity = "real"

[commands]
test = "demo test"
lint = "demo lint"
typecheck = "demo typecheck"
build = ""
```

`tests/fixtures/profiles/demo.toml`:
```toml
profile = "demo"
agents = ["claude"]
git_host = "github"
ci = "github-actions"
cloud = "aws"
ticket_format = "#<número>"
branch_pattern = "feature/<n>-descripcion"
```

`tests/fixtures/addons/demo/addon.toml`:
```toml
addon = "demo"
skills = ["demo-addon-skill"]
```

- [ ] **Step 2: Escribir el test que falla — `tests/test_loader.py`**

```python
from pathlib import Path

import pytest

from framework.loader import available, load_addon, load_preset, load_profile
from framework.model import ConfigError

FIX = Path(__file__).parent / "fixtures"


def test_load_preset_ok():
    p = load_preset(FIX / "presets", "demo")
    assert p["stack"] == "demo"
    assert p["commands"]["test"] == "demo test"


def test_load_preset_unknown_lists_available():
    with pytest.raises(ConfigError) as exc:
        load_preset(FIX / "presets", "noexiste")
    assert "demo" in str(exc.value)


def test_load_preset_missing_key(tmp_path):
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "preset.toml").write_text('stack = "bad"\n', encoding="utf-8")
    with pytest.raises(ConfigError):
        load_preset(tmp_path, "bad")


def test_load_profile_ok():
    pr = load_profile(FIX / "profiles", "demo")
    assert pr["git_host"] == "github"


def test_load_addon_ok():
    a = load_addon(FIX / "addons", "demo")
    assert a["skills"] == ["demo-addon-skill"]


def test_available_sorted():
    assert available(FIX / "presets") == ["demo"]
```

- [ ] **Step 3: Correr para ver que falla**

Run: `python -m pytest tests/test_loader.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.loader`.

- [ ] **Step 4: Implementar `framework/loader.py`**

```python
"""Carga y validación de presets, profiles y addons desde TOML (stdlib tomllib)."""
from __future__ import annotations

import tomllib
from pathlib import Path

from framework.model import ConfigError

_PRESET_KEYS = {"stack", "language", "commands", "structure", "skills", "precommit", "maturity"}
_PROFILE_KEYS = {"profile", "agents", "git_host", "ci", "ticket_format", "branch_pattern"}
_ADDON_KEYS = {"addon", "skills"}
_VALID_MATURITY = {"real", "plantilla-base"}


def available(directory: Path) -> list[str]:
    if not directory.exists():
        return []
    return sorted(p.name for p in directory.iterdir() if p.is_dir())


def _load_toml(path: Path) -> dict:
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _require(data: dict, keys: set[str], what: str) -> None:
    missing = keys - data.keys()
    if missing:
        raise ConfigError(f"{what} incompleto, faltan claves: {', '.join(sorted(missing))}")


def load_preset(presets_dir: Path, stack: str) -> dict:
    path = presets_dir / stack / "preset.toml"
    if not path.exists():
        raise ConfigError(
            f"stack '{stack}' no existe. Disponibles: {', '.join(available(presets_dir))}"
        )
    data = _load_toml(path)
    _require(data, _PRESET_KEYS, f"preset '{stack}'")
    if data["maturity"] not in _VALID_MATURITY:
        raise ConfigError(
            f"preset '{stack}': maturity '{data['maturity']}' inválido "
            f"(usar {' o '.join(sorted(_VALID_MATURITY))})"
        )
    return data


def load_profile(profiles_dir: Path, name: str) -> dict:
    path = profiles_dir / f"{name}.toml"
    if not path.exists():
        names = sorted(p.stem for p in profiles_dir.glob("*.toml"))
        raise ConfigError(f"profile '{name}' no existe. Disponibles: {', '.join(names)}")
    data = _load_toml(path)
    _require(data, _PROFILE_KEYS, f"profile '{name}'")
    return data


def load_addon(addons_dir: Path, name: str) -> dict:
    path = addons_dir / name / "addon.toml"
    if not path.exists():
        raise ConfigError(
            f"addon '{name}' no existe. Disponibles: {', '.join(available(addons_dir))}"
        )
    data = _load_toml(path)
    _require(data, _ADDON_KEYS, f"addon '{name}'")
    return data
```

- [ ] **Step 5: Correr para ver que pasa**

Run: `python -m pytest tests/test_loader.py -v`
Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add framework/loader.py tests/test_loader.py tests/fixtures
git commit -m "feat(loader): carga y validación de presets/profiles/addons en TOML

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: Construcción del contexto (`context.py`)

**Files:**
- Create: `framework/context.py`
- Test: `tests/test_context.py`

**Interfaces:**
- Consumes: dicts de `load_preset`/`load_profile`.
- Produces: `build_context(preset: dict, profile: dict) -> dict[str, str]` con exactamente las claves del "Contrato de variables de contexto".

- [ ] **Step 1: Escribir el test que falla — `tests/test_context.py`**

```python
from framework.context import build_context

PRESET_REAL = {
    "stack": "python-fastapi",
    "language": "Python 3.12+",
    "structure": "app/",
    "skills": ["a"],
    "precommit": ["test", "lint"],
    "maturity": "real",
    "commands": {"test": "pytest -q", "lint": "ruff check app/", "typecheck": "mypy app/", "build": ""},
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
```

- [ ] **Step 2: Correr para ver que falla**

Run: `python -m pytest tests/test_context.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.context`.

- [ ] **Step 3: Implementar `framework/context.py`**

```python
"""Construye el diccionario de variables de contexto para el render de plantillas."""
from __future__ import annotations

_COMMAND_KEYS = {
    "test": "test_cmd",
    "lint": "lint_cmd",
    "typecheck": "typecheck_cmd",
    "build": "build_cmd",
}

_MATURITY_WARNING = (
    "> ⚠️ **Preset sin probar en proyecto real todavía.** Es una plantilla base: "
    "revisá y endurecé las convenciones antes de confiar en ella.\n"
)


def _precommit_steps(preset: dict) -> str:
    cmds = preset["commands"]
    lines = []
    for i, key in enumerate(preset["precommit"], start=1):
        lines.append(f"{i}. `{cmds.get(key, '')}`")
    return "\n".join(lines)


def build_context(preset: dict, profile: dict) -> dict[str, str]:
    ctx: dict[str, str] = {
        "stack": preset["stack"],
        "language": preset["language"],
        "structure": preset["structure"],
        "precommit_steps": _precommit_steps(preset),
        "profile": profile["profile"],
        "git_host": profile["git_host"],
        "ci": profile["ci"],
        "cloud": profile.get("cloud", ""),
        "ticket_format": profile["ticket_format"],
        "branch_pattern": profile["branch_pattern"],
        "maturity_warning": _MATURITY_WARNING if preset["maturity"] == "plantilla-base" else "",
    }
    for src, dst in _COMMAND_KEYS.items():
        ctx[dst] = preset["commands"].get(src) or ""
    return {k: str(v) for k, v in ctx.items()}
```

- [ ] **Step 4: Correr para ver que pasa**

Run: `python -m pytest tests/test_context.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add framework/context.py tests/test_context.py
git commit -m "feat(context): construcción del contexto de variables desde preset+profile

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: Escritor idempotente (`writer.py`)

**Files:**
- Create: `framework/writer.py`
- Test: `tests/test_writer.py`

**Interfaces:**
- Consumes: `framework.model.OutputFile`, `framework.model.InstallReport`.
- Produces:
  - `write_tree(target: Path, files: list[OutputFile], report: InstallReport) -> InstallReport` — crea archivos que no existen (creando dirs padre), salta los existentes, registra en `created`/`skipped`.
  - `ensure_line(path: Path, line: str, report: InstallReport) -> None` — crea el archivo o agrega la línea si falta; idempotente.

- [ ] **Step 1: Escribir el test que falla — `tests/test_writer.py`**

```python
from framework.model import InstallReport, OutputFile
from framework.writer import ensure_line, write_tree


def test_write_tree_creates_and_reports(tmp_path):
    files = [OutputFile("a/b.txt", "hola"), OutputFile("c.txt", "mundo")]
    report = write_tree(tmp_path, files, InstallReport())
    assert (tmp_path / "a" / "b.txt").read_text(encoding="utf-8") == "hola"
    assert set(report.created) == {"a/b.txt", "c.txt"}


def test_write_tree_is_idempotent(tmp_path):
    files = [OutputFile("a.txt", "v1")]
    write_tree(tmp_path, files, InstallReport())
    report2 = write_tree(tmp_path, [OutputFile("a.txt", "v2")], InstallReport())
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "v1"  # no se pisa
    assert report2.skipped == ["a.txt"]
    assert report2.created == []


def test_ensure_line_creates_then_noop(tmp_path):
    gi = tmp_path / ".gitignore"
    report = InstallReport()
    ensure_line(gi, ".claude/", report)
    ensure_line(gi, ".claude/", report)
    assert gi.read_text(encoding="utf-8").count(".claude/") == 1
```

- [ ] **Step 2: Correr para ver que falla**

Run: `python -m pytest tests/test_writer.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.writer`.

- [ ] **Step 3: Implementar `framework/writer.py`**

```python
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
```

- [ ] **Step 4: Correr para ver que pasa**

Run: `python -m pytest tests/test_writer.py -v`
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add framework/writer.py tests/test_writer.py
git commit -m "feat(writer): escritura idempotente de árboles y ensure_line

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: Generador Claude (`generators/claude.py`)

**Files:**
- Create: `framework/generators/__init__.py` (vacío)
- Create: `framework/generators/claude.py`
- Create: fixtures de core mínimo bajo `tests/fixtures/core/` y skills bajo `tests/fixtures/presets/demo/skills/demo-skill/SKILL.md`
- Test: `tests/test_generator_claude.py`

**Interfaces:**
- Consumes: `render.render`, `model.OutputFile`, dicts de preset/profile/addon, `context` de `build_context`.
- Produces:
  ```python
  def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
               preset: dict, profile: dict, addons: list[dict],
               context: dict[str, str], scope: str) -> list[OutputFile]
  ```
  - `scope == "global"` → emite `.claude/CLAUDE.md` (header + estándares concatenados y renderizados) y `.claude/commands/<n>.md` para cada archivo en `core/commands/global/`.
  - `scope == "project"` → emite `CLAUDE.md` (de `core/claude-md/project.md`), `AGENTS.md` (de `core/agents-md.md`), `.claude/commands/<n>.md` (de `core/commands/project/`), `.claude/agents/<n>.md`, `.claude/context/<n>.md`, `.claude/settings.json` (de `core/settings.json`), `docs/adr/README.md` y `docs/adr/template.md`, y las skills de `preset.skills` + skills de cada addon (copiadas desde `presets/<stack>/skills/<skill>/**` y `addons/<addon>/skills/<skill>/**`).

- [ ] **Step 1: Crear fixtures de core mínimo**

`tests/fixtures/core/standards/01-demo.md`: `## Estándar demo\nLenguaje ${language}.\n`
`tests/fixtures/core/claude-md/global-header.md`: `# CLAUDE.md global (${profile})\n`
`tests/fixtures/core/claude-md/project.md`: `# CLAUDE.md — ${stack}\nComplementa ~/.claude/CLAUDE.md.\n${maturity_warning}Tests: ${test_cmd}\n`
`tests/fixtures/core/agents-md.md`: `# AGENTS.md\nStack ${stack}.\n`
`tests/fixtures/core/agents-md.md` (nota: un solo archivo).
`tests/fixtures/core/commands/global/manage-context.md`: `# manage-context\n`
`tests/fixtures/core/commands/project/new-ticket.md`: `# new-ticket (${ticket_format})\n`
`tests/fixtures/core/agents/validator.md`: `# validator para ${language}\n`
`tests/fixtures/core/context-templates/MEMORY.md`: `# MEMORY ${stack}\n`
`tests/fixtures/core/adr/README.md`: `# ADR\n`
`tests/fixtures/core/adr/template.md`: `# ADR-NNNN\n`
`tests/fixtures/core/settings.json`: `{}\n`
`tests/fixtures/presets/demo/skills/demo-skill/SKILL.md`: `# demo skill para ${stack}\n`

- [ ] **Step 2: Escribir el test que falla — `tests/test_generator_claude.py`**

```python
from pathlib import Path

from framework.context import build_context
from framework.generators.claude import generate
from framework.loader import load_preset, load_profile

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
    assert "${" not in body


def test_project_scope_emits_expected_tree_and_skills():
    preset, profile, ctx = _setup()
    files = generate(core_dir=FIX / "core", presets_dir=FIX / "presets",
                     addons_dir=FIX / "addons", preset=preset, profile=profile,
                     addons=[], context=ctx, scope="project")
    rel = _relpaths(files)
    assert {"CLAUDE.md", "AGENTS.md", ".claude/settings.json",
            ".claude/commands/new-ticket.md", ".claude/context/MEMORY.md",
            "docs/adr/README.md", ".claude/skills/demo-skill/SKILL.md"} <= rel
    assert all("${" not in f.content for f in files)
```

- [ ] **Step 3: Correr para ver que falla**

Run: `python -m pytest tests/test_generator_claude.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.generators.claude`.

- [ ] **Step 4: Implementar `framework/generators/__init__.py` (vacío) y `framework/generators/claude.py`**

```python
"""Generador para Claude Code: (core + preset + profile + addons) -> archivos."""
from __future__ import annotations

from pathlib import Path

from framework.model import OutputFile
from framework.render import render


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rendered(path: Path, context: dict[str, str], relpath: str) -> OutputFile:
    return OutputFile(relpath, render(_read(path), context, source=str(path)))


def _standards_body(core_dir: Path, context: dict[str, str]) -> str:
    fragments = sorted((core_dir / "standards").glob("*.md"))
    joined = "\n".join(_read(f) for f in fragments)
    return render(joined, context, source="core/standards/*")


def _copy_command_dir(core_dir: Path, sub: str, context: dict[str, str]) -> list[OutputFile]:
    out = []
    for f in sorted((core_dir / "commands" / sub).glob("*.md")):
        out.append(_rendered(f, context, f".claude/commands/{f.name}"))
    return out


def _copy_skill_dirs(base: Path, skills: list[str], context: dict[str, str]) -> list[OutputFile]:
    out = []
    for skill in skills:
        skill_dir = base / skill
        if not skill_dir.exists():
            continue
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                rel = f.relative_to(skill_dir).as_posix()
                out.append(_rendered(f, context, f".claude/skills/{skill}/{rel}"))
    return out


def generate(*, core_dir: Path, presets_dir: Path, addons_dir: Path,
             preset: dict, profile: dict, addons: list[dict],
             context: dict[str, str], scope: str) -> list[OutputFile]:
    if scope == "global":
        header = render(_read(core_dir / "claude-md" / "global-header.md"), context,
                        source="core/claude-md/global-header.md")
        body = header + "\n" + _standards_body(core_dir, context)
        files = [OutputFile(".claude/CLAUDE.md", body)]
        files += _copy_command_dir(core_dir, "global", context)
        return files

    if scope == "project":
        files: list[OutputFile] = [
            _rendered(core_dir / "claude-md" / "project.md", context, "CLAUDE.md"),
            _rendered(core_dir / "agents-md.md", context, "AGENTS.md"),
            OutputFile(".claude/settings.json", _read(core_dir / "settings.json")),
            _rendered(core_dir / "adr" / "README.md", context, "docs/adr/README.md"),
            _rendered(core_dir / "adr" / "template.md", context, "docs/adr/template.md"),
        ]
        files += _copy_command_dir(core_dir, "project", context)
        for f in sorted((core_dir / "agents").glob("*.md")):
            files.append(_rendered(f, context, f".claude/agents/{f.name}"))
        for f in sorted((core_dir / "context-templates").glob("*.md")):
            files.append(_rendered(f, context, f".claude/context/{f.name}"))
        files += _copy_skill_dirs(presets_dir / preset["stack"] / "skills",
                                  preset["skills"], context)
        for addon in addons:
            files += _copy_skill_dirs(addons_dir / addon["addon"] / "skills",
                                      addon["skills"], context)
        return files

    raise ValueError(f"scope desconocido: {scope}")
```

- [ ] **Step 5: Correr para ver que pasa**

Run: `python -m pytest tests/test_generator_claude.py -v`
Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add framework/generators tests/test_generator_claude.py tests/fixtures/core tests/fixtures/presets/demo/skills
git commit -m "feat(generator): generador Claude para scopes global y project

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: CLI (`cli.py` + `install.py`)

**Files:**
- Create: `framework/cli.py`
- Create: `install.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: `framework.cli.main(argv: list[str] | None = None) -> int`. Flags: `--scope {global,project}` (req), `--stack` (req si project), `--profile` (req), `--addons` (csv, opcional), `--target` (req si project), `--home` (opcional, override de `~` para scope global/tests), `--root` (opcional, raíz del framework; default: carpeta de `install.py`). Devuelve 0 en éxito, 2 en `ConfigError`.

- [ ] **Step 1: Escribir el test que falla — `tests/test_cli.py`**

```python
from pathlib import Path

from framework.cli import main

ROOT = Path(__file__).parent / "fixtures"


def test_cli_project_scope_writes_files(tmp_path, capsys):
    code = main(["--scope", "project", "--stack", "demo", "--profile", "demo",
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "commands" / "new-ticket.md").exists()
    assert ".claude/" in (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert "Creados" in capsys.readouterr().out


def test_cli_global_scope_uses_home(tmp_path):
    code = main(["--scope", "global", "--profile", "demo",
                 "--home", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()


def test_cli_unknown_stack_returns_2(capsys):
    code = main(["--scope", "project", "--stack", "noexiste", "--profile", "demo",
                 "--target", ".", "--root", str(ROOT)])
    assert code == 2
    assert "no existe" in capsys.readouterr().err


def test_cli_unknown_addon_returns_2(tmp_path, capsys):
    code = main(["--scope", "project", "--stack", "demo", "--profile", "demo",
                 "--addons", "noexiste", "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 2
    assert "addon" in capsys.readouterr().err.lower()
```

> Nota: el `--root` de los tests apunta a `tests/fixtures`, que ya contiene `core/`, `presets/`, `profiles/`, `addons/`.

- [ ] **Step 2: Correr para ver que falla**

Run: `python -m pytest tests/test_cli.py -v`
Expected: FAIL con `ModuleNotFoundError: framework.cli`.

- [ ] **Step 3: Implementar `framework/cli.py`**

```python
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
```

- [ ] **Step 4: Implementar `install.py`**

```python
#!/usr/bin/env python3
"""Punto de entrada del configurador de agentes. Ver README.md."""
import sys

from framework.cli import main

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Correr para ver que pasa**

Run: `python -m pytest tests/test_cli.py -v`
Expected: 4 passed.

- [ ] **Step 6: Correr toda la suite y lint**

Run: `python -m pytest -q && python -m ruff check .`
Expected: todo verde, ruff limpio.

- [ ] **Step 7: Commit**

```bash
git add framework/cli.py install.py tests/test_cli.py
git commit -m "feat(cli): orquestador install.py con validación y reporte idempotente

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: Contenido neutral de `core/` (extracción real)

**Files (crear todos bajo `core/`):**
- `core/standards/01-adr.md`, `02-config-local.md`, `03-verificar-no-inferir.md`, `04-anti-alucinacion.md`, `05-multiagente.md`, `06-tokens.md`, `07-git.md`, `08-seguridad.md`, `09-testing.md`
- `core/claude-md/global-header.md`, `core/claude-md/project.md`
- `core/agents-md.md`
- `core/commands/global/{manage-context,review-changes,setup-standards}.md`
- `core/commands/project/{new-ticket,finish-ticket,run-tests,review-pr,compact-context,update-context}.md`
- `core/agents/{validator-reviewer,pipeline-debugger}.md`
- `core/context-templates/{MEMORY,architecture,api-endpoints,data-models,services-layer}.md`
- `core/adr/{README,template}.md`
- `core/settings.json`

**Fuentes de extracción (verificadas):**
- Estándares → ssacar de sus secciones en `C:\Users\patriciods\.claude\CLAUDE.md` (secciones "Estándares de Ingeniería", "Anti-Alucinación", "Multi-Agente", "Manejo de Contexto y Tokens", "Git", "Seguridad", "Testing"). Generalizar: reemplazar comandos concretos por `${test_cmd}`/`${lint_cmd}`, y las rutas Python/FastAPI por `${structure}`/`${language}`.
- Commands `project` → copiar de `C:\Users\patriciods\lambda-scanner\UDLA_backend_ssh\.claude\commands\*.md`, reemplazando `AB#`/`main`/`pytest` por `${ticket_format}`, `${branch_pattern}`, `${test_cmd}`, `${lint_cmd}`.
- Commands `global` → copiar de `C:\Users\patriciods\.claude\commands\{manage-context,review-changes,setup-standards}.md` (ya neutrales; dejar tal cual salvo referencias a stack).
- `adr/README.md` y `adr/template.md` → el contenido canónico ya está en `setup-standards.md` (sección "Contenido canónico"); usar ese, con `Ámbito: <módulo/servicio> | proyecto`.
- `agents/*` → de `UDLA_backend_ssh\.claude\agents\{validator-reviewer,pipeline-debugger}.md`, quitando lo específico de UDLA.
- `context-templates/*` → de `UDLA_backend_ssh\.claude\context\*.md`, vaciados a esqueletos con secciones y `${...}`.
- `claude-md/project.md` → basado en el encabezado del `UDLA_backend_ssh\CLAUDE.md` ("Complementa las instrucciones globales de ~/.claude/CLAUDE.md"), parametrizado con `${stack}`, `${language}`, `${maturity_warning}`, lista de context files, `${precommit_steps}`.
- `settings.json` → un `UDLA_backend_ssh\.claude\settings.json` despojado de permisos específicos (base mínima).

**Regla de verificación:** cada archivo de `core/` incluye al final un comentario HTML `<!-- origen: <ruta real> -->`.

- [ ] **Step 1: Escribir el test de completitud — `tests/test_core_content.py`**

```python
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
```

- [ ] **Step 2: Correr para ver que falla**

Run: `python -m pytest tests/test_core_content.py -v`
Expected: FAIL (faltan archivos).

- [ ] **Step 3: Crear los archivos de `core/`** siguiendo las fuentes de extracción de arriba. Leer cada fuente real con `Read`, generalizar reemplazando lo específico por las variables del contrato, y escribir en `core/`. Ejemplo de `core/claude-md/project.md`:

```markdown
# CLAUDE.md — proyecto ${stack}

Instrucciones específicas de este proyecto. **Complementa** las instrucciones
globales de `~/.claude/CLAUDE.md` (no las repite).

${maturity_warning}
## Contexto

- Stack: **${stack}** (${language})
- Entorno: **${profile}** — CI `${ci}`, nube `${cloud}`, host git `${git_host}`
- Tickets: `${ticket_format}` — ramas `${branch_pattern}`

## Al iniciar cada sesión

Leer `.claude/context/MEMORY.md` (memoria portable del proyecto).

## Protocolo pre-commit

${precommit_steps}

<!-- origen: UDLA_backend_ssh/CLAUDE.md (generalizado) -->
```

Ejemplo de `core/commands/project/run-tests.md`:

```markdown
---
description: Corre la suite de tests y el lint del proyecto
---

Ejecuta en orden y reporta resultados:

1. Tests: `${test_cmd}`
2. Lint: `${lint_cmd}`

Si alguno falla, muestra el error y NO continúes.

<!-- origen: UDLA_backend_ssh/.claude/commands/run-tests.md (generalizado) -->
```

(El resto de archivos se crean análogamente desde sus fuentes.)

- [ ] **Step 4: Verificar que no hay placeholders huérfanos**

Escribir y correr un chequeo rápido: renderizar cada archivo de `core/` con un contexto demo completo no debe lanzar `UnresolvedPlaceholderError`. Añadir a `tests/test_core_content.py`:

```python
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
```

- [ ] **Step 5: Correr los tests de core**

Run: `python -m pytest tests/test_core_content.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add core tests/test_core_content.py
git commit -m "feat(core): contenido neutral extraído y generalizado de las configs reales

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 9: Presets reales y profiles

**Files:**
- Create: `presets/python-fastapi/preset.toml` (+ `skills/` copiadas de `UDLA_backend_ssh/.claude/skills/`)
- Create: `presets/react-vite/preset.toml` (+ `skills/` si aplica de `UDLA_front`)
- Create: `profiles/personal.toml`, `profiles/work.toml`
- Test: `tests/test_golden.py` (parte real)

**Interfaces:**
- Consumes: motor completo.
- Produces: instalaciones reales verificables.

- [ ] **Step 1: Crear `profiles/personal.toml` y `profiles/work.toml`**

```toml
# profiles/personal.toml
profile = "personal"
agents = ["claude"]
git_host = "github"
ci = "github-actions"
cloud = "aws"
ticket_format = "#<número>"
branch_pattern = "feature/<n>-descripcion"
```
```toml
# profiles/work.toml
profile = "work"
agents = ["claude"]
git_host = "github"
ci = "azure-pipelines"
cloud = "azure"
ticket_format = "AB#<número>"
branch_pattern = "feature/AB#<n>-descripcion"
```

- [ ] **Step 2: Crear `presets/python-fastapi/preset.toml`**

```toml
stack = "python-fastapi"
language = "Python 3.12+"
maturity = "real"
skills = ["async-python-patterns", "fastapi-templates", "python-testing-patterns",
          "python-design-patterns", "sql-optimization-patterns"]
precommit = ["test", "lint"]
structure = """
app/
├── core/        # config, security, exceptions
├── api/         # routers/endpoints
├── services/    # lógica de negocio
├── models/      # dominio
├── schemas/     # Pydantic DTOs
└── db/          # repositories
tests/
"""

[commands]
test = "pytest tests/ -q"
lint = "ruff check app/"
typecheck = "mypy app/"
build = ""
```

Copiar las carpetas de skill listadas desde `C:\Users\patriciods\lambda-scanner\UDLA_backend_ssh\.claude\skills\<skill>\` a `presets/python-fastapi/skills/<skill>\`.

- [ ] **Step 3: Crear `presets/react-vite/preset.toml`**

```toml
stack = "react-vite"
language = "TypeScript + React (Vite)"
maturity = "real"
skills = []
precommit = ["lint", "build"]
structure = """
src/
├── components/
├── pages/
├── services/
└── hooks/
"""

[commands]
test = "npm test"
lint = "npx eslint src/"
typecheck = "tsc --noEmit"
build = "npm run build"
```

- [ ] **Step 4: Escribir el golden test real — `tests/test_golden.py`**

```python
from pathlib import Path

from framework.cli import main

ROOT = Path(__file__).parent.parent  # raíz real del framework


def _install(tmp_path, stack, profile, addons=""):
    args = ["--scope", "project", "--stack", stack, "--profile", profile,
            "--target", str(tmp_path), "--root", str(ROOT)]
    if addons:
        args += ["--addons", addons]
    return main(args)


def test_python_fastapi_work_installs_clean(tmp_path):
    assert _install(tmp_path, "python-fastapi", "work") == 0
    claude_md = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "AB#" in claude_md  # profile work
    assert "python-fastapi" in claude_md
    assert (tmp_path / ".claude" / "skills" / "fastapi-templates").exists()
    # ningún archivo generado conserva placeholders
    for md in (tmp_path).rglob("*.md"):
        assert "${" not in md.read_text(encoding="utf-8")


def test_react_vite_personal_installs_clean(tmp_path):
    assert _install(tmp_path, "react-vite", "personal") == 0
    assert "#<número>" in (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
```

- [ ] **Step 5: Correr los tests golden reales**

Run: `python -m pytest tests/test_golden.py -v`
Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add presets/python-fastapi presets/react-vite profiles tests/test_golden.py
git commit -m "feat(presets): presets reales python-fastapi y react-vite + profiles

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 10: Presets plantilla-base (`java-springboot`, `dotnet`, `aws-lambda`)

**Files:**
- Create: `presets/java-springboot/preset.toml`
- Create: `presets/dotnet/preset.toml`
- Create: `presets/aws-lambda/preset.toml`
- Test: ampliar `tests/test_golden.py`

**Interfaces:**
- Produces: 3 presets con `maturity = "plantilla-base"`.

- [ ] **Step 1: Crear `presets/java-springboot/preset.toml`**

```toml
stack = "java-springboot"
language = "Java 21 + Spring Boot"
maturity = "plantilla-base"
skills = []
precommit = ["test", "build"]
structure = """
src/main/java/...   # controllers, services, repositories
src/test/java/...
# NOTA: en trabajo se usa el framework interno 'nano' (sobre Spring Boot, para BFF).
# Ajustar convenciones de 'nano' al endurecer este preset.
"""

[commands]
test = "mvn test"
lint = "mvn spotless:check"
typecheck = ""
build = "mvn -q package"
```

- [ ] **Step 2: Crear `presets/dotnet/preset.toml`**

```toml
stack = "dotnet"
language = "C# / .NET 8"
maturity = "plantilla-base"
skills = []
precommit = ["test", "build"]
structure = """
src/        # proyectos .csproj
tests/
"""

[commands]
test = "dotnet test"
lint = "dotnet format --verify-no-changes"
typecheck = ""
build = "dotnet build -c Release"
```

- [ ] **Step 3: Crear `presets/aws-lambda/preset.toml`**

```toml
stack = "aws-lambda"
language = "Python 3.12 (AWS Lambda)"
maturity = "plantilla-base"
skills = ["async-python-patterns"]
precommit = ["test", "lint"]
structure = """
lambda_function.py
tests/
"""

[commands]
test = "pytest tests/ -q"
lint = "ruff check ."
typecheck = "mypy ."
build = ""
```

- [ ] **Step 4: Ampliar `tests/test_golden.py` con aviso de plantilla-base**

```python
def test_springboot_is_plantilla_base_warns(tmp_path, capsys):
    from framework.cli import main
    from pathlib import Path
    code = main(["--scope", "project", "--stack", "java-springboot", "--profile", "work",
                 "--target", str(tmp_path), "--root", str(Path(__file__).parent.parent)])
    out = capsys.readouterr().out
    assert code == 0
    assert "plantilla-base" in out
    assert "sin probar" in (tmp_path / "CLAUDE.md").read_text(encoding="utf-8").lower()
```

- [ ] **Step 5: Correr**

Run: `python -m pytest tests/test_golden.py -v`
Expected: 3 passed.

- [ ] **Step 6: Commit**

```bash
git add presets/java-springboot presets/dotnet presets/aws-lambda tests/test_golden.py
git commit -m "feat(presets): plantillas base java-springboot (nano), dotnet y aws-lambda

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 11: Addons `docker` y `k8s`

**Files:**
- Create: `addons/docker/addon.toml` (+ `skills/docker-patterns/SKILL.md`)
- Create: `addons/k8s/addon.toml` (+ `skills/k8s-patterns/SKILL.md`)
- Test: ampliar `tests/test_golden.py`

**Interfaces:**
- Consumes: soporte de addons ya presente en `generate()` (Task 6) y `cli` (Task 7).
- Produces: superposición de skills de contenedores sobre cualquier stack.

- [ ] **Step 1: Crear `addons/docker/addon.toml` y su skill**

```toml
# addons/docker/addon.toml
addon = "docker"
skills = ["docker-patterns"]
```
`addons/docker/skills/docker-patterns/SKILL.md`:
```markdown
---
name: docker-patterns
description: Patrones de contenedorización para ${stack}
---

# Docker para ${stack}

- Multi-stage builds; imagen final mínima.
- `.dockerignore` para no filtrar `.claude/`, `node_modules/`, `.venv/`.
- Healthcheck y usuario no-root.
```

- [ ] **Step 2: Crear `addons/k8s/addon.toml` y su skill**

```toml
# addons/k8s/addon.toml
addon = "k8s"
skills = ["k8s-patterns"]
```
`addons/k8s/skills/k8s-patterns/SKILL.md`:
```markdown
---
name: k8s-patterns
description: Patrones de despliegue en Kubernetes para ${stack}
---

# Kubernetes para ${stack}

- Deployment + Service + probes (readiness/liveness).
- Requests/limits de recursos; ConfigMap/Secret para configuración.
```

- [ ] **Step 3: Ampliar `tests/test_golden.py` con addons**

```python
def test_addons_overlay_skills(tmp_path):
    from framework.cli import main
    from pathlib import Path
    code = main(["--scope", "project", "--stack", "java-springboot", "--profile", "work",
                 "--addons", "docker,k8s", "--target", str(tmp_path),
                 "--root", str(Path(__file__).parent.parent)])
    assert code == 0
    assert (tmp_path / ".claude" / "skills" / "docker-patterns" / "SKILL.md").exists()
    assert (tmp_path / ".claude" / "skills" / "k8s-patterns" / "SKILL.md").exists()
```

- [ ] **Step 4: Correr**

Run: `python -m pytest tests/test_golden.py::test_addons_overlay_skills -v`
Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add addons tests/test_golden.py
git commit -m "feat(addons): docker y k8s como capas ortogonales de skills

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 12: Suite de idempotencia y matriz completa

**Files:**
- Create: `tests/test_idempotency.py`

**Interfaces:**
- Consumes: `framework.cli.main`.

- [ ] **Step 1: Escribir `tests/test_idempotency.py`**

```python
from pathlib import Path

import pytest

from framework.cli import main

ROOT = Path(__file__).parent.parent
STACKS = ["python-fastapi", "react-vite", "java-springboot", "dotnet", "aws-lambda"]
PROFILES = ["personal", "work"]


@pytest.mark.parametrize("stack", STACKS)
@pytest.mark.parametrize("profile", PROFILES)
def test_matrix_installs_without_leftover_placeholders(tmp_path, stack, profile):
    code = main(["--scope", "project", "--stack", stack, "--profile", profile,
                 "--target", str(tmp_path), "--root", str(ROOT)])
    assert code == 0
    for f in tmp_path.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".json"}:
            assert "${" not in f.read_text(encoding="utf-8"), f


def test_second_run_creates_nothing(tmp_path, capsys):
    args = ["--scope", "project", "--stack", "python-fastapi", "--profile", "work",
            "--target", str(tmp_path), "--root", str(ROOT)]
    main(args)
    capsys.readouterr()
    main(args)
    out = capsys.readouterr().out
    assert "Creados (0)" in out


def test_global_scope_matrix(tmp_path):
    for profile in PROFILES:
        code = main(["--scope", "global", "--profile", profile,
                     "--home", str(tmp_path / profile), "--root", str(ROOT)])
        assert code == 0
        assert (tmp_path / profile / ".claude" / "CLAUDE.md").exists()
```

- [ ] **Step 2: Correr toda la suite**

Run: `python -m pytest -q && python -m ruff check .`
Expected: todo verde (incluye la matriz 5×2 + idempotencia + global), ruff limpio.

- [ ] **Step 3: Commit**

```bash
git add tests/test_idempotency.py
git commit -m "test: matriz completa scope×stack×profile e idempotencia

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 13: README, ADRs propios y push a GitHub

**Files:**
- Create: `README.md`
- Create: `docs/adr/README.md`, `docs/adr/template.md`, `docs/adr/0001-nucleo-neutral-generadores.md`, `docs/adr/0002-tres-ejes-scope-stack-profile.md`, `docs/adr/0003-cero-dependencias-toml.md`

- [ ] **Step 1: Escribir `README.md`**

Contenido: qué es, requisitos (Python 3.11+), los 3 ejes + addons, tabla de comandos de uso (copiada de la sección "El instalador" del spec), y una nota de que los presets `plantilla-base` no están probados en proyecto real.

- [ ] **Step 2: Crear `docs/adr/` propio del framework**

Copiar `core/adr/README.md` y `core/adr/template.md` a `docs/adr/` (con `Ámbito: proyecto`), y escribir los 3 ADRs listados registrando las decisiones 2, (3+5), y (4) del spec.

- [ ] **Step 3: Verificación final**

Run: `python -m pytest -q && python -m ruff check .`
Expected: todo verde.

Además, prueba manual de humo (scope global sobre carpeta temporal, sin tocar el `~/.claude` real):
Run: `python install.py --scope global --profile personal --home .\_tmp_home`
Expected: crea `_tmp_home\.claude\CLAUDE.md` y commands globales; borrar `_tmp_home` después.

- [ ] **Step 4: Commit y push**

```bash
git add README.md docs/adr
git commit -m "docs: README y ADRs propios del framework

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

Luego (requiere confirmación del usuario y que exista el repo remoto en su GitHub personal):
```bash
gh repo create agent-framework --private --source=. --remote=origin --push
```

---

## Self-Review (cobertura del spec)

- **3 ejes + addons** → Tasks 4 (context), 6 (generator scopes), 7 (cli flags), 11 (addons). ✅
- **scope global/project** → Task 6 (ambas ramas) + Task 12 (matriz global). ✅
- **Núcleo neutral, fuente única** → Task 8. ✅
- **Presets reales vs plantilla-base + aviso** → Tasks 9, 10 (+ test de aviso). ✅
- **profile GitHub host ambos, work=Azure Pipelines/AB#** → Task 9 (`profiles/*.toml`) + assert `AB#` en Task 9. ✅
- **nano en java** → Task 10 (nota en structure). ✅
- **Cero dependencias / TOML / Python 3.11+** → Global Constraints + Task 1 (`pyproject`) + Task 3 (`tomllib`). ✅
- **Idempotencia + falla ante placeholder** → Tasks 5, 12 + `render` (Task 2). ✅
- **Testing golden-master + idempotencia + smoke equivalencia** → Tasks 9, 12 (smoke: assert skills de UDLA presentes y `AB#`). ✅
- **Manejo de errores (stack/addon inexistente)** → Task 7 (tests de retorno 2). ✅
- **Dogfooding docs/adr propio** → Task 13. ✅
