---
description: Revisión del PR antes de subirlo — calidad, tipos, manejo de errores y cumplimiento de las instrucciones
name: review-pr
argument-hint: "[code|types|errors|tests|all]"
---

# Revisión de PR — ${stack}

Revisá los cambios actuales (`git diff HEAD`, archivos modificados, rama actual) antes
de commit/push. Enfocate en el aspecto que te indique (code / types / errors / tests /
all); si no indico nada, revisá todo.

## 1. Reglas críticas (siempre)

- No queries directas en controladores/routers — usar servicios o repositorios.
- Todos los endpoints con schema de request y response.
- No commitear secrets, `.env` ni credenciales; no commits directos a `main`.
- Convenciones de naming según el stack (${language}); queries parametrizadas.

## 2. Calidad

- Tipos/anotaciones en las funciones; manejo de errores explícito con status correctos.
- Dependencias inyectadas, no hardcodeadas; tests para la lógica nueva.

## 3. Resumen

Agrupá en: **Críticos** (bloquean el PR), **Importantes** (deben corregirse),
**Sugerencias** (opcional). Si no hay críticos, indicá que está listo para `/finish-ticket`.

<!-- generado por agent-framework — fuente: core/commands/project/review-pr.md -->
