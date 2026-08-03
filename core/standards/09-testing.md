## Estándar 9: Testing

- TDD: test que falla → código mínimo que lo pasa → refactor.
- Cobertura mínima: services 80%, utils/helpers 90%, routers 70% (integración).
- Los tests unitarios aislados no bastan: la mayoría de los bugs viven en la
  integración (datos reales, servicios externos, pipelines). Priorizar flujos
  end-to-end sobre unidades mockeadas.
- Pre-commit: correr tests y lint del proyecto (comandos concretos en el
  `CLAUDE.md` del proyecto y en `/run-tests`). Si algo falla, no commitear:
  arreglar primero.
- Test que falla tras un cambio: **nunca desactivarlo**. Diagnosticar si rompió
  funcionalidad existente (fix del código), si el comportamiento cambió a
  propósito (actualizar el test) o si el test estaba mal escrito (corregirlo).

<!-- origen: ~/.claude/CLAUDE.md §Testing -->
