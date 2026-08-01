---
description: Revisa los cambios actuales del repo contra las decisiones vigentes (docs/adr/), las instrucciones del proyecto y buenas prácticas. Funciona en cualquier proyecto.
name: review-changes
argument-hint: "[all|code|tests|security]"
agent: 'ask'
---

# Revisión de cambios contra los estándares

Revisá los cambios actuales antes de commit/push. Enfocá en lo que te indique
(all / code / tests / security); si no indico nada, revisá todo.

## 1. Decisiones de arquitectura (ADR) — PRIMERO

Leé `docs/adr/README.md` y los `docs/adr/NNNN-*.md` si existen. Son la **fuente de
verdad viva**. Verificá que el diff (`git diff HEAD`) respete cada decisión con estado
`aceptada`; cada ADR indica en "Consecuencias" qué marcar como violación. **Los ADR
mandan sobre cualquier otra regla.** Si el diff introduce una decisión nueva que no está
en ningún ADR, señalalo para escribir uno (`/setup-standards` crea el scaffold si falta).

## 2. Protocolo de verificación

Cada hallazgo lleva evidencia (regla citada, resultado real de test, lo observado). Lo
que no se pueda comprobar se declara `no verificado: <razón>`. No adivines.

## 3. Instrucciones del proyecto

Verificá cumplimiento de lo que declaren `.github/copilot-instructions.md` y `AGENTS.md`:
convenciones de nombres, capas, manejo de errores, secrets, no commits directos a `main`.

## 4. Calidad general

- Correctitud y casos borde; manejo de errores explícito.
- Tests para la lógica nueva (y que prueben el flujo real, no solo unidades aisladas).
- Sin secrets ni credenciales hardcodeadas.

## 5. Resumen final

Agrupá en **Críticos** (bloquean el PR), **Importantes** (deben corregirse) y
**Sugerencias** (opcional). Si no hay críticos, indicá que está listo para commit.

<!-- generado por agent-framework (global, copilot) — fuente: core/commands/global/review-changes.md -->
