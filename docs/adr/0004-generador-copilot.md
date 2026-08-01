# ADR-0004: Generador GitHub Copilot vía `--agent`, reutilizando `core/`

- **Estado**: aceptada
- **Fecha**: 2026-08-01
- **Ámbito**: proyecto

## Contexto

El framework nació con un solo generador (Claude Code). El entorno de trabajo del usuario
usa **GitHub Copilot** (VS Code Copilot Chat, modelo Sonnet 4.6). El diseño original
(ADR-0001) ya previó "generadores por agente" sobre una fuente neutral única, por lo que
agregar Copilot es una extensión, no un rediseño.

Formatos verificados en la documentación oficial (agosto 2026): Copilot lee
`.github/copilot-instructions.md` y `AGENTS.md` a nivel repo, `~/.copilot/copilot-instructions.md`
a nivel global (Copilot CLI), y `.github/prompts/*.prompt.md` como prompts invocables con `/`.

## Decisión

Se agrega un segundo generador (`framework/generators/copilot.py`) seleccionable con el
flag `--agent {claude,copilot}` (default `claude`, retrocompatible). Reutiliza la fuente
neutral (`core/standards`, `core/agents-md.md`) y añade templates con forma Copilot en
`core/copilot/`. Los helpers compartidos viven en `framework/generators/common.py` (DRY).
Alcance v2: instructions + `AGENTS.md` + prompts. Fuera de v2: path-specific
`*.instructions.md` con `applyTo`, chat modes, y campos `tools`/`model` en prompts.

## Consecuencias

- **Permitido/esperado**: cualquier nuevo agente se agrega como un generador más en el
  registro del CLI (`GENERATORS`), consumiendo `core/`; no se duplica conocimiento.
- **Regla**: para el agente `copilot`, los archivos generados (`.github/`, `AGENTS.md`)
  **se commitean** (viajan con el repo); no se agregan a `.gitignore`. Solo `claude`
  ignora su `.claude/`. Un revisor debe marcar como violación gitignorear `.github/`.
- **Regla**: los templates de Copilot solo usan placeholders del contrato de contexto
  existente; introducir otro `${...}` rompe la generación (falla-duro de `render`).
