# ${stack} — Memoria de Proyecto

## Estado del Contexto

- **Última actualización**: YYYY-MM-DD
- **Rama principal**: main
- **Rama en curso**: (ninguna)
- **CI/CD**: ${ci} → ${cloud}

## Archivos de Contexto por Módulo

Leer solo el que corresponda al módulo en que se trabaje:

- [architecture.md](architecture.md) — Stack, estructura, patrones
- [api-endpoints.md](api-endpoints.md) — Endpoints REST
- [data-models.md](data-models.md) — Modelos de datos y tipos
- [services-layer.md](services-layer.md) — Servicios y lógica de negocio

## Reglas de Trabajo Críticas

1. **NO inventar endpoints** — verificar contra [api-endpoints.md](api-endpoints.md)
2. **NO inventar campos** — revisar modelos en [data-models.md](data-models.md)
3. **Patrón repositorio** — queries en servicios/repositorios, no en controladores

## Decisiones Arquitectónicas

_(las decisiones formales van en `docs/adr/`; registrá aquí solo el resumen que
haga falta tener siempre a mano)_

## Dónde está la config

`.github/copilot-instructions.md` instrucciones · `.github/prompts/` prompts `/` ·
`.github/agents/` custom agents · `.github/instructions/` convenciones por tipo de
archivo (`applyTo`) · `docs/context/` esta memoria

<!-- generado por agent-framework (scope project, agente copilot) — fuente: core/context-templates/MEMORY.md (forma Copilot) -->
