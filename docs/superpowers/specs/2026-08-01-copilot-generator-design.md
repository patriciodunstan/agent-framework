# Diseño: generador GitHub Copilot (v2)

- **Fecha**: 2026-08-01
- **Estado**: aprobado — implementación en curso
- **Contexto de uso**: laptop de trabajo con VS Code + GitHub Copilot Chat (modelo Sonnet 4.6).

## Objetivo

Agregar un segundo generador (`copilot`) al framework, que consume la **misma fuente
`core/`** y emite configuración para GitHub Copilot, simétrico al generador Claude.

## Hechos verificados (docs oficiales, agosto 2026)

- **Global (Copilot CLI)**: `$HOME/.copilot/copilot-instructions.md` (+ `$HOME/.copilot/instructions/**/*.instructions.md`); reubicable con `COPILOT_HOME`.
- **Proyecto**: `.github/copilot-instructions.md` (leído en cada request), `.github/instructions/**/*.instructions.md` (path-specific con `applyTo`), `AGENTS.md` (Copilot CLI también lee `CLAUDE.md`).
- **Prompts (VS Code/VS/JetBrains)**: `.github/prompts/<n>.prompt.md`, frontmatter `description`/`name`/`argument-hint`/`agent`/`model`/`tools`; se invocan con `/n`.
- **Nivel usuario en VS Code**: perfil de VS Code (path OS-específico) vía `chat.instructionsFilesLocations` / `chat.promptFilesLocations`, sincronizable con Settings Sync — NO es un archivo portable fijo.
- Fuentes: docs.github.com (Copilot CLI custom instructions + config dir), code.visualstudio.com (prompt files + custom instructions).

## Decisión de alcance (aprobada)

Superficie: **`.github/copilot-instructions.md` + `AGENTS.md` + `.github/prompts/*.prompt.md`**.
Ambos scopes (**global + project**), simétrico al generador Claude.

**Fuera de v2 (YAGNI)**: path-specific `*.instructions.md` con `applyTo`, chat modes,
prompt files de nivel usuario, y los campos `tools`/`model`/`agent` en el frontmatter de prompts.

## Salida por scope

| scope | archivos emitidos |
|-------|-------------------|
| `global` | `.copilot/copilot-instructions.md` (header + `core/standards/*` concatenados), bajo `$HOME` o `--home` |
| `project` | `.github/copilot-instructions.md` (delgado + contexto del stack/profile), `AGENTS.md` (de `core/agents-md.md`), `.github/prompts/<n>.prompt.md` × 6 (los 6 commands) |

Para VS Code, el global se engancha apuntando `chat.instructionsFilesLocations` al archivo
`~/.copilot/copilot-instructions.md` (o Settings Sync). Se documenta en el README.

## Arquitectura

- **Selección de generador**: nuevo flag `--agent {claude,copilot}` en `install.py` (default `claude`, retrocompatible). Registro `{"claude": generate, "copilot": generate}` en el CLI.
- **DRY**: extraer helpers compartidos (`read_text`, `rendered`, `standards_body`) de `generators/claude.py` a `generators/common.py`; ambos generadores los usan.
- **`framework/generators/copilot.py`**: misma firma `generate(*, core_dir, presets_dir, addons_dir, preset, profile, addons, context, scope) -> list[OutputFile]`.
- **`core/copilot/`** (nuevo, forma Copilot, análogo a `core/claude-md/` y `core/commands/`):
  - `instructions-global-header.md` — cabecera del `.copilot/copilot-instructions.md` global.
  - `instructions-project.md` — el `.github/copilot-instructions.md` de proyecto (delgado + contexto).
  - `prompts/<6>.prompt.md` — los 6 commands como prompt files neutrales (frontmatter `description`/`name`, prosa; sin ejecución `!`bash propia de Claude que Copilot no soporta).
- **Reutiliza** `core/standards`, `core/agents-md.md` sin cambios.
- **`.gitignore`**: el paso `ensure_line('.claude/')` es específico de Claude; para Copilot no se ignora nada (los `.github/*` viajan con el repo).

## Manejo de errores

- Mismo motor idempotente + `render` (falla-duro ante `${...}` no resuelto).
- `--agent` inválido → error de argparse (choices). Combinaciones inválidas de scope/stack/target ya validadas.
- Solo se usan placeholders del contrato de contexto existente; prohibido introducir otros `${...}`.

## Testing

`tests/test_golden_copilot.py`:
- **project** (python-fastapi, work, `--agent copilot`): existen `.github/copilot-instructions.md`, `AGENTS.md`, `.github/prompts/new-ticket.prompt.md`; cada `.prompt.md` tiene frontmatter `description`; `AB#` aparece (profile work); `find_unresolved()==[]` en todos los archivos generados.
- **global** (personal, `--agent copilot`, `--home`): existe `.copilot/copilot-instructions.md`; `find_unresolved()==[]`; sin `AB#` (estándares neutrales).
- Reusa el patrón de `tests/test_golden.py`. La suite completa queda verde; ruff limpio.

## Criterios de éxito

1. `python install.py --scope project --stack python-fastapi --profile work --agent copilot --target <repo>` produce un `.github/` que VS Code Copilot Chat lee automáticamente, con los 6 prompts invocables por `/`.
2. `--agent copilot --scope global --home ~/.copilot-test` produce `copilot-instructions.md` con los estándares.
3. El generador Claude sigue intacto (default `--agent claude`), suite completa verde.
4. README documenta el uso Copilot y cómo enganchar VS Code al global.
