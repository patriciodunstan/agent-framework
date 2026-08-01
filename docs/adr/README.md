# Decisiones de Arquitectura (ADR) — agent-framework

Registro de las decisiones de arquitectura, prácticas y convenciones del proyecto.
Es la **fuente de verdad única** contra la que se revisa el código: cuando tomamos
una decisión, se escribe un ADR aquí, y el review (`/review-changes`) las lee.

## Cómo funciona

1. **Tomamos una decisión** (arquitectura, práctica, convención de código).
2. **Se escribe un ADR** — copiar `template.md` a `NNNN-titulo-corto.md` con el
   siguiente número correlativo, y agregarlo al índice.
3. **El review la sigue** — `/review-changes` lee esta carpeta y verifica que el
   diff respete las decisiones vigentes.

Una decisión que reemplaza a otra: la nueva cita a la vieja, y la vieja pasa a
estado `reemplazada por ADR-NNNN`. No se borran los ADR — son registro histórico.

## Índice

| ADR | Título | Ámbito | Estado |
|-----|--------|--------|--------|
| [0001](0001-nucleo-neutral-generadores.md) | Núcleo neutral + generadores por agente | proyecto | aceptada |
| [0002](0002-tres-ejes-scope-stack-profile.md) | Modelo core + scope×stack×profile + addons | proyecto | aceptada |
| [0003](0003-cero-dependencias-toml.md) | Instalador Python cero-deps + TOML + Python 3.11+ | proyecto | aceptada |
| [0004](0004-generador-copilot.md) | Generador GitHub Copilot vía `--agent`, reutilizando `core/` | proyecto | aceptada |
| [0005](0005-hooks-de-contexto.md) | Automatizar manejo de contexto vía hooks de Claude Code | proyecto | aceptada |
| [0006](0006-copilot-v2-1-instructions-agents.md) | Copilot v2.1 — path-specific instructions, custom agents y campo `agent` | proyecto | aceptada |

<!-- origen: core/adr/README.md (adaptado, Ámbito: proyecto) -->
