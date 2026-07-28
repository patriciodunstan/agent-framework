---
description: "Revisa los cambios actuales contra las decisiones vigentes (docs/adr/), el CLAUDE.md del proyecto y buenas prácticas. Funciona en cualquier proyecto."
argument-hint: "[all|code|tests|security]"
allowed-tools: ["Bash", "Glob", "Grep", "Read"]
---

# Revisión de cambios contra los estándares

Revisa los cambios actuales antes de commit/push. **Aspectos:** "$ARGUMENTS"

## Contexto

- Archivos modificados: !`git diff --name-only HEAD`
- Diff completo: !`git diff HEAD`
- Rama actual: !`git branch --show-current`
- Decisiones vigentes (ADR): !`cat docs/adr/README.md docs/adr/[0-9]*.md 2>/dev/null || echo "(sin docs/adr — corre /setup-standards para crearlo)"`
- Convenciones del proyecto: @CLAUDE.md

## Flujo de revisión

### 1. Decisiones de arquitectura vigentes (ADR) — PRIMERO

Los ADR de `docs/adr/` (cargados arriba) son la **fuente de verdad viva**. Verifica
que el diff respete cada decisión con estado `aceptada`; cada ADR indica en
"Consecuencias" qué marcar como violación. **Los ADR mandan sobre cualquier otra
regla.** Si el diff introduce una decisión de arquitectura/práctica nueva que no
está en ningún ADR, señálalo para escribir uno (copiar `docs/adr/template.md`).

### 2. Protocolo de verificación

Cada hallazgo lleva evidencia (regla citada, resultado real de test, lo observado).
Lo que no se pueda comprobar se declara `no verificado: <razón>`. No adivinar.

### 3. Convenciones del proyecto (CLAUDE.md)

Verifica cumplimiento de lo que declare el `CLAUDE.md` del proyecto (cargado arriba):
convenciones de nombres, capas, manejo de errores, secrets, no commits a main, etc.

### 4. Calidad general

- Correctitud y casos borde; manejo de errores explícito
- Tests para la lógica nueva (y que prueben el flujo real, no solo unidades aisladas)
- Sin secrets ni credenciales hardcodeadas
- Sin `.claude/` u otra config local trackeada (debe estar en `.gitignore`)

### 5. Resumen final

```
## Problemas Críticos (bloquean el PR)
- ...

## Problemas Importantes (deben corregirse)
- ...

## Sugerencias (opcional)
- ...

## OK — Listo para commit
- ...
```

Si no hay críticos, indicar que está listo para commit por el flujo del proyecto.

<!-- origen: ~/.claude/commands/review-changes.md -->
