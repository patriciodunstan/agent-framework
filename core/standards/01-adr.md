## Estándar 1: Registro de decisiones (ADR)

Las decisiones de arquitectura, prácticas y convenciones se registran en
`docs/adr/` del proyecto (versionado, viaja con `git clone`) — es la **fuente de
verdad única**. Cuando se toma una decisión, se escribe un ADR (copiar
`docs/adr/template.md`, siguiente número, agregar al índice). El review
(`/review-changes`) lee `docs/adr/` y verifica que el diff las respete. Los ADR no
se borran; una decisión reemplazada pasa a estado `reemplazada por ADR-NNNN`.

<!-- origen: ~/.claude/CLAUDE.md §Estándares de Ingeniería / 1. Registro de decisiones -->
