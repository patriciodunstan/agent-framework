# CLAUDE.md — proyecto ${stack}

Instrucciones específicas de este proyecto. **Complementa** las instrucciones
globales de `~/.claude/CLAUDE.md` (no las repite).

${maturity_warning}
## Contexto

- Stack: **${stack}** (${language})
- Entorno: **${profile}** — CI `${ci}`, nube `${cloud}`, host git `${git_host}`
- Tickets: `${ticket_format}` — ramas `${branch_pattern}`

La memoria del proyecto se inyecta sola al iniciar sesión: `.claude/context/MEMORY.md`
completo, y el resto de `.claude/context/` como índice para leer bajo demanda.

## Protocolo pre-commit

${precommit_steps}

Si alguno falla → **NO commitear**. Primero arreglar, luego volver a correr, luego commitear.

## Slash commands

`/new-ticket` rama desde la base actualizada · `/finish-ticket` contexto + commit +
push + PR · `/review-pr` revisar antes de commitear · `/run-tests` tests con
cobertura · `/update-context` actualiza `.claude/context/` · `/compact-context`
guarda la sesión y prepara `/compact`

<!-- origen: UDLA_backend_ssh/CLAUDE.md (generalizado) -->
