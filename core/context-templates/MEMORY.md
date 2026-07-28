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
3. **Patrón repositorio** — queries en servicios/repositorios, no en routers
4. **No secrets en repo** — usar `.env` (en .gitignore) o vault del cloud
5. **Queries parametrizadas** — prevenir SQL injection

## Decisiones Arquitectónicas

_(registrar aquí las decisiones clave tomadas durante el proyecto)_

## Configuración de Claude Code

- `CLAUDE.md` — instrucciones proyecto
- `.claude/commands/` — slash commands
- `.claude/context/` — archivos de contexto por módulo (esta carpeta)
- `.claude/settings.json` — MCP servers

<!-- origen: UDLA_backend_ssh/.claude/context/MEMORY.md (generalizado) -->
