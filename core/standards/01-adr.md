## Estándar 1: Registro de decisiones (ADR)

Fuente de verdad única de las decisiones (arquitectura, prácticas, convenciones):
`docs/adr/` del proyecto, versionado.

- Decisión tomada → escribir el ADR: copiar `docs/adr/template.md`, siguiente
  número, agregarlo al índice.
- Los ADR no se borran. Una decisión reemplazada pasa a `reemplazada por ADR-NNNN`.
- `/review-changes` lee `docs/adr/` y verifica que el diff las respete.

<!-- origen: ~/.claude/CLAUDE.md §Estándares de Ingeniería / 1. Registro de decisiones -->
