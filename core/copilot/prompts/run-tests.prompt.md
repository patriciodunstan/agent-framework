---
description: Ejecuta la suite de tests y el lint del proyecto y reporta resultados
name: run-tests
---

Ejecutá la verificación del proyecto y reportá.

1. Tests (con cobertura si aplica): `${test_cmd}`
2. Lint: `${lint_cmd}`
3. Reportame: total pasados / fallados / saltados, cobertura por módulo
   (target: services ≥80%, utils ≥90%), y los tests fallados con su error completo.
4. Si hay tests fallando: analizá la causa y sugerí la corrección, pero no la apliques
   sin consultarme primero.
5. Si la cobertura es baja: indicá qué módulos necesitan más tests.

<!-- generado por agent-framework — fuente: core/commands/project/run-tests.md -->
