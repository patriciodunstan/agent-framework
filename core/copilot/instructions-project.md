# Instrucciones del proyecto — ${stack}

Proyecto **${stack}** (${language}). Entorno **${profile}**: CI `${ci}`, nube `${cloud}`,
host git `${git_host}`. Tickets `${ticket_format}`, ramas `${branch_pattern}`.

Complementá estas instrucciones con `AGENTS.md` (en la raíz del repo) y con mis
estándares globales de Copilot (`~/.copilot/copilot-instructions.md`).

${maturity_warning}
## Estructura

${structure}

## Reglas clave

- Antes de push: ejecutá los tests (`${test_cmd}`) y el lint (`${lint_cmd}`). Si algo
  falla, no commitees — arreglá primero.
- Nunca hagas commits directos a `main`; cada cambio va en su rama con PR.
- No commitear secrets, `.env` ni credenciales.
- Nombres y convenciones según el stack (${language}).

## Prompts disponibles

Invocá con `/` en Copilot Chat: `/new-ticket`, `/run-tests`, `/review-pr`,
`/finish-ticket`, `/update-context`, `/compact-context`.

<!-- generado por agent-framework (scope project, agente copilot) — fuente: UDLA_backend_ssh/CLAUDE.md (generalizado) -->
