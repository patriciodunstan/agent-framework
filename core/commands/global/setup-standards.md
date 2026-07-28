---
description: "Estampa los estándares de ingeniería en el proyecto actual (docs/adr/ + .gitignore .claude/). Idempotente: seguro en proyectos nuevos y existentes."
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob"]
---

# Setup de Estándares de Ingeniería

Aplica el estándar reutilizable a ESTE proyecto. **Idempotente**: no pises lo que
ya existe; agrega solo lo que falta y reporta. Antes de crear o editar, muestra el
cambio y confirma (según el CLAUDE.md global).

## Contexto del proyecto

- Raíz: !`git rev-parse --show-toplevel 2>/dev/null || pwd`
- ¿docs/adr existe?: !`ls docs/adr 2>/dev/null && echo EXISTE || echo FALTA`
- ¿.gitignore ignora .claude?: !`git check-ignore .claude 2>/dev/null && echo SI || echo NO`
- ¿.claude trackeado?: !`git ls-files .claude 2>/dev/null | head -1`

## Pasos

1. **docs/adr/** — si FALTA, crear `docs/adr/README.md` y `docs/adr/template.md`
   con el contenido canónico de abajo. Si ya existe, no tocar.
2. **.gitignore** — si `.claude/` no está ignorado, agregar la línea `.claude/`.
   Si `.claude/` aparece trackeado, correr `git rm -r --cached .claude` (NO borra
   los archivos locales) y avisar que el des-trackeo queda staged para el flujo git.
3. **Reportar**: qué se creó, qué ya estaba, y qué queda pendiente de commitear.

No commitear nada — el proyecto tiene su propio flujo git.

## Contenido canónico

### `docs/adr/README.md`

```markdown
# Decisiones de Arquitectura (ADR)

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
| — | (aún no hay decisiones registradas) | — | — |
```

### `docs/adr/template.md`

```markdown
# ADR-NNNN: <título corto de la decisión>

- **Estado**: aceptada | reemplazada por ADR-NNNN | obsoleta
- **Fecha**: YYYY-MM-DD
- **Ámbito**: <módulo/servicio> | proyecto

## Contexto

Qué problema o situación motivó la decisión. Hechos, no opiniones.

## Decisión

Qué decidimos, en una o dos frases claras y accionables (lo que el review debe
poder verificar).

## Consecuencias

Qué implica: qué se permite, qué se prohíbe, qué hay que hacer distinto. Incluir
lo que un revisor debe marcar como violación.
```

<!-- origen: ~/.claude/commands/setup-standards.md -->
