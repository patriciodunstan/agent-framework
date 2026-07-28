## Estándar 9: Testing

### Filosofía TDD (Test-Driven Development)

**Los tests PRIMERO, el código después.**

El ciclo TDD:
1. **Red**: Escribir un test que falla (porque la funcionalidad no existe)
2. **Green**: Implementar el código mínimo para pasar el test
3. **Refactor**: Mejorar el código manteniendo los tests verdes

### Estrategia de Testing

1. **Unit tests**: Lógica de negocio aislada (mock de dependencias externas)
2. **Integration tests**: APIs con DB real/mock
3. **E2E tests**: Flujos completos (selectivos, solo críticos)

Los tests unitarios aislados no bastan: la mayoría de los bugs viven en la
integración (datos reales, servicios externos, pipelines). Priorizar tests que
ejerciten el flujo completo end-to-end, no solo unidades mockeadas.

### Cobertura Mínima

- Services: 80%+
- Utils/Helpers: 90%+
- Routers: 70%+ (integration)

### Protocolo Pre-commit

Antes de hacer push de cambios, SIEMPRE:

${precommit_steps}

Si algún test falla, no commitear. Fix primero.

### Regression Testing

Cuando un test existente falla tras un cambio:

- **No desactivar el test** — eso oculta un bug real
- **Investigar por qué falla**:
  - ¿El cambio rompió funcionalidad existente? → Fix del código
  - ¿El comportamiento requerido cambió intencionalmente? → Actualizar el test
  - ¿El test estaba mal escrito? → Corregir el test

<!-- origen: ~/.claude/CLAUDE.md §Testing -->
