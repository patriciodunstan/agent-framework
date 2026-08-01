# ${stack} — Memoria de Proyecto

## Estado del Contexto

- **Última actualización**: YYYY-MM-DD
- **Rama principal**: main
- **Rama en curso**: (ninguna)
- **CI/CD**: ${ci} → ${cloud}

## Archivos de Contexto por Módulo

- [architecture.md](architecture.md) — Stack, estructura, patrones arquitectónicos
- [api-endpoints.md](api-endpoints.md) — Endpoints REST del proyecto
- [data-models.md](data-models.md) — Modelos de datos y tipos
- [services-layer.md](services-layer.md) — Servicios y lógica de negocio

## Reglas de Trabajo Críticas

1. **NO inventar endpoints** — siempre verificar contra [api-endpoints.md](api-endpoints.md)
2. **NO inventar campos** — revisar modelos en [data-models.md](data-models.md)
3. **Patrón repositorio** — queries en servicios/repositorios, no en controladores
4. **No secrets en repo** — usar `.env` (en .gitignore) o vault del cloud
5. **Queries parametrizadas** — prevenir SQL injection

## Decisiones Arquitectónicas

_(las decisiones formales van en `docs/adr/`; registrá aquí un resumen si aplica)_

## Configuración de Copilot

- `.github/copilot-instructions.md` — instrucciones del proyecto
- `.github/prompts/` — prompts invocables con `/`
- `.github/agents/` — custom agents
- `.github/instructions/` — convenciones por tipo de archivo (`applyTo`)
- `docs/context/` — memoria del proyecto por módulo (esta carpeta)

<!-- generado por agent-framework (scope project, agente copilot) — fuente: core/context-templates/MEMORY.md (forma Copilot) -->
