# ADR-0001: Núcleo neutral + generadores por agente

- **Estado**: aceptada
- **Fecha**: 2026-07-28
- **Ámbito**: proyecto

## Contexto

El framework necesita soportar múltiples agentes de IA (Claude Code en v1, GitHub
Copilot en v2) que consumen la misma base de conocimiento: estándares de ingeniería,
commands, skills y context-templates. Duplicar el conocimiento para cada agente
produce drift inevitable y trabajo de mantenimiento duplicado.

Además, la fuente original (configuraciones maduras de `UDLA_backend_ssh`,
`UDLA_front` y el `CLAUDE.md` global) contiene referencias específicas a
Claude Code que no deberían contaminar el núcleo común.

## Decisión

Separar el conocimiento en dos capas:

1. **`core/`** — contiene el conocimiento neutral (estándares, commands, context-templates,
   agents) expresado con placeholders genéricos, sin referencia a ningún agente concreto.
   Es la única fuente de verdad del conocimiento reutilizable.

2. **`generators/<agente>/`** — cada generador toma `core + preset + profile` y emite
   la configuración específica para su agente objetivo. El generador Claude Code
   (`generators/claude/`) emite `.claude/`, `CLAUDE.md`, `AGENTS.md`. Un futuro
   generador Copilot emitiría `.github/copilot-instructions.md`.

En v1 solo existe `generators/claude/`. El generador Copilot queda fuera de alcance
(decisión 3 del spec: YAGNI v1).

## Consecuencias

- **Permitido**: agregar un nuevo generador en `generators/` sin tocar `core/`.
- **Prohibido**: meter conocimiento específico de un agente en `core/`; los archivos
  bajo `core/` deben ser agnósticos al agente de IA de destino.
- **Obligatorio**: todo nuevo estándar o template se agrega primero en `core/` y luego
  se referencia desde el generador correspondiente. Nunca al revés.
- **Violación a marcar en review**: imports o referencias directas a rutas de Claude
  Code (`.claude/`, `CLAUDE.md`) dentro de `core/`.
