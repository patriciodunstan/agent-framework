# ADR-0007: Paridad Copilot↔Claude — skills, memoria de contexto y scaffold ADR

- **Estado**: aceptada
- **Fecha**: 2026-08-01
- **Ámbito**: proyecto

## Contexto

Una revisión de paridad (generando ambos agentes para el mismo stack/profile y comparando
los árboles) mostró que el generador Copilot emitía menos que el de Claude en tres frentes:
no emitía skills de stack, no emitía la memoria de contexto por módulo, y no emitía el
scaffold de ADR. Además, los prompts de Copilot ya referenciaban una "documentación de
contexto (`docs/`)" que no existía (referencia colgante).

Hallazgo verificado en la doc oficial de VS Code Copilot: **Agent Skills es un estándar
abierto**; Copilot lee `.github/skills/`, `.claude/skills/` y `.agents/skills/` con el mismo
`SKILL.md` (frontmatter `name`+`description`). Los skills del framework son reutilizables
verbatim, sin traducción.

## Decisión

El generador Copilot (scope `project`) alcanza paridad con Claude reutilizando la fuente
neutral existente:

- **Skills**: emite los skills de preset y addon a `.github/skills/<skill>/…` con el mismo
  `SKILL.md`. Se extrae el helper `skill_dirs(base, skills, context, dest_prefix)` a
  `common.py` (DRY, compartido con el generador Claude).
- **Memoria de contexto**: emite `docs/context/` con `MEMORY.md` en forma Copilot
  (`core/copilot/context/MEMORY.md`, apunta a `.github/…` y `docs/adr/`) y el resto de los
  templates neutrales de `core/context-templates/`. Las instrucciones y los prompts
  `update/compact/finish` referencian ahora `docs/context/` (antes: `docs/` genérico).
- **ADR**: emite `docs/adr/README.md` + `template.md` (mismos templates neutrales que Claude).

Contrapartida por diseño (no son gaps): los **hooks** de contexto no aplican a Copilot (no
tiene mecanismo equivalente); el resumen semántico sigue siendo model-driven vía
`/compact-context`.

## Consecuencias

- **Permitido/esperado**: un proyecto Copilot arranca con la misma base que uno Claude —
  skills de dominio, memoria por módulo y registro de decisiones.
- **Regla**: `skill_dirs` es la única vía para emitir skills en ambos generadores; el destino
  (`.claude/skills` vs `.github/skills`) es el único parámetro que cambia.
- **Regla**: la memoria de contexto de Copilot vive en `docs/context/` (se commitea, como
  todo lo de Copilot); la de Claude en `.claude/context/` (gitignored). No se mezclan.
- **Alcance**: solo cambia el generador `copilot` (y el refactor DRY en `common.py`/`claude.py`
  sin cambio de salida para Claude, cubierto por los golden existentes).
