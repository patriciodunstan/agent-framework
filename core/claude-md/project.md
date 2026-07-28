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

## Archivos de Contexto

Disponibles en `.claude/context/` — leer según el módulo en que se trabaje:

- `.claude/context/MEMORY.md` — **Memoria del proyecto** (leer siempre al inicio)
- `.claude/context/architecture.md` — Stack, estructura, patrones arquitectónicos
- `.claude/context/api-endpoints.md` — Endpoints REST del proyecto
- `.claude/context/data-models.md` — Modelos de datos y tipos
- `.claude/context/services-layer.md` — Servicios y lógica de negocio

## Protocolo pre-commit

${precommit_steps}

Si alguno falla → **NO commitear**. Primero arreglar, luego volver a correr, luego commitear.

## Slash Commands

| Comando | Descripción |
|---------|-------------|
| `/new-ticket` | Crea rama desde la base actualizada |
| `/finish-ticket` | Actualiza `.claude/context/`, commit, push, PR |
| `/review-pr` | Revisa código antes de commitear |
| `/run-tests` | Ejecuta tests con cobertura |
| `/update-context` | Actualiza `.claude/context/` sin commit |
| `/compact-context` | Guarda sesión y prepara para `/compact` |

<!-- origen: UDLA_backend_ssh/CLAUDE.md (generalizado) -->
