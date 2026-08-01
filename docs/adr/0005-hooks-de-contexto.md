# ADR-0005: Automatizar el manejo de contexto vía hooks de Claude Code

- **Estado**: aceptada
- **Fecha**: 2026-08-01
- **Ámbito**: proyecto

## Contexto

El manejo de contexto (guardar antes de compactar, recargar al iniciar) era manual vía los
comandos `/manage-context`, `/compact-context` y `/update-context`. Tras una compactación,
los archivos `.claude/context/*.md` (memoria persistente del proyecto) no se reinyectan
solos, así que la sesión arranca sin esa memoria hasta que alguien la referencia a mano.

Formatos verificados en la documentación oficial (agosto 2026,
`code.claude.com/docs/en/hooks`):

- **`SessionStart`** (matchers `startup|resume|clear|compact|fork`, tipo `command`): lo que
  el comando escribe a stdout se agrega al contexto. Patrón documentado explícitamente para
  "re-inject critical context after compaction".
- **`PreCompact`** (matchers `manual|auto`): recibe `transcript_path` y `compaction_trigger`
  por stdin; puede correr un `command` antes de compactar.
- **Límite verificado**: un hook `command` no tiene acceso al modelo; `type: "prompt"` es
  "single-turn LLM evaluation" que **solo devuelve un sí/no** (no escribe archivos); y
  `type: "agent"` (multi-turn con tools) está marcado **experimental** ("prefer command
  hooks for production"). Por lo tanto el **resumen semántico** de una sesión NO se puede
  automatizar de forma confiable con hooks hoy.

## Decisión

El generador Claude estampa, en scope `project`, dos hooks tipo `command` (cero
dependencias, solo Python) en `.claude/settings.json`, más sus scripts en `.claude/hooks/`:

- **`load_context.py`** (`SessionStart`, `startup|resume|compact`): concatena
  `.claude/context/*.md` a stdout para reinyectarlos automáticamente. Reutiliza la memoria
  que `/update-context` y `/compact-context` ya mantienen — no duplica lógica.
- **`snapshot_transcript.py`** (`PreCompact`, `manual|auto`): copia el `transcript_path` a
  `.claude/snapshots/` para no perder nunca la sesión cruda, y recuerda por stderr correr
  `/compact-context`. No resume.

El **resumen semántico** sigue siendo model-driven a demanda (`/compact-context`),
porque los tipos de hook capaces de hacerlo son inadecuados (ver Contexto).

## Consecuencias

- **Permitido/esperado**: la recarga de contexto tras compactar es automática y sin costo de
  tokens; la sesión cruda queda respaldada en cada compactación.
- **Regla**: los scripts de hook se emiten **verbatim** (no pasan por `render`), porque son
  código y podrían contener `{}`/`%` que no son placeholders del framework.
- **Regla**: `.claude/` (incluidos `hooks/` y `snapshots/`) sigue gitignoreado por el
  estándar #2; los snapshots son locales, no viajan con el repo.
- **Alcance**: solo aplica al agente `claude`. Copilot no tiene un mecanismo de hooks
  equivalente, así que su generador no emite nada de esto.
- **Revisión futura**: si el hook `agent` deja de ser experimental, se puede reevaluar
  automatizar también el resumen semántico en `PreCompact`.
