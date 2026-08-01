---
description: Estampa los estándares de ingeniería en el proyecto actual (docs/adr/ + memoria docs/context/). Idempotente — seguro en proyectos nuevos y existentes.
name: setup-standards
agent: 'agent'
---

# Setup de Estándares de Ingeniería

Aplicá el estándar reutilizable a ESTE proyecto. **Idempotente**: no pises lo que ya
existe; agregá solo lo que falta y reportá. Antes de crear o editar, mostrame el cambio.

## Pasos

1. **docs/adr/** — si falta, creá `docs/adr/README.md` (índice de decisiones) y
   `docs/adr/template.md`. El registro de ADR es la fuente de verdad contra la que
   `/review-changes` revisa el código. Si ya existe, no lo toques.
2. **docs/context/** — si falta, creá `docs/context/MEMORY.md` como memoria del proyecto
   (estado, reglas críticas, índice de contexto por módulo). Es lo que los prompts
   `/update-context` y `/compact-context` mantienen.
3. **Reportá**: qué creaste, qué ya estaba, y qué queda pendiente. **No commitees** — el
   proyecto tiene su propio flujo git.

## Contenido canónico

### `docs/adr/README.md`

Índice con la explicación del flujo (tomar decisión → escribir ADR desde `template.md`
con número correlativo → `/review-changes` la verifica) y una tabla de índice vacía.

### `docs/adr/template.md`

Secciones: título `ADR-NNNN`, **Estado** (aceptada | reemplazada por ADR-NNNN | obsoleta),
**Fecha**, **Ámbito**, **Contexto** (hechos, no opiniones), **Decisión** (accionable y
verificable), **Consecuencias** (qué se permite/prohíbe; qué marcar como violación).

<!-- generado por agent-framework (global, copilot) — fuente: core/commands/global/setup-standards.md -->
