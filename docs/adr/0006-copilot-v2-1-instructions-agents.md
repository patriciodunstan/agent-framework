# ADR-0006: Copilot v2.1 — path-specific instructions, custom agents y campo `agent` en prompts

- **Estado**: aceptada
- **Fecha**: 2026-08-01
- **Ámbito**: proyecto

## Contexto

El ADR-0004 dejó fuera de v2 tres capacidades de VS Code Copilot: instructions path-specific
(`applyTo`), chat modes y los campos `tools`/`model` en prompts. Al implementarlas se
verificaron los formatos reales en la documentación oficial (agosto 2026), con un cambio
relevante respecto de lo que asumía el ADR-0004:

- **Path-specific instructions**: `.github/instructions/*.instructions.md`, frontmatter
  `applyTo: '<glob>'` (varios globs separados por coma). Copilot las adjunta automáticamente
  cuando el archivo en contexto matchea el glob.
- **Prompts**: el campo de modo es **`agent`** (`ask`/`agent`/`plan`), no `mode`. Además
  `model`, `tools[]`, `description`, `name`, `argument-hint`.
- **Chat modes → custom agents**: `.chatmode.md` está **deprecado**; el formato vigente es
  `*.agent.md` en `.github/agents/`, frontmatter `description`, `tools`, `model`.

## Decisión

El generador Copilot (scope `project`) emite, además de lo de v2:

- `.github/instructions/conventions.instructions.md` con `applyTo: '${code_globs}'`. Se
  agrega el campo **`code_globs`** a cada preset (opcional, default `**`), expuesto por
  `build_context`.
- `.github/agents/*.agent.md` traducidos desde `core/agents/` a forma Copilot, autorados en
  `core/copilot/agents/` (mismo patrón que `core/copilot/prompts/`).
- Campo **`agent`** en los 6 prompts: `agent` para los agénticos, `ask` para la revisión
  read-only (`review-pr`).

**No se fijan `model` ni `tools`** (ni en prompts ni en agents). Verificado: los IDs de
modelo cambian, el modelo se elige en la UI de VS Code, y un tool inexistente se ignora.
Fijarlos acopla la salida a nombres volátiles de VS Code; el read-only de los agents lo
impone el cuerpo, no el frontmatter.

## Consecuencias

- **Permitido/esperado**: un archivo abierto de un stack recibe sus convenciones
  automáticamente vía `applyTo`; los custom agents quedan disponibles en el dropdown de Chat.
- **Regla**: `code_globs` es opcional en el preset; si falta, el generador usa `**` (aplica a
  todo) — nunca rompe.
- **Regla**: los templates Copilot solo usan placeholders del contrato de contexto vigente
  (ahora incluye `${code_globs}`); introducir otro `${...}` rompe la generación (falla-duro
  de `render`).
- **Alcance**: solo agente `copilot`. El generador `claude` no cambia.
- **Revisión futura**: si se decide pinear `model`, hacerlo como campo opcional del profile
  (no hardcodeado en los templates) para no acoplar a un ID concreto.
